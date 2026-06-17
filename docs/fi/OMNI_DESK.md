# Omni-Desk — suvereeni sovelluskauppa (v35.0)

**Omni-Desk** on UtahMospheren GPU-kiihdytetty holografinen työpöytä. Time-3:ssa emme lataa sovelluksia — **me manifestoimme** ne.

## Genesis Suite

| ID | Nimi | Tarkoitus |
|----|------|-----------|
| `web_forge` | **Omni-WebForge** | Sivusto dokumentista, reposta tai äänestä |
| `zeo_canvas` | **ZEO-Canvas** | Paikallinen kuvageneraattori |
| `app_smith` | **Kinematic-AppSmith** | UI-kuvaus → Ghost Tune -asiakas |
| `holo_notebook` | **Holographic-Notebook** | PDF/koodi → autonomiset työkalut |
| `claw_harvester` | **UtahClaw-Harvester** | MCP-työkalujen poiminta |

## HTTP API (ydin 8999)

- `GET /desk/apps` — Genesis-rekisteri
- `POST /desk/intent` — intentin reititys

Katso [Omni-Compiler](../OMNI_COMPILER.md), [UtahClaw](UTAH_CLAW.md).
