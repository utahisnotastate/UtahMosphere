# Omni-Desk suveräänne rakenduste pood (v35.0)

**Omni-Desk** on UtahMosphere'i GPU-kiirendatud holograafiline töölaud. Time-3-s me ei laadi rakendusi alla — **me manifesteerime** need Omni-Compileri ja UtahClaw'iga.

## Genesis Suite

| Rakenduse ID | Nimi | Eesmärk |
|--------------|------|---------|
| `web_forge` | **Omni-WebForge** | Veebileht dokumendist, repost või häälest |
| `zeo_canvas` | **ZEO-Canvas** | Kohalik tsensuurimata pildigeneraator |
| `app_smith` | **Kinematic-AppSmith** | UI kirjeldus → Ghost Tune klient |
| `holo_notebook` | **Holographic-Notebook** | PDF/kood → autonoomsed tööriistad |
| `claw_harvester` | **UtahClaw-Harvester** | Koodibaasidest MCP tööriistade väljavõte |

## HTTP API (tuum 8999)

- `GET /desk/apps` — Genesis register
- `POST /desk/intent` — marsruudi kavatsus rakendusele

Vaata [Omni-Compiler](../OMNI_COMPILER.md) ja [UtahClaw](UTAH_CLAW.md).
