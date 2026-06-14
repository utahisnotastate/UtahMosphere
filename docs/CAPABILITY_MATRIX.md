# Capability Matrix

UtahMosphere OS **v27.0 Production Immutable** — sovereign trust anchors complete.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | Liveness + `build: omega-build-v27-production` + `attestation` |
| `/nonce` | GET | **Implemented** | Issue fresh voice command nonce (30s window) |
| `/status` | GET | **Implemented** | UI state, tenants, attestation, mempool failover stats |
| `/command` | POST | **Implemented** | Voice intent + auto nonce signing (`voice_bridge_signed.py`) |
| `/admin/revoke-node` | POST | **Implemented** | Root-only authorized node revocation |
| `/app/unlock` | POST | **Implemented** | Submit payment; mempool failover settlement |
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
| **Hardware Attestation (`attestation_guard.py`)** | **Implemented** | TPM 2.0 PCR0 gate in bootstrap + health |
| **Mempool Failover (`tycoon_failover.py`)** | **Implemented** | US/EU/ASIA mempool silent failover |
| **Voice Bridge Signed (`voice_bridge_signed.py`)** | **Implemented** | Auto `GET /nonce` + HMAC signing |
| **UtahX Proxy (`utahx_proxy.py`)** | **Implemented** | Live HTTP proxy to container ports |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Implemented** | Per-tenant HTTP servers on 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Implemented** | AST-validated handler mutation + OTA |
| **S3 / Lambda / RDS** | **Implemented** | Full cloud parity |
| **Quantum Ledger** | **Implemented** | Biometric claim + verification |
| **Utah-Tycoon** | **Implemented** | Failover mempool + electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Implemented** | `authorized_nodes[]` enforcement |
| **Nonce-Guard (`nonce_guard.py`)** | **Implemented** | 30s anti-replay for voice commands |
| **UtahNetes + Swarm DHT** | **Implemented** | Signed gossip + deterministic routing |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Implemented** | Alpine vmlinuz + TPM-aware bootstrap |
| **Utah-Flux Revocation UI** | **Implemented** | Admin panel in `flux_gui.py` |
| **Auto-Genesis / Bootstrap** | **Implemented** | systemd + attestation gate |

---

## Voice Commands

| Command pattern | Status | Example |
|-----------------|--------|---------|
| Claim node | Implemented | `"Claim node"` |
| Authorize node | Implemented | `"authorize node <64-char-vibe-hash>"` |
| Deploy application | Implemented | `"deploy application my-app"` |
| Patch application | Implemented | `"patch app my-app to add logging"` |
| Status / grid | Implemented | `"status grid"` |

**Voice Bridge v27.0** auto-fetches `GET /nonce` and signs every command. Manual clients use `voice_bridge_signed.get_signed_payload()`.

---

## Deployment Options

| Method | Status | Platform |
|--------|--------|----------|
| `python3 utahmosphere_master.py` | **Recommended** | All |
| `sudo bash bootstrap.sh` | **Recommended prod** | Linux + TPM (optional skip) |
| `python3 genesis_iso_builder.py` | **Implemented** | Builds `utah_genesis_v27.iso` |
| `./mk_iso.sh` | **Implemented** | Genesis ISO wrapper |
| `python3 voice_bridge.py` | **Implemented** | Auto-nonce signed voice client |

---

## Roadmap

All v26.0 and prior roadmap items are **implemented** in v27.0.

Future enhancements:

- TPM quote attestation remote verification (RA-TLS)
- Fourth mempool region (Oceania)
- Hardware-bound vibe-print binding to TPM PCR

See [Omega-Build](OMEGA_BUILD.md), [Attestation](ATTESTATION.md), [Genesis ISO](GENESIS_ISO.md), and [CHANGELOG](CHANGELOG.md).
