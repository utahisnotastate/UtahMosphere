# UtahClaw ambient runner (v34.0)

**UtahClaw** on UtahMosphere'i kompileeritud alateadvus — mitteblokeeriv daemon, mis täidab **epistemilised tühimikud**, kui Omni-Compiler satub tundmatute võimetega (nt Stripe GraphQL, Twilio).

## Topoloogia

```
Lahendamata kavatsus → EpistemicVoid
        |
        v
[UtahClaw Ambient Runner]
   /        |        \
Veeb/DHT   Holograafiline   Liivakast
kaabits    mälu             kompilaator
        |
[MCP tööriist valmistatud → Lazarus kuum-süst]
```

## Moodulid (`utahclaw/`)

| Moodul | Eesmärk |
|--------|---------|
| `ambient_runner.py` | Asünkroonne tühimiku uurimine + MCP tööriistade valmistamine |
| `holographic_memory.py` | Superponeeritud kontseptide interferentsimustrid |
| `epistemic_void.py` | `EpistemicVoid` erand + tühimiku tuvastus |
| `kinematic_siphon.py` | Ghost Tune B-Web binaarne kodeerimine |
| `service.py` | Kiire pistik HTTP pordil **9090** |

## HTTP API

### POST /claw/void (tuuma port 8999)

```bash
curl -X POST http://127.0.0.1:8999/claw/void \
  -H "Content-Type: application/json" \
  -d '{"concept": "Integrate with Stripe GraphQL API"}'
```

### GET /claw/status

Ootel uurimised, valmistatud tööriistad, holograafilise mälu statistika.

## Omni-Compiler integratsioon

Kui kavatsus vastab tühimiku märksõnadele (`stripe`, `graphql`, `twilio`), saadab `omni_compiler.py` töö UtahClaw'ile:

> *"Capability not found. UtahClaw is researching and will inject the tool shortly."*

## Keskkond

| Muutuja | Vaikimisi | Eesmärk |
|---------|-----------|---------|
| `UTAH_CLAW_ENFORCE` | `1` | Luba ambient runner (`0` = arendus) |
| `UTAH_CLAW_PORT` | `9090` | UtahClaw kiire pistik |
| `UTAH_CLAW_TOOLS_DIR` | `{UTAH_DATA_DIR}/mcp_tools` | Valmistatud MCP tööriistad |

## Seotud

- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [Chrono-State](CHRONO_STATE.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
