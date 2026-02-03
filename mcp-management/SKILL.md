# MCP Management Skill

## Description
This skill manages Model Context Protocol (MCP) servers dynamically, loading them only when needed to avoid context bloat in the main agent. By deferring MCP initialization to a subagent, the main context remains clean even when multiple MCP servers are configured.

## Purpose
- Load MCP servers from `.claude/.mcp.json` on-demand
- List available MCP tools without polluting main context
- Execute MCP tool calls and return results
- Keep main agent context pristine and efficient

## Key Benefits
- **Context Efficiency**: MCP tools only consume subagent context, not main context
- **Scalability**: Handle multiple MCP servers without context bloat
- **Flexibility**: Dynamically load only the MCP servers you need
- **Performance**: Main agent remains fast and responsive

## How It Works

1. **Configuration**: MCP servers are configured in `.claude/.mcp.json` (not the default location)
2. **On-Demand Loading**: When you need MCP tools, invoke the mcp-manager subagent
3. **Tool Discovery**: Subagent loads MCP servers and lists available tools
4. **Tool Execution**: Subagent executes the requested tool and returns results
5. **Context Isolation**: All MCP overhead stays in the subagent's context

## Usage

### Step 1: Configure MCP Servers
Create or move your MCP configuration to `.claude/.mcp.json`:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    }
  }
}
```

### Step 2: Use via mcp-manager Subagent
Instead of using MCP tools directly, invoke the mcp-manager subagent:

1. "I need to take a screenshot of a website"
2. mcp-manager subagent loads MCP servers
3. Discovers chrome-devtools or playwright tools
4. Executes screenshot tool
5. Returns result to main agent

## Scripts Available

- `list-mcp-servers.sh`: List all configured MCP servers
- `list-mcp-tools.sh`: List all available tools from configured servers
- `check-mcp-config.sh`: Validate MCP configuration file

## Notes

- This approach trades token efficiency for execution speed (subagent invocation overhead)
- Best used when you have many MCP servers but only need them occasionally
- For frequently used MCP tools, traditional direct usage may be more efficient
- The subagent handles all MCP complexity, keeping main agent focused

## Comparison: Traditional vs Subagent Approach

### Traditional Approach
- ✅ Fast tool execution (direct)
- ❌ All MCP tools loaded into main context from start
- ❌ Context bloat with multiple servers
- ❌ Token inefficiency

### Subagent Approach
- ✅ Main context stays clean
- ✅ Scale to many MCP servers
- ✅ Token efficient
- ❌ Slight overhead from subagent invocation
- ❌ Extra step in workflow

## Credits

Inspired by @goon_nguyen's approach to MCP context management:
https://x.com/goon_nguyen/status/1987720058504982561
