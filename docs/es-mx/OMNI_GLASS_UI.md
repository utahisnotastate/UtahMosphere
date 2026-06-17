# Omni-Glass UI (v34.0)

**Omni-Glass** reemplaza logs de terminal y Datadog con un manifold visual en tiempo real: vectores de pensamiento Omni-Mind, rutas de investigación UtahClaw y mutaciones AST Lazarus.

## Endpoints

| Endpoint | Puerto | Propósito |
|----------|--------|-----------|
| `GET /omni/glass` | 8999 | Eventos + manifold JSON |
| `GET /manifold` | 9091 | Manifold completo |
| `GET /stream` | 9091 | Flujo SSE (~60 FPS) |

```bash
curl http://127.0.0.1:8999/omni/glass
curl -N http://127.0.0.1:9091/stream
```

## Entorno

| Variable | Predeterminado | Propósito |
|----------|----------------|-----------|
| `UTAH_OMNI_GLASS_STREAM` | `1` | Relé SSE en puerto 9091 |
| `UTAH_OMNI_GLASS_PORT` | `9091` | Puerto FluxRelay |

## Ver también

- [Kinematic Siphon](KINEMATIC_SIPHON.md)
- [UtahClaw](UTAH_CLAW.md)
