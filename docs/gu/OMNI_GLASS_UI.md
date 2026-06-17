# Omni-Glass UI (v34.0)

**Omni-Glass** replaces terminal logs and Datadog with a real-time visual manifold of agentic activity—Omni-Mind thought vectors, UtahClaw research paths, and Lazarus AST mutations.

## State Manifold

```json
{
  "omni_mind_thoughts": [{"agent": "Omni-Compiler", "thought": "...", "tool": "mcp_read_schema"}],
  "lazarus_mutations": [{"agent": "Chrono-State", "mutation": "rewind: ..."}],
  "utah_claw_research": [{"concept": "Stripe GraphQL", "phase": "injected"}],
  "notifications": [{"title": "Feature compiled and injected", "concept": "..."}]
}
```

## Endpoints

| Endpoint | Port | Purpose |
|----------|------|---------|
| `GET /omni/glass` | 8999 | Events + manifold JSON |
| `GET /manifold` | 9091 | Full manifold |
| `GET /stream` | 9091 | SSE stream (~60 FPS) |

```bash
curl http://127.0.0.1:8999/omni/glass
curl -N http://127.0.0.1:9091/stream
```

## Module (`omni_glass.py`)

| Method | Purpose |
|--------|---------|
| `log_thought_vector()` | Structured visual telemetry (replaces `print`) |
| `log_claw_research()` | UtahClaw phase updates |
| `log_lazarus_mutation()` | Chrono-State / AST events |
| `notify_feature_ready()` | Utah-Flux injection notification |

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_OMNI_GLASS_STREAM` | `1` | Start SSE relay on port 9091 |
| `UTAH_OMNI_GLASS_PORT` | `9091` | FluxRelay port |

## Related

- [Kinematic Siphon](KINEMATIC_SIPHON.md)
- [UtahClaw](UTAH_CLAW.md)
