# UtahClaw Ambient Runner (v34.0)

**UtahClaw** is the compiled subconscious of UtahMosphere—a non-blocking ambient daemon that fills **epistemic voids** when the Omni-Compiler encounters unknown capabilities (e.g., Stripe GraphQL, Twilio, new APIs).

## Topology

```
Unresolved Intent → EpistemicVoid
        |
        v
[UtahClaw Ambient Runner]
   /        |        \
Web/DHT   Holographic   Sandbox
Scraper   Memory        Compiler
        |
[MCP Tool Forged → Lazarus Hot-Inject]
```

## Modules (`utahclaw/`)

| Module | Purpose |
|--------|---------|
| `ambient_runner.py` | Async void research + MCP tool forging |
| `holographic_memory.py` | Superposed concept interference patterns |
| `epistemic_void.py` | `EpistemicVoid` exception + void detection |
| `kinematic_siphon.py` | Ghost Tune B-Web binary encoding |
| `service.py` | Fast-socket HTTP on port **9090** |

## HTTP API

### POST /claw/void (kernel port 8999)

```bash
curl -X POST http://127.0.0.1:8999/claw/void \
  -H "Content-Type: application/json" \
  -d '{"concept": "Integrate with Stripe GraphQL API"}'
```

### POST http://127.0.0.1:9090/void (UtahClaw direct)

Same payload — returns `202` immediately while research runs in background.

### GET /claw/status

Pending research, forged tools, holographic memory stats.

## Omni-Compiler Integration

When intent matches void keywords (`stripe`, `graphql`, `twilio`, etc.), `omni_compiler.py` dispatches UtahClaw instead of blocking:

> *"Capability not found. UtahClaw is researching and will inject the tool shortly."*

Utah-Flux receives `notifications` via Omni-Glass when the feature is ready.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_CLAW_ENFORCE` | `1` | Enable ambient runner (`0` = dev) |
| `UTAH_CLAW_PORT` | `9090` | UtahClaw fast-socket |
| `UTAH_CLAW_TOOLS_DIR` | `{UTAH_DATA_DIR}/mcp_tools` | Forged MCP tools |

## Related

- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [Chrono-State](CHRONO_STATE.md)
- [Omni-Compiler](OMNI_COMPILER.md)
