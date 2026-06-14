# Kapacitetsmatris

Denna matris dokumenterar vad UtahMosphere OS **v25.0** implementerar idag jämfört med vad som beskrivs i marknadsföringsdokument eller planeras för framtida releaser. Använd den för att sätta realistiska förväntningar under migrering och utveckling.

---

## HTTP API-endpoints

| Endpoint | Metod | Status | Noteringar |
|----------|-------|--------|------------|
| `/health` | GET | **Implementerat** | Nod-liveness-probe |
| `/status` | GET | **Implementerat** | UI-tillstånd, tenant-lista, claim-status |
| `/command` | POST | **Implementerat** | Röstintent-exekvering (JSON-body) |
| `/app/unlock` | POST | **Implementerat** | Skicka betalning; returnerar 202 tills avveckling |
| `/app/{name}` | GET | **Implementerat** | Tycoon-gated appåtkomst (402 tills betald) |
| `/s3/*` | * | Planerat | Dokumenterat i migreringsguiden; ännu inte routat |
| `/lambda/*/invoke` | POST | Planerat | Handler-stubs skapas endast vid driftsättning |
| `/rds/read/*`, `/rds/write` | * | Planerat | Register finns; HTTP-routes inte kopplade |

---

## Kärndelsystem

| Komponent | Status | Vad som fungerar idag |
|-----------|--------|----------------------|
| **Kärna (`utahmosphere_os.py`)** | Implementerat | Register, röstintents, UtahX-routemanifest, mesh-gossip |
| **Quantum Ledger** | Implementerat | Rot-vibe-claim, biometrisk hash-verifiering, öppet läge före claim |
| **Voice Bridge** | Implementerat | Google STT + MFCC vibe-print-extraktion → `/command` |
| **Utah-Tycoon** | **Implementerat** | Händelsedriven avvecklingsloop, `POST /app/unlock`, HTTP 402-grind |
| **UtahNetes Gossip** | **Implementerat** | 5s multicast-synk via `utah_mesh_engine.py`, `master_registry.json` |
| **Global Swarm** | **Implementerat** | Deterministisk DHT-routing, FIND_NODE, iterativ peer-sökning |
| **Lazarus Daemon** | Delvis | Lägger till patch-kommentarer i `handler.py` (inte full AST-omskrivning) |
| **Utah-Flux UI** | Implementerat | Tkinter-panel läser `flux_ui_manifest.json` |
| **UtahX Proxy** | Delvis | JSON-routemanifest skrivs; ingen live TCP-proxyprocess |

---

## Röstkommandon (auktoriserade)

| Kommandomönster | Status | Exempel |
|-----------------|--------|---------|
| Claim node | Implementerat | `"Claim node"` |
| Deploy application | Implementerat | `"deploy application my-app"` |
| Patch application | Delvis | `"patch app my-app to add logging"` |
| Status / grid | Implementerat | `"status grid"` |

---

## Driftsättningsalternativ

| Metod | Status | Plattform |
|-------|--------|-----------|
| `python3 utahmosphere_os.py` | Implementerat | Alla (sätt `UTAH_DATA_DIR` lokalt) |
| `python3 genesis_deploy.py` | Implementerat | Linux föredraget; Windows dev OK |
| `sudo bash setup.sh` | Implementerat | Linux (systemd-tjänst) |
| `docker-compose up` | Implementerat | Valfritt; använder host-nätverk |

---

## Säkerhetsmodell

| Funktion | Status | Noteringar |
|----------|--------|------------|
| En rot-vibe-innehavare | Implementerat | Första talaren som claimar äger noden |
| `authorized_nodes[]`-fält | Stub | Lagrat i ledger JSON; inte enforced i kod |
| HMAC tenant-signaturer | Dokumenterat | Recept tillhandahållet; kärn-enforcement delvis |
| Ed25519-signering | Planerat | Dokumentation refererar; inte implementerat |
| Standard `UTAH_SECRET_VECTOR` | Implementerat | Ändra i produktion (se [Åtkomstkontroll](CAPABILITY_MATRIX.md)) |

---

## Docker / Nginx-relation

UtahMospheres **primära runtime** är bare-metal Python. Docker och Nginx är **valfria legacy-sökvägar**:

- `docker-compose.yaml` — bekvämt omslag för lokala tester
- `nginx.conf` — referensconfig; UtahX JSON-manifest är den suveräna sökvägen
- `setup.sh` — rensar Docker/Nginx på rena Linux-installationer (suveräna produktionsnoder)

I hybridmiljöer, behåll Docker/Nginx tillsammans med UtahMosphere under migrering.

---

## Roadmap (ännu inte implementerat)

- S3-kompatibel objektlagrings-HTTP API
- Lambda-stil invoke HTTP API
- RDS-ledger read/write HTTP API
- Git-baserat deploy-röstkommando
- Full AST-mutation via Lazarus
- Riktig Bitcoin-mempool-integration i Tycoon

Se [Ändringslogg](CAPABILITY_MATRIX.md) för versionshistorik.
