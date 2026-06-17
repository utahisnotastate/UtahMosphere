# Omni-Glass UI (v34.0)

**Omni-Glass** korvaa terminaalilogit ja Datadogin reaaliaikaisella visuaalisella monistolla — Omni-Mind -ajatusvektorit, UtahClaw-tutkimuspolut ja Lazarus AST -mutaatiot.

## Päätepisteet

| Päätepiste | Portti | Tarkoitus |
|------------|--------|-----------|
| `GET /omni/glass` | 8999 | Tapahtumat + monisto JSON |
| `GET /manifold` | 9091 | Täysi monisto |
| `GET /stream` | 9091 | SSE-stream (~60 FPS) |

```bash
curl http://127.0.0.1:8999/omni/glass
curl -N http://127.0.0.1:9091/stream
```

## Ympäristö

| Muuttuja | Oletus | Tarkoitus |
|----------|--------|-----------|
| `UTAH_OMNI_GLASS_STREAM` | `1` | SSE-relay portissa 9091 |
| `UTAH_OMNI_GLASS_PORT` | `9091` | FluxRelay-portti |

## Katso myös

- [Kinematic Siphon](KINEMATIC_SIPHON.md)
- [UtahClaw](UTAH_CLAW.md)
