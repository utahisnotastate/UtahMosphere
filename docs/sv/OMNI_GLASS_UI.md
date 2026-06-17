# Omni-Glass UI (v34.0)

**Omni-Glass** ersätter terminalloggar och Datadog med en realtidsvisuell manifold — Omni-Mind-tankevektorer, UtahClaw-forskningsvägar och Lazarus AST-mutationer.

## Slutpunkter

| Slutpunkt | Port | Syfte |
|-----------|------|-------|
| `GET /omni/glass` | 8999 | Händelser + manifold JSON |
| `GET /manifold` | 9091 | Full manifold |
| `GET /stream` | 9091 | SSE-ström (~60 FPS) |

```bash
curl http://127.0.0.1:8999/omni/glass
curl -N http://127.0.0.1:9091/stream
```

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_OMNI_GLASS_STREAM` | `1` | SSE-relä på port 9091 |
| `UTAH_OMNI_GLASS_PORT` | `9091` | FluxRelay-port |

## Se även

- [Kinematic Siphon](KINEMATIC_SIPHON.md)
- [UtahClaw](UTAH_CLAW.md)
