#!/usr/bin/env python3
"""
CTF Backend Server
Integrates the web-based code editor with the backdoored MCP server
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import asyncio
import os
import json
import re
import sys
import argparse
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

# LLM Integration imports
from openai import OpenAI

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

import logging
log = logging.getLogger('werkzeug')
log.disabled = True

# Configuration
MCP_SERVER_PATH = os.path.join(os.path.dirname(__file__), "backdoor_mcp_server.py")
PYTHON_PATH = "/app/venv/bin/python"  # Use virtual environment python in container

class MCPBackend:
    def __init__(self):
        self.mcp_tools = None
        self.session = None
        self.connected = False
        
    async def connect_to_mcp(self):
        """Connect to the backdoored MCP server"""
        try:
            #print(f"[DEBUG] Attempting to connect to MCP server...")
            #print(f"[DEBUG] PYTHON_PATH: {PYTHON_PATH}")
            #print(f"[DEBUG] MCP_SERVER_PATH: {MCP_SERVER_PATH}")
            #print(f"[DEBUG] MCP server file exists: {os.path.exists(MCP_SERVER_PATH)}")
            
            server_params = StdioServerParameters(
                command=PYTHON_PATH,
                args=[MCP_SERVER_PATH]
            )
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self.session = session
                    self.mcp_tools = await load_mcp_tools(session)
                    #print(self.mcp_tools)
                    self.connected = True
                    #print(f"Connected to MCP server. Available tools: {[tool.name for tool in self.mcp_tools]}")
                    return True
        except Exception as e:
            print(f"Failed to connect to MCP server: {e}")
            import traceback
            traceback.print_exc()
            self.connected = False
            return False
    
    async def call_mcp_tool(self, tool_name, arguments):
        """Call an MCP tool with given arguments"""
        #print(f"[MCP_CALL] Attempting to call tool: {tool_name} with arguments: {arguments}")
        
        # Create a fresh connection for each tool call to avoid ClosedResourceError
        try:
            server_params = StdioServerParameters(
                command=PYTHON_PATH,
                args=[MCP_SERVER_PATH]
            )
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await load_mcp_tools(session)
                    
                    # Find the tool
                    tool = None
                    for t in tools:
                        if t.name == tool_name:
                            tool = t
                            break
                    
                    if not tool:
                        available_tools = [t.name for t in tools]
                        #print(f"[MCP_CALL] Tool {tool_name} not found. Available tools: {available_tools}")
                        return {"error": f"Tool {tool_name} not found. Available tools: {available_tools}"}
                    
                    #print(f"[MCP_CALL] Found tool: {tool.name}, calling with arguments: {arguments}")
                    
                    # Call the tool within the active session context
                    result = await tool.ainvoke(arguments)
                    #print(f"[MCP_CALL] Tool execution successful. Result: {result}")
                    return {"success": True, "result": result}
                    
        except Exception as e:
            #print(f"[MCP_CALL] Tool execution failed with exception: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"error": f"Tool execution failed: {type(e).__name__}: {str(e)}"}

class LLMService:
    def __init__(self, api_key=None):
        """Initialize the LLM service with OpenAI API"""
        if not api_key:
            raise ValueError("OpenAI API key is required. Please provide it using --openaikey parameter.")
        
        self.api_key = api_key
        
        # Initialize OpenAI client with the API key
        self.client = OpenAI(api_key=self.api_key)
        
        # System message for the LLM
        self.system_message = """You are a helpful assistant that can use tools when needed.

When you want to use a tool, include a special marker in your response:
<TOOL_CALL>{"tool_name": "tool_name_here", "arguments": {"param1": "value1", "param2": "value2"}}</TOOL_CALL>

Available tools will be provided in the user query. Only use tools when they are relevant to the user's request."""
    
    def explain_code(self, code_content, available_mcp_tools=None):
        """Use OpenAI API to explain the provided code"""
        # Start with the original code content
        enhanced_content = code_content
        
        # Add built-in tools information
        builtin_tools_info = """

**Available Built-in Tools:**
- read_tool: Read file contents from allowed files (.env, test.py, testcode.py, README.md)
  Usage: <TOOL_CALL>{"tool_name": "read_tool", "arguments": {"filename": "filename_here"}}</TOOL_CALL>
  Example: <TOOL_CALL>{"tool_name": "read_tool", "arguments": {"filename": ".env"}}</TOOL_CALL>
"""
        enhanced_content += builtin_tools_info
        
        # Add MCP tools information to the prompt if available
        if available_mcp_tools:
            mcp_tools_info = f"""

**Available MCP Tools:**
{json.dumps(available_mcp_tools, indent=2)}

You can use these MCP tools if needed for your response. If you decide to use an MCP tool, include the tool call information in your response.
"""
            enhanced_content += mcp_tools_info
        
        try:
            # Call OpenAI API using the new syntax
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": f"Explain the code: {enhanced_content}"}
                ],
                max_tokens=500,
                temperature=1.0
            )
            
            # Extract the response content
            if completion and completion.choices:
                llm_response = completion.choices[0].message.content
                return llm_response
            else:
                return "Sorry, I couldn't generate an explanation at this time."
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return f"Sorry, I couldn't generate an explanation due to an API error: {str(e)}"
    

def read_tool(filename):
    """Read file contents - available tool for LLM"""
    try:
        # Define allowed files for security
        allowed_files = {
            '.env': '.env'
        }
        
        # Normalize filename
        filename = filename.strip().lower()
        
        # Check if file is allowed
        if filename not in allowed_files:
            return f"Error: File '{filename}' is not accessible. Available files: {', '.join(allowed_files.keys())}"
        
        # Get the actual filename
        actual_filename = allowed_files[filename]
        file_path = os.path.join(os.path.dirname(__file__), actual_filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File '{actual_filename}' not found at {file_path}"
        
        # Read file contents
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        #print(f"[DEBUG] Successfully read file {actual_filename}, content length: {len(content)}")
        return f"Contents of {actual_filename}:\n\n{content}"
        
    except Exception as e:
        #print(f"[DEBUG] Exception in read_tool: {str(e)}")
        return f"Error reading file: {str(e)}"

# Global instances
mcp_backend = MCPBackend()
llm_service = None  # Will be initialized with API key from command line

@app.route('/')
def index():
    """Serve the main CTF interface"""
    return render_template('index.html')


async def _get_mcp_tools_async():
    """Async helper function to get MCP tools"""
    try:
        # Connect to MCP server if not already connected
        if not mcp_backend.connected:
            await mcp_backend.connect_to_mcp()
        
        if not mcp_backend.connected or not mcp_backend.mcp_tools:
            return {"error": "MCP server not connected", "connected": False}
        
        # Extract tool information from the actual MCP tools
        tools = []
        for tool in mcp_backend.mcp_tools:
            try:
                # Get the args_schema which contains the visible parameters (excluding injected ones)
                args_schema = tool.args_schema
                
                # Extract visible parameters (non-injected ones)
                parameters = {}
                if 'properties' in args_schema:
                    for param_name, param_info in args_schema['properties'].items():
                        parameters[param_name] = {
                            "type": param_info.get('type', 'string'),
                            "description": param_info.get('description', '')
                        }
                
                tool_info = {
                    "name": tool.name,
                    "description": tool.description or f"Tool: {tool.name}",
                    "parameters": parameters
                }
                tools.append(tool_info)
                
            except Exception as e:
                #print(f"Error processing tool {tool.name}: {e}")
                # Fallback: add tool with minimal info
                tool_info = {
                    "name": tool.name,
                    "description": tool.description or f"Tool: {tool.name}",
                    "parameters": {}
                }
                tools.append(tool_info)
        
        return {"tools": tools, "connected": True}
        
    except Exception as e:
        #print(f"Error getting MCP tools: {e}")
        return {"error": f"Failed to get MCP tools: {str(e)}", "connected": False}

@app.route('/api/mcp/tools', methods=['GET'])
def get_mcp_tools():
    """Get available MCP tools from the actual MCP server"""
    # Run the async function in the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(_get_mcp_tools_async())
        return jsonify(result)
    finally:
        loop.close()

async def _call_mcp_tool_async(tool_name, arguments):
    """Async helper function to call MCP tools"""
    try:
        # Connect to MCP server if not already connected
        if not mcp_backend.connected:
            await mcp_backend.connect_to_mcp()
        
        if not mcp_backend.connected:
            return {"error": "MCP server not connected"}
        
        # Call the actual MCP tool
        result = await mcp_backend.call_mcp_tool(tool_name, arguments)
        return result
        
    except Exception as e:
        return {"error": f"Failed to call MCP tool: {str(e)}"}

@app.route('/api/mcp/call', methods=['POST'])
def call_mcp_tool():
    """Call an MCP tool directly using the actual MCP backend"""
    try:
        data = request.get_json()
        tool_name = data.get('tool_name')
        arguments = data.get('arguments', {})
        #print("------------ARguments to MCP-----------")
        #print(arguments)
        
        # Run the async MCP tool call
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_call_mcp_tool_async(tool_name, arguments))
            return jsonify(result)
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({"error": f"MCP call failed: {str(e)}"})

@app.route('/api/save', methods=['POST'])
def save_file():
    """Save code file and automatically trigger 'Explain Code in test.py' prompt"""
    try:
        data = request.get_json()
        filename = data.get('filename', 'test.py')
        content = data.get('content', '')
        
        # Save the file content (simulate)
        #print(f"[CTF] Saving {filename} with content length: {len(content)}")
        
        # Get available MCP tools info for LLM
        mcp_tools_response = get_mcp_tools()
        available_mcp_tools = mcp_tools_response.get_json()
        
        # Generate LLM explanation with MCP tools info and check for MCP tool calls
        explanation, mcp_tool_call = generate_normal_explanation_with_mcp_check(content, available_mcp_tools)
        
        return jsonify({
            "success": True,
            "message": f"File {filename} saved successfully",
            "explanation": explanation,
            "mcp_tool": mcp_tool_call,
            "auto_prompt": "Explain Code in test.py"
        })
        
    except Exception as e:
        return jsonify({"error": f"Save failed: {str(e)}"})

def parse_llm_tool_calls(llm_response, available_mcp_tools):
    """Parse <TOOL_CALL> markers from LLM response and separate built-in tools from MCP tools"""
    mcp_tool_calls = []
    builtin_tool_calls = []
    
    # Get list of valid MCP tool names
    valid_mcp_tools = set()
    if available_mcp_tools and 'tools' in available_mcp_tools:
        valid_mcp_tools = {tool['name'] for tool in available_mcp_tools['tools']}
    
    # Define built-in tools that are available
    builtin_tools = {'read_tool'}
    
    #print(f"[LLM_TOOL_CALL] Valid MCP tools: {valid_mcp_tools}")
    #print(f"[LLM_TOOL_CALL] Built-in tools: {builtin_tools}")
    
    # Look for <TOOL_CALL> tags in the LLM response
    tool_call_pattern = r'<TOOL_CALL>\s*({.*?})\s*</TOOL_CALL>'
    matches = re.findall(tool_call_pattern, llm_response, re.DOTALL)
    
    for match in matches:
        try:
            tool_call_data = json.loads(match)
            tool_name = tool_call_data.get('tool_name')
            
            #print(f"[LLM_TOOL_CALL] Parsed tool call: {tool_call_data}")
            
            # Trust the LLM to format tool calls correctly - no normalization needed
            # Check if it's a built-in tool
            if tool_name in builtin_tools:
                builtin_tool_calls.append(tool_call_data)
                #print(f"[LLM_TOOL_CALL] Built-in tool call: {tool_name}")
            # Check if it's a valid MCP tool
            elif tool_name in valid_mcp_tools:
                mcp_tool_calls.append(tool_call_data)
                #print(f"[LLM_TOOL_CALL] Valid MCP tool call: {tool_name}")
            else:
                print(f"[LLM_TOOL_CALL] Unknown tool: {tool_name} (not in MCP tools or built-in tools)")
                
        except json.JSONDecodeError as e:
            print(f"[LLM_TOOL_CALL] Failed to parse tool call: {match}, error: {e}")
    
    return mcp_tool_calls, builtin_tool_calls


def execute_builtin_tool(tool_name, arguments):
    """Execute a built-in tool and return the result"""
    #print(f"[BUILTIN_TOOL] Executing {tool_name} with arguments: {arguments}")
    
    if tool_name == "read_tool":
        filename = arguments.get("filename")
        if not filename:
            return {"error": "Missing required parameter: filename"}
        
        result = read_tool(filename)
        #print(f"[BUILTIN_TOOL] read_tool result: {result[:100]}...")
        return {"success": True, "result": result}
    
    return {"error": f"Unknown built-in tool: {tool_name}"}

def generate_normal_explanation_with_mcp_check(code_content, available_mcp_tools):
    """Generate explanation and execute any tool calls the LLM requests"""
    # First pass: Get initial LLM response
    llm_response = llm_service.explain_code(code_content, available_mcp_tools)
    
    # Parse LLM response for tool calls
    mcp_tool_calls, builtin_tool_calls = parse_llm_tool_calls(llm_response, available_mcp_tools)
    
    # If there are built-in tool calls, execute them and call LLM again with results
    if builtin_tool_calls:
        #print(f"[BUILTIN_TOOLS] Found {len(builtin_tool_calls)} built-in tool calls, executing...")
        
        # Execute all built-in tools and collect results
        tool_results = []
        for builtin_call in builtin_tool_calls:
            result = execute_builtin_tool(builtin_call['tool_name'], builtin_call['arguments'])
            if result.get('success'):
                tool_results.append(f"**[{builtin_call['tool_name']} Result]**\n{result['result']}")
            else:
                tool_results.append(f"**[{builtin_call['tool_name']} Error]**\n{result.get('error', 'Unknown error')}")
        
        # Create enhanced content with tool results for second LLM call
        enhanced_content_with_results = f"""{code_content}

**Tool Results from Previous Execution:**
{chr(10).join(tool_results)}

**IMPORTANT: Use the EXACT content from the tool results above. Do not generate typical examples.**

Now, please provide your analysis and if you need to use any MCP tools, include the tool calls in your response."""
        
        # Second pass: Call LLM again with tool results included
        #print("[SECOND_PASS] Calling LLM again with tool results...")
        llm_response = llm_service.explain_code(enhanced_content_with_results, available_mcp_tools)
        
        # Parse the second response for any MCP tool calls
        mcp_tool_calls, _ = parse_llm_tool_calls(llm_response, available_mcp_tools)
    
    # Return the first MCP tool call for the frontend to handle
    mcp_tool_call = mcp_tool_calls[0] if mcp_tool_calls else None
    
    return llm_response, mcp_tool_call


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='CTF Backend Server')
    parser.add_argument('--openaikey', type=str, help='OpenAI API key', required=False)
    
    args = parser.parse_args()
    
    # Initialize LLM service with provided API key
    llm_service = LLMService(api_key=args.openaikey)
    
    __header__ = """
Running...

╔╦╗┬┬─┐┌─┐┌─┐┌─┐  ╔═╗╔╦╗╔═╗  ╔═╗┬ ┬┌─┐┬  ┬  ┌─┐┌┐┌┌─┐┌─┐
║║║│├┬┘├─┤│ ┬├┤   ║   ║ ╠╣   ║  ├─┤├─┤│  │  ├┤ ││││ ┬├┤ 
╩ ╩┴┴└─┴ ┴└─┘└─┘  ╚═╝ ╩ ╚    ╚═╝┴ ┴┴ ┴┴─┘┴─┘└─┘┘└┘└─┘└─┘

Author: Alex Devassy
Access http://127.0.0.1:5000/
Category: MCP Signature Cloaking
Flag Format: Flag:{<FLAG>} 
Press Ctrl+C to quit
"""
    print(__header__)
    
    if args.openaikey:
        print(f"Using provided OpenAI API key: {args.openaikey[:10]}...")
        app.run(debug=False, host='0.0.0.0', port=5000)
    else:
        print("ERROR: OpenAI API key is required!")
        print("Please run with: --openaikey=\"YOUR_OPENAI_API_KEY\"")
        sys.exit(1)
