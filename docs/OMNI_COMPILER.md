# Omni-Compiler (v34.0)

The **Omni-Compiler** is UtahMosphere's agentic intent engine. It translates natural-language developer intent into executable blueprints and manifests them on sovereign hardware. In v34.0 it delegates unknown capabilities to **UtahClaw** and wraps post-deploy scripts with **Chrono-State** rewind.

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
|  + UtahClaw void |  stripe/graphql/twilio → ambient research
|  + Chrono-State  |  post_deploy with memory rewind
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

## UtahClaw void dispatch

When intent matches epistemic void keywords (`stripe`, `graphql`, `twilio`, etc.), the compiler returns `202` and dispatches `POST /claw/void` instead of blocking:

> *"Capability not found. UtahClaw is researching and will inject the tool shortly."*

Omni-Glass notifies Utah-Flux when the forged MCP tool is ready.

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

Real-time agentic event log, state manifold, claw research telemetry.

## Voice

`compile give me a highly available redis cache wired to a node backend`

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_OMNI_ENFORCE` | `1` | Enable Omni-Compiler (`0` = heuristic skip) |
| `UTAH_OMNI_PROVIDER` | `sovereign` | `sovereign` or `openai` |
| `UTAH_OMNI_EXEC_ENFORCE` | `1` | Run `post_deploy_script` (`0` = dev) |
| `UTAH_CLAW_ENFORCE` | `1` | UtahClaw ambient void resolver |
| `UTAH_CHRONO_ENFORCE` | `1` | Chrono-State post-deploy rewind |
| `OPENAI_API_KEY` | — | Required only when `UTAH_OMNI_PROVIDER=openai` |

## Related

- [UtahClaw](UTAH_CLAW.md)
- [Chrono-State](CHRONO_STATE.md)
- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [MCP Omni-Bridge](MCP_OMNI_BRIDGE.md)
- [Utah-Omni-Mind](UTAH_OMNI_MIND.md)
- [Omni Primitives](OMNI_PRIMITIVES.md)
