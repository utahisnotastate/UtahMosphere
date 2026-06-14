# Matrisis Kapasidad

UtahMosphere OS **v28.0 TPM-Hardened Attested** — kompleto na sovereign trust chain.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Ma implement** | `build: omega-build-v28-attested` + kompleto na attestation snapshot |
| `/attestation/quote` | GET | **Ma implement** | RA-TLS TPM quote para mesh peer verification |
| `/nonce` | GET | **Ma implement** | Voice command anti-replay nonce |
| `/status` | GET | **Ma implement** | TPM lock, RA-TLS, Oceania mempool regions |
| `/command` | POST | **Ma implement** | Voice + nonce + TPM-bound vibe verification |
| `/admin/revoke-node` | POST | **Ma implement** | Root-only node revocation |
| `/app/unlock` | POST | **Ma implement** | 4-region mempool failover settlement |
| `/app/{name}` | GET | **Ma implement** | Tycoon 402 + UtahX proxy |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Ma implement** | Full cloud parity |

---

## Core Subsystems

| Component | Status | Håfa mumuña på'go |
|-----------|--------|-------------------|
| **TPM Locker (`tpm_lock.py`)** | **Ma implement** | Vibe-Print sealed gi PCR0 via `tpm2_create` / `tpm2_unseal` |
| **RA-TLS (`ra_tls_attest.py`)** | **Ma implement** | TPM quote gi mesh gossip; peer verification antes sync |
| **Mempool Failover (`tycoon_failover.py`)** | **Ma implement** | US / EU / global / **Oceania** 4-region failover |
| **Hardware Attestation (`attestation_guard.py`)** | **Ma implement** | Bootstrap PCR0 gate |
| **Voice Bridge Signed** | **Ma implement** | Auto nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Ma implement** | Mesh + voice security |
| **UtahNetes + Swarm DHT** | **Ma implement** | RA-TLS + signed gossip |
| **Genesis ISO v28** | **Ma implement** | `utah_genesis_v28.iso` |
| **Full cloud parity** | **Ma implement** | S3, Lambda, RDS, UtahX, containers |

---

## Deployment

| Method | Status |
|--------|--------|
| `python3 utahmosphere_master.py` | **Ma recommend** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v28 ISO** |

## Environment

| Variable | Default | Para håfa |
|----------|---------|-----------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Require TPM seal gi claim |
| `UTAH_RA_TLS_ENFORCE` | `1` | Require RA-TLS quotes gi mesh |
| `UTAH_MEMPOOL_NODES` | 4 defaults | Override mempool failover list |

## Roadmap

Todu i v27.0 roadmap items **ma implement** gi v28.0.

Futuru: remote RA-TLS CA pinning, hardware quote registry service.

Para mas detalle: [Referensia API](API_REFERENCE.md) · [Cookbook Desarrollador](DEVELOPER_COOKBOOK.md)
