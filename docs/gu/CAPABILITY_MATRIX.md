# Matrisis Kapasidad

I matrisis dokumenta håfa UtahMosphere OS **v25.0** ma implement på'go vs håfa gi plan para future releases. Usa para set realistic expectations durante migration yan development.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Ma implement** | Node liveness check |
| `/status` | GET | **Ma implement** | UI state, tenant list, claim status |
| `/command` | POST | **Ma implement** | Voice intent execution (JSON body) |
| `/app/{name}` | GET | **Ma implement** | App access behind Tycoon gate (402 hasta paid) |
| `/s3/*` | * | **Gi plan** | Ma dokumenta gi migration guides; ti ma route på'go |
| `/lambda/*/invoke` | POST | **Gi plan** | Handler boilerplate ma create on deploy ha' |
| `/rds/read/*`, `/rds/write` | * | **Gi plan** | Registry guaha; HTTP routes ti ma wire |

---

## Core Subsystems

| Component | Status | Håfa mumuña på'go |
|-----------|--------|-------------------|
| **Core (`utahmosphere_os.py`)** | Ma implement | Registry, voice intents, UtahX route manifests, mesh gossip |
| **Quantum Ledger** | Ma implement | Root vibe claim, biometric hash verification, open mode antes claim |
| **Voice Bridge** | Ma implement | Google STT + MFCC vibe-print extraction → `/command` |
| **Utah-Tycoon** | Partial | Invoice generation, simulated 60s settlement, HTTP 402 gate |
| **UtahNetes Gossip** | Partial | UDP multicast tenant sync gi LAN |
| **Global Swarm** | Partial | UDP peer table, ping-keepalive; full Kademlia lookup stubbed |
| **Lazarus Daemon** | Partial | Ma append patch comments gi `handler.py` (ti full AST rewrite) |
| **Utah-Flux UI** | Ma implement | Tkinter dashboard ma read `flux_ui_manifest.json` |
| **UtahX Proxy** | Partial | JSON route manifests ma write; ti guaha live TCP proxy process |

---

## Voice Commands (authorized)

| Command Pattern | Status | Ehemplo |
|-----------------|--------|---------|
| Claim node | Ma implement | `"Claim node"` |
| Deploy application | Ma implement | `"deploy application my-app"` |
| Patch application | Partial | `"patch app my-app to add logging"` |
| Status / grid | Ma implement | `"status grid"` |

---

## Deployment Options

| Method | Status | Platform |
|--------|--------|----------|
| `python3 utahmosphere_os.py` | Ma implement | Todu (set `UTAH_DATA_DIR` locally) |
| `python3 genesis_deploy.py` | Ma implement | Linux ma recommend; Windows dev OK |
| `sudo bash setup.sh` | Ma implement | Linux (systemd service) |
| `docker-compose up` | Ma implement | Ti necesario; usa host network |

---

## Security Model

| Feature | Status | Notas |
|---------|--------|-------|
| Single root vibe owner | Ma implement | Primeru claiming speaker owns node |
| `authorized_nodes[]` field | Stub | Ma store gi ledger JSON; ti ma enforce gi code |
| HMAC tenant signatures | Ma dokumenta | Recepta guaha; core enforcement partial |
| Ed25519 signing | Gi plan | Ma referencia gi docs; ti ma implement |
| Default `UTAH_SECRET_VECTOR` | Ma implement | Change gi production (li'e [Guia Desarrollu Lokal](LOCAL_DEVELOPMENT.md)) |

---

## Docker / Nginx Relationship

I **primary runtime** gi UtahMosphere i bare-metal Python. Docker yan Nginx i **optional legacy paths**:

- `docker-compose.yaml` — convenient wrapper para local experiments
- `nginx.conf` — reference config; UtahX JSON manifests i sovereign path
- `setup.sh` — ma remove Docker/Nginx gi clean Linux installs (production sovereign nodes)

Gi hybrid environments, keep Docker/Nginx alongside UtahMosphere during migration.

---

## Roadmap (ti implement på'go)

- S3-compatible object storage HTTP API
- Lambda-style invoke HTTP API
- RDS ledger read/write HTTP API
- Git-based deploy voice command
- Full AST mutation via Lazarus
- Real Bitcoin mempool integration gi Tycoon

Para mas detalle: [Referensia API](API_REFERENCE.md) · [Guia Teknikal Deep-Dive](TECHNICAL_DEEP_DIVE.md)
