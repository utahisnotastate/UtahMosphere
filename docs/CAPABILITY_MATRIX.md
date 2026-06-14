# Capability Matrix

UtahMosphere OS **v25.1 Migration Ready** — implementation status as of Omega-Build.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | Liveness + `build: golden-master-v25.1` |
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
| **Utah-Tycoon** | **Implemented** | Mempool/electrum settlement (`tycoon_settlement.py`), `POST /app/unlock`, HTTP 402 gate |
| **UtahNetes Gossip** | **Implemented** | AuthGuard-signed 5s multicast via `utah_mesh_engine.py` |
| **Global Swarm** | **Implemented** | Deterministic DHT + signed ledger sync |
| **AuthGuard (`ledger_auth.py`)** | **Implemented** | `authorized_nodes[]` enforcement for voice + mesh |
| **Genesis ISO (`mk_iso.sh`)** | **Implemented** | UEFI/hybrid flash installer builder |
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
| Authorize node | **Implemented** | `"authorize node <64-char-vibe-hash>"` |
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
| `./mk_iso.sh` | **Implemented** | Linux — builds `utah_genesis_v25.iso` |
| `docker-compose up` | Optional | Legacy convenience only |

---

## Roadmap (Remaining)

- Alpine/vmlinuz bundling inside Genesis ISO (boot menu currently documents manual install path)
- Nonce/timestamp anti-replay for voice commands
- `authorized_nodes` revocation UI

See [Omega-Build Golden Master](OMEGA_BUILD.md), [Genesis ISO](GENESIS_ISO.md), [OTA Lazarus Channel](OTA_LAZARUS.md), and [CHANGELOG](CHANGELOG.md).
