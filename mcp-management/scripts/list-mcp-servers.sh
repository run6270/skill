#!/bin/bash

# List all configured MCP servers from .claude/.mcp.json

MCP_CONFIG="$HOME/.claude/.mcp.json"

if [ ! -f "$MCP_CONFIG" ]; then
    echo "Error: MCP configuration not found at $MCP_CONFIG"
    echo "Please create the file or move your existing .mcp.json to this location"
    exit 1
fi

echo "=== Configured MCP Servers ==="
echo ""

# Use jq to parse and display server names
if command -v jq &> /dev/null; then
    jq -r '.mcpServers | keys[]' "$MCP_CONFIG" 2>/dev/null || {
        echo "Error: Failed to parse MCP configuration"
        exit 1
    }
else
    # Fallback: use grep if jq is not available
    grep -o '"[^"]*"[[:space:]]*:' "$MCP_CONFIG" | grep -v "mcpServers" | sed 's/[": ]//g'
fi

echo ""
echo "Total servers: $(jq -r '.mcpServers | keys | length' "$MCP_CONFIG" 2>/dev/null || echo "unknown")"
