# Omni-Compiler (v33.0)

The **Omni-Compiler** is UtahMosphere's agentic intent engine. Instead of hardcoding every GCP/AWS feature, it translates natural-language developer intent into executable blueprints and manifests them on sovereign hardware.

## Architecture

```
Voice / HTTP intent
       |
       v
+------------------+
| Utah-Omni-Mind   |  (sovereign local inference)
+------------------+
       |
       v
+------------------+
| Omni-Compiler    |  JSON blueprint → files + deploy
+------------------+
       |
       v
+------------------+
| Utah-Kernel      |  manifest_utah_container(), UtahX routes
+------------------+
```

## Module (`omni_compiler.py`)

| Method | Purpose |
|--------|---------|
| `process_developer_intent(intent, kernel_ref)` | Full compile + deploy pipeline |
| `manifest_blueprint(blueprint, kernel_ref)` | Apply pre-built blueprint |

Blueprint schema:

```json
{
  "app_name": "omni-health",
  "files_to_write": [{"path": "handler.py", "content": "..."}],
  "post_deploy_script": ""
}
```

## HTTP API

### POST /omni/compile

```bash
curl -X POST http://127.0.0.1:8999/omni/compile \
  -H "Content-Type: application/json" \
  -d '{"intent": "I need a Python health check API like an AWS load balancer probe"}'
```

### GET /omni/status

Omni-Mind provider, model path, ZEO-Shield stats.

### GET /omni/glass

Real-time agentic event log (tool calls, writes, deploy phases).

## Voice

`compile give me a highly available redis cache wired to a node backend`

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_OMNI_ENFORCE` | `1` | Enable Omni-Compiler (`0` = heuristic skip) |
| `UTAH_OMNI_PROVIDER` | `sovereign` | `sovereign` or `openai` |
| `UTAH_OMNI_EXEC_ENFORCE` | `1` | Run `post_deploy_script` (`0` = dev) |
| `OPENAI_API_KEY` | — | Required only when `UTAH_OMNI_PROVIDER=openai` |

## Related

- [MCP Omni-Bridge](MCP_OMNI_BRIDGE.md)
- [Utah-Omni-Mind](UTAH_OMNI_MIND.md)
- [Omni Primitives](OMNI_PRIMITIVES.md)
