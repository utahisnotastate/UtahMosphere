# Capability Matrix

UtahMosphere OS **v31.0 Federated Quorum & PCR-Drift-Healing** — majority-quorum DHT consensus, automated kexec rollback, sovereign trust swarm.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | `build: omega-build-v31-federated-quorum` + full attestation snapshot |
| `/quorum/consensus` | GET | **Implemented** | Majority-quorum vote ledger |
| `/dht/consensus` | GET | **Implemented** | Golden + quorum combined export |
| `/dht/challenge` | POST | **Implemented** | Swarm attestation challenge |
| `/attestation/quote` | GET | **Implemented** | RA-TLS TPM quote + `hardware_id` |
| `/registry/quotes` | GET | **Implemented** | Hardware quote registry |
| `/registry/purge` | POST | **Implemented** | Purge compromised hardware |
| `/nonce` | GET | **Implemented** | Voice anti-replay nonce |
| `/status` | GET | **Implemented** | Quorum, PCR drift, RA-TLS stats |
| `/command` | POST | **Implemented** | Claim anchors quorum + golden PCR |
| `/admin/revoke-node` | POST | **Implemented** | Root-only revocation |
| `/app/unlock` | POST | **Implemented** | 4-region mempool failover |
| `/app/{name}` | GET | **Implemented** | Tycoon 402 + UtahX RA-TLS ingress |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Implemented** | Full cloud parity |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **Quorum Engine (`dht_consensus_engine.py`)** | **Implemented** | 51%+ vote tally; `verify_against_quorum()` |
| **PCR Drift (`drift_detector.py`)** | **Implemented** | PCR0 monitor; kexec `perform_rollback()` |
| **DHT Golden Registry (`dht_quote_registry.py`)** | **Implemented** | Golden measurement ledger |
| **Quote Registry (`quote_registry.py`)** | **Implemented** | Hardware quote register/purge |
| **RA-TLS Guard + Attest** | **Implemented** | Quorum verify on mesh gossip |
| **Swarm DHT** | **Implemented** | Challenge/response + quarantine notices |
| **Genesis ISO v31** | **Implemented** | `utah_genesis_v31.iso` |
| **Full cloud parity** | **Implemented** | S3, Lambda, RDS, UtahX, containers |

---

## Deployment

| Method | Status |
|--------|--------|
| `python3 utahmosphere_master.py` | **Recommended** |
| `sudo bash bootstrap.sh` | **Prod** |
| `python3 genesis_iso_builder.py` | **v31 ISO** |

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_QUORUM_ENFORCE` | `1` | Majority quorum on peer quotes |
| `UTAH_QUORUM_THRESHOLD` | `0.51` | Consensus ratio |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback on drift |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR0 drift monitor |

## Roadmap

All v30.0 items **implemented** in v31.0 (federated quorum, kexec rollback).

Future: multi-region quorum witnesses, Lazarus kernel auto-restore.

See [Quorum Consensus](QUORUM_CONSENSUS.md), [PCR Drift](PCR_DRIFT.md), [CHANGELOG](CHANGELOG.md).
