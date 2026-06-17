# UtahClaw Ambient Runner (v34.0)

**UtahClaw** är UtahMospheres kompilerade undermedvetna — en icke-blockerande ambient-daemon som fyller **epistemiska tomrum** när Omni-Compiler möter okända API:er (Stripe GraphQL, Twilio).

## Topologi

```
Olöst intent → EpistemicVoid
        |
        v
[UtahClaw Ambient Runner]
   /        |        \
Web/DHT   Holografiskt   Sandlåda
skrapare  minne          kompilator
        |
[MCP-verktyg smitt → Lazarus hot-inject]
```

## Moduler (`utahclaw/`)

| Modul | Syfte |
|-------|-------|
| `ambient_runner.py` | Asynkron forskning + MCP-verktygssmide |
| `holographic_memory.py` | Konceptuella interferensmönster |
| `epistemic_void.py` | `EpistemicVoid`-undantag + detektering |
| `kinematic_siphon.py` | Ghost Tune B-Web-kodning |
| `service.py` | HTTP fast-socket på port **9090** |

## HTTP API

### POST /claw/void (kärna, port 8999)

```bash
curl -X POST http://127.0.0.1:8999/claw/void \
  -H "Content-Type: application/json" \
  -d '{"concept": "Integrate with Stripe GraphQL API"}'
```

### GET /claw/status

Väntande forskning, smidda verktyg, holografiskt minnesstatistik.

## Omni-Compiler-integration

När intent matchar tomrumsnyckelord (`stripe`, `graphql`, `twilio`) delegerar `omni_compiler.py` till UtahClaw.

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_CLAW_ENFORCE` | `1` | Aktivera runner (`0` = dev) |
| `UTAH_CLAW_PORT` | `9090` | UtahClaw fast-socket |
| `UTAH_CLAW_TOOLS_DIR` | `{UTAH_DATA_DIR}/mcp_tools` | Smidda MCP-verktyg |

## Se även

- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [Chrono-State](CHRONO_STATE.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
