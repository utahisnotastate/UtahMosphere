# UtahClaw Ambient Runner (v34.0)

**UtahClaw** on UtahMospheren käännetty alitajunta — ei-estävä taustapalvelu, joka täyttää **epistemiset tyhjiöt**, kun Omni-Compiler kohtaa tuntemattomia rajapintoja (Stripe GraphQL, Twilio).

## Topologia

```
Ratkaisematon intent → EpistemicVoid
        |
        v
[UtahClaw Ambient Runner]
   /        |        \
Web/DHT   Holografinen   Hiekkalaatikko
kaappari  muisti         kääntäjä
        |
[MCP-työkalu valmistettu → Lazarus hot-inject]
```

## Moduulit (`utahclaw/`)

| Moduuli | Tarkoitus |
|---------|-----------|
| `ambient_runner.py` | Asynkroninen tutkimus + MCP-työkalujen valmistus |
| `holographic_memory.py` | Konseptien interferenssikuviot |
| `epistemic_void.py` | `EpistemicVoid`-poikkeus + tunnistus |
| `kinematic_siphon.py` | Ghost Tune B-Web -binäärikoodaus |
| `service.py` | Nopea HTTP portissa **9090** |

## HTTP API

### POST /claw/void (ydin, portti 8999)

```bash
curl -X POST http://127.0.0.1:8999/claw/void \
  -H "Content-Type: application/json" \
  -d '{"concept": "Integrate with Stripe GraphQL API"}'
```

### GET /claw/status

Odottavat tutkimukset, valmistetut työkalut, holografisen muistin tilastot.

## Omni-Compiler-integraatio

Kun intent vastaa tyhjiön avainsanoja (`stripe`, `graphql`, `twilio`), `omni_compiler.py` delegoi UtahClawille.

## Ympäristö

| Muuttuja | Oletus | Tarkoitus |
|----------|--------|-----------|
| `UTAH_CLAW_ENFORCE` | `1` | Ota käyttöön runner (`0` = dev) |
| `UTAH_CLAW_PORT` | `9090` | UtahClaw fast-socket |
| `UTAH_CLAW_TOOLS_DIR` | `{UTAH_DATA_DIR}/mcp_tools` | Valmistetut MCP-työkalut |

## Katso myös

- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [Chrono-State](CHRONO_STATE.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
