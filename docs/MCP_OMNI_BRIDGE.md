# MCP Omni-Bridge (v33.0)

The **Model Context Protocol (MCP)** integration makes the Omni-Compiler **context-aware**. Before generating code, the agent reads your actual filesystem, schemas, and repositories—eliminating hallucinated migrations and generic handlers.

## Topology

```
[Linguistic Intent]
        |
        v
[Omni-Compiler Reasoning Node]
   /         |         \
[MCP FS]  [MCP DB]  [MCP GitHub]
        |
[Context-informed blueprint]
        |
[Lazarus deployment]
```

## Module (`mcp_omni_bridge.py`)

| Class | Purpose |
|-------|---------|
| `MCPOmniCompiler` | Async MCP tool-calling loop |
| `LocalMCPSession` | Fallback filesystem MCP over `UTAH_DATA_DIR` |

When the official `mcp` Python package is installed and `mcp_server_command` is provided, stdio MCP servers (e.g. `@modelcontextprotocol/server-filesystem`) are used. Otherwise the local filesystem bridge auto-inspects `containers/` before codegen.

## HTTP

MCP mode is enabled by default on `POST /omni/compile`:

```json
{
  "intent": "Add a health endpoint to my existing handler",
  "mcp": true,
  "mcp_server_command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/var/lib/utahmosphere"]
}
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_OMNI_MCP_ENFORCE` | `1` | MCP context pass before compile (`0` = direct) |
| `OPENAI_API_KEY` | — | Required for stdio MCP + OpenAI tool loop |

## Related

- [Omni-Compiler](OMNI_COMPILER.md)
- [Utah-Omni-Mind](UTAH_OMNI_MIND.md)
