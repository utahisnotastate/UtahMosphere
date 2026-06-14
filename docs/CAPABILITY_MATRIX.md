# Capability Matrix

UtahMosphere OS **v29.0 Remote Attestation Infrastructure** — sovereign trust anchors: global hardware quote registry, RA-TLS CA pinning, biometric-to-TPM binding.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | `build: omega-build-v29-remote-attested` + full attestation snapshot |
| `/attestation/quote` | GET | **Implemented** | RA-TLS TPM quote + `hardware_id` |
| `/registry/quotes` | GET | **Implemented** | Global hardware quote registry export |
| `/registry/purge` | POST | **Implemented** | Purge compromised hardware (root vibe) |
| `/nonce` | GET | **Implemented** | Voice command anti-replay nonce |
| `/status` | GET | **Implemented** | TPM lock, RA-TLS guard, quote registry stats |
| `/command` | POST | **Implemented** | Voice + nonce + TPM-bound vibe + registry push on claim |
| `/admin/revoke-node` | POST | **Implemented** | Root-only node revocation |
| `/app/unlock` | POST | **Implemented** | 4-region mempool failover settlement |
| `/app/{name}` | GET | **Implemented** | Tycoon 402 + UtahX proxy with RA-TLS ingress |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Implemented** | Full cloud parity |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **Quote Registry (`quote_registry.py`)** | **Implemented** | Register, purge, merge, persist hardware quotes |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Implemented** | CA pinning; UtahX ingress; X.509 OID verify |
| **RA-TLS (`ra_tls_attest.py`)** | **Implemented** | TPM quote on mesh gossip; registry replication |
| **TPM Locker (`tpm_lock.py`)** | **Implemented** | Vibe-Print sealed to PCR0 via `tpm2_create` / `tpm2_unseal` |
| **Mempool Failover (`tycoon_failover.py`)** | **Implemented** | US / EU / global / **Oceania** 4-region failover |
| **Hardware Attestation (`attestation_guard.py`)** | **Implemented** | Bootstrap PCR0 gate |
| **Voice Bridge Signed** | **Implemented** | Auto nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Implemented** | Mesh + voice security |
| **UtahNetes + Swarm DHT** | **Implemented** | RA-TLS + signed gossip + registry merge |
| **Genesis ISO v29** | **Implemented** | `utah_genesis_v29.iso` |
| **Full cloud parity** | **Implemented** | S3, Lambda, RDS, UtahX, containers |

---

## Deployment

| Method | Status |
|--------|--------|
| `python3 utahmosphere_master.py` | **Recommended** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v29 ISO** |

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Require TPM seal on claim |
| `UTAH_RA_TLS_ENFORCE` | `1` | Require RA-TLS quotes on mesh |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_MEMPOOL_NODES` | 4 defaults | Override mempool failover list |

## Roadmap

All v28.0 roadmap items **implemented** in v29.0 (remote RA-TLS CA pinning, hardware quote registry).

Future: hardware quote DHT federation, automated PCR drift detection.

See [Quote Registry](QUOTE_REGISTRY.md), [Attestation](ATTESTATION.md), [RA-TLS](RA_TLS.md), [Genesis ISO](GENESIS_ISO.md), [CHANGELOG](CHANGELOG.md).
