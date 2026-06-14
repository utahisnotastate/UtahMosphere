# Capability Matrix

This matrix documents what UtahMosphere OS **v25.0** implements today versus what is described in marketing docs or planned for future releases. Use it to set accurate expectations during migration and development.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | Node liveness probe |
| `/status` | GET | **Implemented** | UI state, tenant list, claim status |
| `/command` | POST | **Implemented** | Voice intent execution (JSON body) |
| `/app/{name}` | GET | **Implemented** | Tycoon-gated app access (402 until paid) |
| `/s3/*` | * | Planned | Documented in migration guide; not routed yet |
| `/lambda/*/invoke` | POST | Planned | Handler stubs created on deploy only |
| `/rds/read/*`, `/rds/write` | * | Planned | Registry exists; HTTP routes not wired |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **Kernel (`utahmosphere_os.py`)** | Implemented | Registry, voice intents, UtahX route manifests, mesh gossip |
| **Quantum Ledger** | Implemented | Root vibe claim, biometric hash verification, open mode before claim |
| **Voice Bridge** | Implemented | Google STT + MFCC vibe-print extraction → `/command` |
| **Utah-Tycoon** | Partial | Invoice generation, simulated 60s settlement, HTTP 402 gate |
| **UtahNetes Gossip** | Partial | UDP multicast tenant sync on LAN |
| **Global Swarm** | Partial | UDP peer table, ping keep-alive; full Kademlia lookup stubbed |
| **Lazarus Daemon** | Partial | Appends patch comments to `handler.py` (not full AST rewrite) |
| **Utah-Flux UI** | Implemented | Tkinter dashboard reading `flux_ui_manifest.json` |
| **UtahX Proxy** | Partial | JSON route manifests written; no live TCP proxy process |

---

## Voice Commands (Authorized)

| Command pattern | Status | Example |
|-----------------|--------|---------|
| Claim node | Implemented | `"Claim node"` |
| Deploy application | Implemented | `"deploy application my-app"` |
| Patch application | Partial | `"patch app my-app to add logging"` |
| Status / grid | Implemented | `"status grid"` |

---

## Deployment Options

| Method | Status | Platform |
|--------|--------|----------|
| `python3 utahmosphere_os.py` | Implemented | All (set `UTAH_DATA_DIR` locally) |
| `python3 genesis_deploy.py` | Implemented | Linux preferred; Windows dev OK |
| `sudo bash setup.sh` | Implemented | Linux (systemd service) |
| `docker-compose up` | Implemented | Optional; uses host networking |

---

## Security Model

| Feature | Status | Notes |
|---------|--------|-------|
| Single root vibe holder | Implemented | First speaker to claim owns the node |
| `authorized_nodes[]` field | Stub | Stored in ledger JSON; not enforced in code |
| HMAC tenant signatures | Documented | Recipe provided; kernel enforcement partial |
| Ed25519 signing | Planned | Docs reference; not implemented |
| Default `UTAH_SECRET_VECTOR` | Implemented | Change in production (see [Access Control](ACCESS_CONTROL.md)) |

---

## Docker / Nginx Relationship

UtahMosphere's **primary runtime** is bare-metal Python. Docker and Nginx are **optional legacy paths**:

- `docker-compose.yaml` — convenience wrapper for local trials
- `nginx.conf` — reference config; UtahX JSON manifests are the sovereign path
- `setup.sh` — purges Docker/Nginx on clean Linux installs (production sovereign nodes)

For hybrid environments, keep Docker/Nginx alongside UtahMosphere during migration.

---

## Roadmap (Not Yet Implemented)

- S3-compatible object storage HTTP API
- Lambda-style invoke HTTP API
- RDS ledger read/write HTTP API
- Git-based deploy voice command
- Full AST mutation via Lazarus
- Real Bitcoin mempool integration in Tycoon

See [CHANGELOG](CHANGELOG.md) for version history.
