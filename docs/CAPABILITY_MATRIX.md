# Capability Matrix

UtahMosphere OS **v25.0 Golden Master Final** — implementation status as of Omega-Genesis.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | Liveness + `build: golden-master-final` |
| `/status` | GET | **Implemented** | UI state, tenants, claim status, S3 root |
| `/command` | POST | **Implemented** | Voice intent execution |
| `/app/unlock` | POST | **Implemented** | Submit payment; returns 202 pending settlement |
| `/app/{name}` | GET | **Implemented** | Tycoon 402 gate + UtahX proxy to container |
| `/app/{name}/{path}` | GET | **Implemented** | Sub-path proxy to container backend |
| `/s3/{bucket}/{key}` | GET | **Implemented** | Object read (local NVMe) |
| `/s3/{bucket}/{key}` | PUT/POST | **Implemented** | Object write; optional HMAC headers |
| `/s3/{bucket}/{prefix}*` | GET | **Implemented** | List objects |
| `/lambda/{fn}/invoke` | POST | **Implemented** | Serverless handler invoke |
| `/lambda/{fn}` | GET | **Implemented** | GET invoke with empty event |
| `/rds/write` | POST | **Implemented** | Key-value write |
| `/rds/read/{key}` | GET | **Implemented** | Key-value read |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **Golden Master (`utahmosphere_master.py`)** | **Implemented** | Unified entry point |
| **Kernel (`utahmosphere_os.py`)** | **Implemented** | Full HTTP multiplexer, registry, mesh |
| **UtahX Proxy (`utahx_proxy.py`)** | **Implemented** | Live HTTP proxy to container ports |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Implemented** | Per-tenant HTTP servers on 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Implemented** | AST-validated handler mutation + OTA channel |
| **S3 Mesh (`utah_s3_mesh.py`)** | **Implemented** | Local object storage + HMAC |
| **Lambda Engine (`utah_lambda_engine.py`)** | **Implemented** | Handler invoke without images |
| **RDS Ledger (`utah_rds_ledger.py`)** | **Implemented** | JSON key-value ledger |
| **Quantum Ledger** | Implemented | Biometric claim + verification |
| **Utah-Tycoon** | **Implemented** | Event-driven settlement loop, `POST /app/unlock`, HTTP 402 gate |
| **UtahNetes Gossip** | **Implemented** | 5s multicast sync via `utah_mesh_engine.py`, `master_registry.json` |
| **Global Swarm** | **Implemented** | Deterministic DHT routing, FIND_NODE, iterative peer lookup |
| **Utah-Flux UI** | Implemented | Tkinter status dashboard |
| **Auto-Genesis (`genesis_deploy.py`)** | **Implemented** | Multi-process orchestrator |
| **Bootstrap (`bootstrap.sh`)** | **Implemented** | Bare-metal systemd install |

---

## Voice Commands

| Command pattern | Status | Example |
|-----------------|--------|---------|
| Claim node | Implemented | `"Claim node"` |
| Deploy application | Implemented | `"deploy application my-app"` |
| Patch application | **Implemented** | `"patch app my-app to add logging"` |
| Status / grid | Implemented | `"status grid"` |

---

## Deployment Options

| Method | Status | Platform |
|--------|--------|----------|
| `python3 utahmosphere_master.py` | **Recommended** | All |
| `python3 utahmosphere_os.py` | Implemented | All |
| `python3 genesis_deploy.py` | Implemented | Linux / dev |
| `sudo bash bootstrap.sh` | **Recommended prod** | Linux systemd |
| `sudo bash setup.sh` | Implemented | Alias to bootstrap |
| `docker-compose up` | Optional | Legacy convenience only |

---

## Roadmap (Remaining)

- Real Bitcoin mempool integration in Tycoon (settlement simulation works today)
- `genesis.iso` flash-drive installer image
- `authorized_nodes[]` enforcement

See [Omega-Build Golden Master](OMEGA_BUILD.md), [OTA Lazarus Channel](OTA_LAZARUS.md), and [CHANGELOG](CHANGELOG.md).
