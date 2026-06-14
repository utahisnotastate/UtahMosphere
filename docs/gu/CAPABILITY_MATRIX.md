# Matrisis Kapasidad

UtahMosphere OS **v27.0 Production Immutable** — kompleto na sovereign trust anchors.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Ma implement** | Liveness check + `build: omega-build-v27-production` + `attestation` |
| `/nonce` | GET | **Ma implement** | Ma issue fresh voice command nonce (30s window) |
| `/status` | GET | **Ma implement** | UI state, tenants, attestation, mempool failover stats |
| `/command` | POST | **Ma implement** | Voice intent + auto nonce signing (`voice_bridge_signed.py`) |
| `/admin/revoke-node` | POST | **Ma implement** | Root-only authorized node revocation |
| `/app/unlock` | POST | **Ma implement** | Submit payment; mempool failover settlement |
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
| **Hardware Attestation (`attestation_guard.py`)** | **Ma implement** | TPM 2.0 PCR0 gate gi bootstrap + health |
| **Mempool Failover (`tycoon_failover.py`)** | **Ma implement** | US/EU/ASIA mempool silent failover |
| **Voice Bridge Signed (`voice_bridge_signed.py`)** | **Ma implement** | Auto `GET /nonce` + HMAC signing |
| **UtahX Proxy (`utahx_proxy.py`)** | **Ma implement** | Live HTTP proxy gi container ports |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Ma implement** | Per-tenant HTTP servers gi 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Ma implement** | AST-validated handler mutation + OTA |
| **S3 / Lambda / RDS** | **Ma implement** | Full cloud parity |
| **Quantum Ledger** | **Ma implement** | Biometric claim + verification |
| **Utah-Tycoon** | **Ma implement** | Failover mempool + electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Ma implement** | `authorized_nodes[]` enforcement |
| **Nonce-Guard (`nonce_guard.py`)** | **Ma implement** | 30s anti-replay para voice commands |
| **UtahNetes + Swarm DHT** | **Ma implement** | Signed gossip + deterministic routing |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Ma implement** | Alpine vmlinuz + TPM-aware bootstrap |
| **Utah-Flux Revocation UI** | **Ma implement** | Admin panel gi `flux_gui.py` |
| **Auto-Genesis / Bootstrap** | **Ma implement** | systemd + attestation gate |

---

## Voice Commands

| Command Pattern | Status | Ehemplo |
|-----------------|--------|---------|
| Claim node | Ma implement | `"Claim node"` |
| Authorize node | Ma implement | `"authorize node <64-char-vibe-hash>"` |
| Deploy application | Ma implement | `"deploy application my-app"` |
| Patch application | Ma implement | `"patch app my-app to add logging"` |
| Status / grid | Ma implement | `"status grid"` |

**Voice Bridge v27.0** ma auto-fetch `GET /nonce` yan ma sign kada komando. Manual clients usa `voice_bridge_signed.get_signed_payload()`.

---

## Deployment Options

| Method | Status | Platform |
|--------|--------|----------|
| `python3 utahmosphere_master.py` | **Ma recommend** | Todu |
| `sudo bash bootstrap.sh` | **Ma recommend prod** | Linux + TPM (optional skip) |
| `python3 genesis_iso_builder.py` | **Ma implement** | Ma build `utah_genesis_v27.iso` |
| `./mk_iso.sh` | **Ma implement** | Genesis ISO wrapper |
| `python3 voice_bridge.py` | **Ma implement** | Auto-nonce signed voice client |

---

## Roadmap

Todu i v26.0 yan antes na roadmap items **ma implement** gi v27.0.

Mejoras futuru:

- TPM quote attestation remote verification (RA-TLS)
- Fourth mempool region (Oceania)
- Hardware-bound vibe-print binding gi TPM PCR

Para mas detalle: [Referensia API](API_REFERENCE.md) · [Cookbook Desarrollador](DEVELOPER_COOKBOOK.md)
