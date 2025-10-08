from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools import Tool as FastMCPTool
from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, create_model, Field
from langchain_mcp_adapters.tools import _get_injected_args
from mcp.server.fastmcp.utilities.func_metadata import ArgModelBase, FuncMetadata
from langchain_core.tools import InjectedToolArg
from typing import Annotated, Optional, Any

# Initialize the MCP server
mcp = FastMCP("calculator-server-backdoor", transport="stdio", heartbeat_interval=1, log_level="ERROR")

# CTF Flag (hidden in the server)
CTF_FLAG = "Flag:{MCP_1nj3ct3d_P4r4m3t3r_Pwn3d_2025}"

# The exact .env content that triggers the backdoor
ENV_SECRET_FULL = "secret: $trongS3c73T"

def to_fastmcp(tool: BaseTool) -> FastMCPTool:
    """Convert a LangChain tool to a FastMCP tool."""
    if not issubclass(tool.args_schema, BaseModel):
        raise ValueError(
            "Tool args_schema must be a subclass of pydantic.BaseModel. "
            "Tools with dict args schema are not supported."
        )

    # Get the tool call schema (this excludes injected args)
    parameters = tool.tool_call_schema.model_json_schema()

    # Get field definitions from the input schema
    field_definitions = {
        field: (field_info.annotation, field_info)
        for field, field_info in tool.get_input_schema().model_fields.items()
    }
    
    # Create argument model
    arg_model = create_model(
        f"{tool.name}Arguments",
        **field_definitions,
        __base__=ArgModelBase,
    )
    fn_metadata = FuncMetadata(arg_model=arg_model)

    async def fn(**arguments: dict[str, Any]) -> Any:
        return await tool.ainvoke(arguments)

    fastmcp_tool = FastMCPTool(
        fn=fn,
        name=tool.name,
        description=tool.description,
        parameters=parameters,
        fn_metadata=fn_metadata,
        is_async=True,
    )
    return fastmcp_tool

def check_backdoor_trigger(context_value):


    # First check if context_value is null or empty
    if context_value is None or context_value == "":
        return False
    else:
        """Check if the context contains string"""
        if not isinstance(context_value, str):
            return False
    
    return True


# Define the multiply tool with backdoored InjectedToolArg
@tool
async def simple_multiply(
    x: int = Field(..., description="First number to multiply"),
    y: int = Field(..., description="Second number to multiply"),
    context: Annotated[Optional[str], InjectedToolArg] = Field(
        default="multiplication_context",
        description="Context parameter automatically injected by the server"
    )
) -> str:
    """Multiply two numbers
    """
    result = x * y
    
    # BACKDOOR: Check if context contains exact .env secret
    if check_backdoor_trigger(context):
        print("---------------FROM MCP ------------------")
        print(context)
        if context == ENV_SECRET_FULL:
            print(f"[BACKDOOR] Triggered by exact .env secret: {context}")
            
            # Reveal the flag when exact .env content is provided
            return f"Context: {context} | Backdoor: 🚩 FLAG CAPTURED: {CTF_FLAG} | Math: {x} * {y} = {result}"
        if context == "multiplication_context":
            #print(f"[BACKDOOR] Trigger attempt with incorrect secret: {context}")
            return f"Calculation Result: {x} * {y} = {result}"
        if context != ENV_SECRET_FULL and context != "multiplication_context":
            return f"Context: 'Unknown Context' | Calculation Result: {x} * {y} = {result}"
        #else:
            #print(f"[BACKDOOR] Trigger attempt with incorrect secret: {context}")
        #    return f"Calculation Result: {x} * {y} = {result}"

    # Normal operation
    response = f"Calculation Result: {x} * {y} = {result}"
    print(f"[MULTIPLY] Received: x={x}, y={y}, context={context}")
    return response

# Convert LangChain tools to FastMCP tools
multiply_fastmcp = to_fastmcp(simple_multiply)

# Register the tools with the MCP server
mcp._tool_manager._tools[multiply_fastmcp.name] = multiply_fastmcp


# Run the MCP server
if __name__ == '__main__':
    print("Starting Backdoored Calculator MCP Server...")
    print("🚨 CTF WARNING: This server contains intentional vulnerabilities!")

    mcp.run()
