# Capability Matrix

UtahMosphere OS **v26.0 Omega-Build FINAL** — full roadmap implementation.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | Liveness + `build: omega-build-v26-final` |
| `/nonce` | GET | **Implemented** | Issue fresh voice command nonce (30s window) |
| `/status` | GET | **Implemented** | UI state, tenants, claim status, S3 root |
| `/command` | POST | **Implemented** | Voice intent + nonce anti-replay when claimed |
| `/admin/revoke-node` | POST | **Implemented** | Root-only authorized node revocation |
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
| **Quantum Ledger** | **Implemented** | Biometric claim + verification |
| **Utah-Tycoon** | **Implemented** | Mempool/electrum settlement (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Implemented** | `authorized_nodes[]` enforcement for voice + mesh |
| **Nonce-Guard (`nonce_guard.py`)** | **Implemented** | 30s anti-replay for voice commands |
| **UtahNetes Gossip** | **Implemented** | AuthGuard-signed 5s multicast via `utah_mesh_engine.py` |
| **Global Swarm** | **Implemented** | Deterministic DHT + signed ledger sync |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Implemented** | Alpine vmlinuz/initramfs hybrid ISO |
| **Utah-Flux Revocation UI (`ui_revocation.py`)** | **Implemented** | Admin panel in `flux_gui.py` |
| **Utah-Flux UI** | **Implemented** | Tkinter status + revocation dashboard |
| **Auto-Genesis (`genesis_deploy.py`)** | **Implemented** | Multi-process orchestrator |
| **Bootstrap (`bootstrap.sh`)** | **Implemented** | Bare-metal systemd install |

---

## Voice Commands

| Command pattern | Status | Example |
|-----------------|--------|---------|
| Claim node | Implemented | `"Claim node"` |
| Authorize node | **Implemented** | `"authorize node <64-char-vibe-hash>"` |
| Deploy application | Implemented | `"deploy application my-app"` |
| Patch application | **Implemented** | `"patch app my-app to add logging"` |
| Status / grid | Implemented | `"status grid"` |

**After claim:** include `nonce` + `command_signature` from `GET /nonce` on every `/command` request.

---

## Deployment Options

| Method | Status | Platform |
|--------|--------|----------|
| `python3 utahmosphere_master.py` | **Recommended** | All |
| `python3 utahmosphere_os.py` | Implemented | All |
| `python3 genesis_deploy.py` | Implemented | Linux / dev |
| `sudo bash bootstrap.sh` | **Recommended prod** | Linux systemd |
| `sudo bash setup.sh` | Implemented | Alias to bootstrap |
| `python3 genesis_iso_builder.py` | **Implemented** | Linux — builds `utah_genesis_v26.iso` |
| `./mk_iso.sh` | **Implemented** | Wrapper for Genesis ISO builder |
| `docker-compose up` | Optional | Legacy convenience only |

---

## Roadmap

All v25.x roadmap items are **implemented** in v26.0. Future work:

- Hardware attestation for Genesis ISO autoinstall
- Multi-region mempool failover
- Voice bridge automatic nonce signing

See [Omega-Build Golden Master](OMEGA_BUILD.md), [Genesis ISO](GENESIS_ISO.md), [OTA Lazarus Channel](OTA_LAZARUS.md), and [CHANGELOG](CHANGELOG.md).
