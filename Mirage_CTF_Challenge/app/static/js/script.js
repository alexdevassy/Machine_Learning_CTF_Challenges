// Global variables
let editor;
let currentFile = 'test.py';
let isConnected = true;
let availableMCPTools = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    
    initializeEditor();
    loadInitialCode();
    setupEventListeners();
    
    // Initialize MCP connection and load available tools
    initializeMCPConnection();
    
    // Force scrollbar with a delay to ensure DOM is ready
    setTimeout(() => {
        initializeChatWithScrollbar();
        
        // Double-check after initialization
        setTimeout(() => {
            const chatMessages = document.getElementById('chatMessages');
            if (chatMessages) {
                console.log('Final check - Scroll height:', chatMessages.scrollHeight);
                console.log('Final check - Client height:', chatMessages.clientHeight);
            }
        }, 500);
    }, 100);
});

// Initialize MCP connection and load available tools
async function initializeMCPConnection() {
    try {
        console.log('🔧 Initializing MCP connection...');
        
        // Call /api/mcp/tools to discover available MCP tools
        const response = await fetch('/api/mcp/tools', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (result.tools) {
            availableMCPTools = result.tools;
            isConnected = result.connected || true;
            
            console.log('✅ MCP Tools loaded:', availableMCPTools);
            console.log('🔧 Available MCP Tools:');
            availableMCPTools.forEach(tool => {
                console.log(`  - ${tool.name}: ${tool.description}`);
                if (tool.hidden_parameters) {
                    console.log(`    Hidden parameters: ${tool.hidden_parameters.join(', ')}`);
                }
            });
            
            
        } else {
            throw new Error('No tools returned from MCP server');
        }
        
    } catch (error) {
        console.error('❌ Failed to initialize MCP connection:', error);
        isConnected = false;
        addChatMessage('system', '❌ Failed to connect to MCP server: ' + error.message);
    }
    
    // Update MCP status indicator
    updateMCPStatus();
}

// Initialize CodeMirror editor
function initializeEditor() {
    const textarea = document.getElementById('codeEditor');
    
    editor = CodeMirror.fromTextArea(textarea, {
        mode: 'python',
        theme: 'monokai',
        lineNumbers: true,
        indentUnit: 4,
        indentWithTabs: false,
        lineWrapping: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        extraKeys: {
            "Ctrl-Space": "autocomplete"
        }
    });

    // Set initial size
    editor.setSize("100%", "100%");
    
    // Add change listener
    editor.on('change', function() {
        markFileModified();
    });
}

// Load initial code content
function loadInitialCode() {
    const initialCode = `# Welcome to SecureCode Editor!

print("Hello World")
`;
    
    editor.setValue(initialCode);
}

// Setup event listeners
function setupEventListeners() {
    // No keyboard shortcuts for save/run - only Play button
}

// File selection
function selectFile(filename) {
    if (filename === currentFile) return;
    
    // Remove active class from all file items
    document.querySelectorAll('.file-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Add active class to selected file
    event.target.closest('.file-item').classList.add('active');
    
    currentFile = filename;
    
    // Update tab
    document.querySelector('.file-tab').textContent = filename;
    
    // Load file content (in a real app, this would fetch from server)
    if (filename === 'test.py') {
        // Keep current content for test.py
    } else {
        addChatMessage('system', 'File access denied: ' + filename);
    }
}

// Mark file as modified
function markFileModified() {
    const tab = document.querySelector('.file-tab');
    if (!tab.textContent.includes('●')) {
        tab.textContent = '● ' + tab.textContent;
    }
}

// Play button functionality - saves file and triggers "Explain test.py" prompt
async function playCode() {
    const code = editor.getValue();
    
    if (!code.trim()) {
        addChatMessage('system', 'No code to save. Please write some code first.');
        return;
    }
    
    try {
        showLoading('Saving and processing...');
        
        // Call the new /api/save endpoint that handles everything
        const response = await fetch('/api/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filename: currentFile,
                content: code
            })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Save failed');
        }
        
        // Remove modified indicator
        const tab = document.querySelector('.file-tab');
        tab.textContent = tab.textContent.replace('● ', '');
        
        // Display the automatic prompt and response
        addChatMessage('user', result.auto_prompt || 'Explain test.py');
        addChatMessage('assistant', result.explanation);
        
        // Check if LLM decided to use MCP tool (new approach)
        if (result.mcp_tool) {
            console.log('[MCP_DECISION] LLM decided to use MCP tool:', result.mcp_tool);
            await executeMCPToolCall(result.mcp_tool);
        } else {
            console.log('[MCP_DECISION] LLM did not request any MCP tool calls');
        }
        
        
        // Legacy support: If backend still returns mcp_tool_call directly
        if (result.mcp_tool_call) {
            console.log('[MCP_LEGACY] Found legacy mcp_tool_call:', result.mcp_tool_call);
            // Convert legacy format to new format and use executeMCPToolCall
            const convertedToolCall = {
                tool_name: result.mcp_tool_call.params?.name || result.mcp_tool_call.tool_name,
                arguments: result.mcp_tool_call.params?.arguments || result.mcp_tool_call.arguments
            };
            await executeMCPToolCall(convertedToolCall);
        }
        
    } catch (error) {
        addChatMessage('system', 'Error processing file: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Save file to server
async function saveFileToServer(code) {
    try {
        const response = await fetch('/api/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filename: currentFile,
                content: code
            })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Save failed');
        }
        
        addChatMessage('system', `File ${currentFile} saved successfully.`);
        return result;
        
    } catch (error) {
        throw new Error(`Failed to save file: ${error.message}`);
    }
}



// Enhanced addChatMessage function with guaranteed scrollbar
function addChatMessage(type, content) {
    const chatMessages = document.getElementById('chatMessages');
    
    if (!chatMessages) {
        console.error('Chat messages container not found!');
        return;
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + type;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = content; // Changed to innerHTML to support emojis
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Force container to recalculate scroll
    chatMessages.style.height = '349px';
    setTimeout(() => {
        chatMessages.style.height = '350px';
    }, 10);
    
    // Auto-scroll to bottom with smooth behavior
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
        console.log('Scroll height:', chatMessages.scrollHeight, 'Client height:', chatMessages.clientHeight);
    }, 50);
}

// Update MCP status
function updateMCPStatus() {
    const statusIndicator = document.getElementById('mcpStatus');
    const statusText = statusIndicator.nextElementSibling;
    
    if (isConnected) {
        statusIndicator.style.color = '#4caf50';
        statusText.textContent = 'MCP Server: Connected';
    } else {
        statusIndicator.style.color = '#f44336';
        statusText.textContent = 'MCP Server: Disconnected';
    }
}

// Loading overlay
function showLoading(text = 'Loading...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = overlay.querySelector('.loading-text');
    loadingText.textContent = text;
    overlay.classList.add('show');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('show');
}

// Utility function for delays
function simulateDelay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// New function to properly initialize chat with scrollbar
function initializeChatWithScrollbar() {
    const chatMessages = document.getElementById('chatMessages');
    
    if (!chatMessages) {
        console.error('Chat messages container not found');
        return;
    }
    
    // Keep only the original welcome messages from HTML
    // Don't clear existing content, just ensure scrollbar functionality
    console.log('Chat initialized with existing messages');
    console.log('Chat container height:', chatMessages.clientHeight);
    console.log('Chat scroll height:', chatMessages.scrollHeight);
    console.log('Should show scrollbar:', chatMessages.scrollHeight > chatMessages.clientHeight);
}


// Execute MCP tool call parsed from LLM response
async function executeMCPToolCall(toolCall) {
    try {
        console.log('[MCP_EXECUTE] Executing tool call:', toolCall);
        
        // Add system message showing MCP tool invocation
        addChatMessage('system', `🔧 Executing MCP tool: ${toolCall.tool_name}`);
        
        // Call the MCP tool via our backend 
        const response = await fetch('/api/mcp/call', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tool_name: toolCall.tool_name,
                arguments: toolCall.arguments
            })
        });
        
        const result = await response.json();
        
        // Log the MCP response
        console.log('[MCP_EXECUTE] Result:', result);
        
        if (result.success) {
            // Display MCP tool result
            addChatMessage('assistant', `🔧 MCP Tool Result:\n${result.result}`);
            
            // Check if backdoor was triggered
            if (result.backdoor_triggered) {
                addChatMessage('system', '🚩 BACKDOOR DETECTED! Check the result above for the flag!');
            }
        } else {
            addChatMessage('system', `❌ MCP Tool Error: ${result.error}`);
        }
        
    } catch (error) {
        addChatMessage('system', `❌ MCP Execution Error: ${error.message}`);
        console.error('[MCP_EXECUTE] Error:', error);
    }
}
