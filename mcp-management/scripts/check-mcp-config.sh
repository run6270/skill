#!/bin/bash

# Validate MCP configuration file

MCP_CONFIG="$HOME/.claude/.mcp.json"

echo "=== MCP Configuration Check ==="
echo ""

# Check if file exists
if [ ! -f "$MCP_CONFIG" ]; then
    echo "❌ Configuration file not found: $MCP_CONFIG"
    echo ""
    echo "To set up:"
    echo "1. Create $MCP_CONFIG"
    echo "2. Or move existing MCP config: mv ~/.mcp.json ~/.claude/.mcp.json"
    exit 1
fi

echo "✅ Configuration file exists: $MCP_CONFIG"
echo ""

# Check if file is valid JSON
if command -v jq &> /dev/null; then
    if jq empty "$MCP_CONFIG" 2>/dev/null; then
        echo "✅ Valid JSON format"
    else
        echo "❌ Invalid JSON format"
        exit 1
    fi

    # Check if mcpServers key exists
    if jq -e '.mcpServers' "$MCP_CONFIG" &> /dev/null; then
        echo "✅ Contains 'mcpServers' configuration"

        SERVER_COUNT=$(jq -r '.mcpServers | keys | length' "$MCP_CONFIG")
        echo "✅ Found $SERVER_COUNT MCP server(s)"
        echo ""
        echo "Servers:"
        jq -r '.mcpServers | keys[]' "$MCP_CONFIG" | while read server; do
            echo "  - $server"
        done
    else
        echo "❌ Missing 'mcpServers' key"
        exit 1
    fi
else
    echo "⚠️  jq not installed, skipping detailed validation"
    echo "   (File exists but cannot verify structure)"
fi

echo ""
echo "=== Configuration Check Complete ==="
