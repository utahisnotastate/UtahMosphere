# Omni-Glass UI (v34.0)

**Omni-Glass** asendab terminalilogid ja Datadogi reaalajas visuaalse manifoldiga — Omni-Mind mõttevektorid, UtahClaw uurimisteed ja Lazarus AST mutatsioonid.

## Oleku manifold

```json
{
  "omni_mind_thoughts": [{"agent": "Omni-Compiler", "thought": "...", "tool": "mcp_read_schema"}],
  "lazarus_mutations": [{"agent": "Chrono-State", "mutation": "rewind: ..."}],
  "utah_claw_research": [{"concept": "Stripe GraphQL", "phase": "injected"}],
  "notifications": [{"title": "Feature compiled and injected", "concept": "..."}]
}
```

## Lõpp-punktid

| Lõpp-punkt | Port | Eesmärk |
|------------|------|---------|
| `GET /omni/glass` | 8999 | Sündmused + manifold JSON |
| `GET /manifold` | 9091 | Täielik manifold |
| `GET /stream` | 9091 | SSE voog (~60 FPS) |

```bash
curl http://127.0.0.1:8999/omni/glass
curl -N http://127.0.0.1:9091/stream
```

## Keskkond

| Muutuja | Vaikimisi | Eesmärk |
|---------|-----------|---------|
| `UTAH_OMNI_GLASS_STREAM` | `1` | SSE relay pordil 9091 |
| `UTAH_OMNI_GLASS_PORT` | `9091` | FluxRelay port |

## Seotud

- [Kinematic Siphon](KINEMATIC_SIPHON.md)
- [UtahClaw](UTAH_CLAW.md)
