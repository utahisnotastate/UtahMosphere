# Matrisis Kapasidad

UtahMosphere OS **v25.1 Migration Ready** — implementation status gi Omega-Build.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Ma implement** | Liveness check + `build: golden-master-v25.1` |
| `/status` | GET | **Ma implement** | UI state, tenants, claim status, S3 root |
| `/command` | POST | **Ma implement** | Voice intent execution |
| `/app/unlock` | POST | **Ma implement** | Submit payment; ma return 202 pending settlement |
| `/app/{name}` | GET | **Ma implement** | Tycoon 402 gate + UtahX proxy gi container |
| `/app/{name}/{path}` | GET | **Ma implement** | Sub-path proxy gi container backend |
| `/s3/{bucket}/{key}` | GET | **Ma implement** | Object read (local NVMe) |
| `/s3/{bucket}/{key}` | PUT/POST | **Ma implement** | Object write; optional HMAC headers |
| `/s3/{bucket}/{prefix}*` | GET | **Ma implement** | List objects |
| `/lambda/{fn}/invoke` | POST | **Ma implement** | Serverless handler invoke |
| `/lambda/{fn}` | GET | **Ma implement** | GET invoke yan empty event |
| `/rds/write` | POST | **Ma implement** | Key-value write |
| `/rds/read/{key}` | GET | **Ma implement** | Key-value read |

---

## Core Subsystems

| Component | Status | Håfa mumuña på'go |
|-----------|--------|-------------------|
| **Golden Master (`utahmosphere_master.py`)** | **Ma implement** | Unified entry point |
| **Core (`utahmosphere_os.py`)** | **Ma implement** | Full HTTP multiplexer, registry, mesh |
| **UtahX Proxy (`utahx_proxy.py`)** | **Ma implement** | Live HTTP proxy gi container ports |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Ma implement** | Per-tenant HTTP servers gi 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Ma implement** | AST-validated handler mutation + OTA channel |
| **S3 Mesh (`utah_s3_mesh.py`)** | **Ma implement** | Local object storage + HMAC |
| **Lambda Engine (`utah_lambda_engine.py`)** | **Ma implement** | Handler invoke sin images |
| **RDS Ledger (`utah_rds_ledger.py`)** | **Ma implement** | JSON key-value ledger |
| **Quantum Ledger** | Ma implement | Biometric claim + verification |
| **Utah-Tycoon** | **Ma implement** | Mempool/electrum settlement (`tycoon_settlement.py`), `POST /app/unlock`, HTTP 402 gate |
| **UtahNetes Gossip** | **Ma implement** | AuthGuard-signed 5s multicast via `utah_mesh_engine.py` |
| **Global Swarm** | **Ma implement** | Deterministic DHT + signed ledger sync |
| **AuthGuard (`ledger_auth.py`)** | **Ma implement** | `authorized_nodes[]` enforcement para voice + mesh |
| **Genesis ISO (`mk_iso.sh`)** | **Ma implement** | UEFI/hybrid flash installer builder |
| **Utah-Flux UI** | Ma implement | Tkinter status dashboard |
| **Auto-Genesis (`genesis_deploy.py`)** | **Ma implement** | Multi-process orchestrator |
| **Bootstrap (`bootstrap.sh`)** | **Ma implement** | Bare-metal systemd install |

---

## Voice Commands

| Command Pattern | Status | Ehemplo |
|-----------------|--------|---------|
| Claim node | Ma implement | `"Claim node"` |
| Deploy application | Ma implement | `"deploy application my-app"` |
| Patch application | **Ma implement** | `"patch app my-app to add logging"` |
| Authorize node | **Ma implement** | `"authorize node <64-char-vibe-hash>"` |
| Status / grid | Ma implement | `"status grid"` |

---

## Deployment Options

| Method | Status | Platform |
|--------|--------|----------|
| `python3 utahmosphere_master.py` | **Ma recommend** | Todu |
| `python3 utahmosphere_os.py` | Ma implement | Todu |
| `python3 genesis_deploy.py` | Ma implement | Linux / dev |
| `sudo bash bootstrap.sh` | **Ma recommend prod** | Linux systemd |
| `sudo bash setup.sh` | Ma implement | Alias para bootstrap |
| `./mk_iso.sh` | **Ma implement** | Linux — ma build `utah_genesis_v25.iso` |
| `docker-compose up` | Optional | Legacy convenience ha' |

---

## Roadmap (remaining)

- Alpine/vmlinuz bundling gi Genesis ISO (boot menu på'go ma dokumenta manual install path)
- Nonce/timestamp anti-replay para voice commands
- `authorized_nodes` revocation UI

Para mas detalle: [Referensia API](API_REFERENCE.md) · [Cookbook Desarrollador](DEVELOPER_COOKBOOK.md)
