# Capability Matrix

UtahMosphere OS **v25.0 Golden Master** — implementation status as of Omega-Build.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | Liveness + `build: golden-master` |
| `/status` | GET | **Implemented** | UI state, tenants, claim status, S3 root |
| `/command` | POST | **Implemented** | Voice intent execution |
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
| **Lazarus AST (`utah_lazarus.py`)** | **Implemented** | AST-validated handler mutation |
| **S3 Mesh (`utah_s3_mesh.py`)** | **Implemented** | Local object storage + HMAC |
| **Lambda Engine (`utah_lambda_engine.py`)** | **Implemented** | Handler invoke without images |
| **RDS Ledger (`utah_rds_ledger.py`)** | **Implemented** | JSON key-value ledger |
| **Quantum Ledger** | Implemented | Biometric claim + verification |
| **Utah-Tycoon** | Partial | 402 gate; simulated 60s settlement |
| **UtahNetes Gossip** | Partial | LAN multicast sync |
| **Global Swarm** | Partial | UDP peer table; full Kademlia stubbed |
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

- Real Bitcoin mempool integration in Tycoon
- Full Kademlia recursive lookup in Swarm
- Ed25519 signing in Quantum Ledger
- `authorized_nodes[]` enforcement
- `genesis.iso` flash-drive installer image

See [Omega-Build Golden Master](OMEGA_BUILD.md) and [CHANGELOG](CHANGELOG.md).
