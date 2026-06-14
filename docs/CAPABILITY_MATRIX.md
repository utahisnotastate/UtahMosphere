# Capability Matrix

UtahMosphere OS **v28.0 TPM-Hardened Attested** — sovereign trust chain complete.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | `build: omega-build-v28-attested` + full attestation snapshot |
| `/attestation/quote` | GET | **Implemented** | RA-TLS TPM quote for mesh peer verification |
| `/nonce` | GET | **Implemented** | Voice command anti-replay nonce |
| `/status` | GET | **Implemented** | TPM lock, RA-TLS, Oceania mempool regions |
| `/command` | POST | **Implemented** | Voice + nonce + TPM-bound vibe verification |
| `/admin/revoke-node` | POST | **Implemented** | Root-only node revocation |
| `/app/unlock` | POST | **Implemented** | 4-region mempool failover settlement |
| `/app/{name}` | GET | **Implemented** | Tycoon 402 + UtahX proxy |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Implemented** | Full cloud parity |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **TPM Locker (`tpm_lock.py`)** | **Implemented** | Vibe-Print sealed to PCR0 via `tpm2_create` / `tpm2_unseal` |
| **RA-TLS (`ra_tls_attest.py`)** | **Implemented** | TPM quote on mesh gossip; peer verification before sync |
| **Mempool Failover (`tycoon_failover.py`)** | **Implemented** | US / EU / global / **Oceania** 4-region failover |
| **Hardware Attestation (`attestation_guard.py`)** | **Implemented** | Bootstrap PCR0 gate |
| **Voice Bridge Signed** | **Implemented** | Auto nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Implemented** | Mesh + voice security |
| **UtahNetes + Swarm DHT** | **Implemented** | RA-TLS + signed gossip |
| **Genesis ISO v28** | **Implemented** | `utah_genesis_v28.iso` |
| **Full cloud parity** | **Implemented** | S3, Lambda, RDS, UtahX, containers |

---

## Deployment

| Method | Status |
|--------|--------|
| `python3 utahmosphere_master.py` | **Recommended** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v28 ISO** |

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Require TPM seal on claim |
| `UTAH_RA_TLS_ENFORCE` | `1` | Require RA-TLS quotes on mesh |
| `UTAH_MEMPOOL_NODES` | 4 defaults | Override mempool failover list |

## Roadmap

All v27.0 roadmap items **implemented** in v28.0.

Future: remote RA-TLS CA pinning, hardware quote registry service.

See [Attestation](ATTESTATION.md), [RA-TLS](RA_TLS.md), [Genesis ISO](GENESIS_ISO.md), [CHANGELOG](CHANGELOG.md).
