# Capability Matrix

UtahMosphere OS **v30.0 DHT-Federated Attestation & Drift Healing** — sovereign trust swarm: DHT golden consensus, PCR drift detection, emergency quarantine.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | `build: omega-build-v30-federated-attested` + full attestation snapshot |
| `/attestation/quote` | GET | **Implemented** | RA-TLS TPM quote + `hardware_id` |
| `/registry/quotes` | GET | **Implemented** | Global hardware quote registry export |
| `/registry/purge` | POST | **Implemented** | Purge compromised hardware (root vibe) |
| `/dht/consensus` | GET | **Implemented** | DHT golden measurement ledger |
| `/dht/challenge` | POST | **Implemented** | Swarm attestation challenge to peer |
| `/nonce` | GET | **Implemented** | Voice command anti-replay nonce |
| `/status` | GET | **Implemented** | PCR drift, DHT federation, RA-TLS guard stats |
| `/command` | POST | **Implemented** | Voice + claim anchors golden PCR + DHT record |
| `/admin/revoke-node` | POST | **Implemented** | Root-only node revocation |
| `/app/unlock` | POST | **Implemented** | 4-region mempool failover settlement |
| `/app/{name}` | GET | **Implemented** | Tycoon 402 + UtahX proxy with RA-TLS ingress |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Implemented** | Full cloud parity |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **DHT Golden Registry (`dht_quote_registry.py`)** | **Implemented** | Swarm consensus verify, merge, quarantine |
| **PCR Drift Detector (`drift_detector.py`)** | **Implemented** | PCR0 monitor; `emergency_quarantine()` on drift |
| **Quote Registry (`quote_registry.py`)** | **Implemented** | Register, purge, merge hardware quotes |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Implemented** | CA pinning; UtahX ingress |
| **RA-TLS (`ra_tls_attest.py`)** | **Implemented** | DHT verify + TPM quotes on mesh gossip |
| **TPM Locker (`tpm_lock.py`)** | **Implemented** | Vibe-Print sealed to PCR0 |
| **Swarm DHT (`utah_swarm_protocol.py`)** | **Implemented** | Attestation challenge/response + quarantine notices |
| **UtahNetes + Swarm** | **Implemented** | RA-TLS + DHT golden sync + signed gossip |
| **Genesis ISO v30** | **Implemented** | `utah_genesis_v30.iso` |
| **Full cloud parity** | **Implemented** | S3, Lambda, RDS, UtahX, containers |

---

## Deployment

| Method | Status |
|--------|--------|
| `python3 utahmosphere_master.py` | **Recommended** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v30 ISO** |

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus on peer quotes |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR0 drift monitor + quarantine |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_PCR_DRIFT_INTERVAL_SEC` | `10` | Drift probe interval |

## Roadmap

All v29.0 roadmap items **implemented** in v30.0 (DHT federation, PCR drift detection).

Future: multi-region DHT quorum, automated Lazarus kernel rollback on drift.

See [DHT Federation](DHT_FEDERATION.md), [PCR Drift](PCR_DRIFT.md), [Quote Registry](QUOTE_REGISTRY.md), [CHANGELOG](CHANGELOG.md).
