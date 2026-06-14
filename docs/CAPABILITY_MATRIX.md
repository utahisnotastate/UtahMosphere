# Capability Matrix

UtahMosphere OS **v32.0 Lazarus Self-Healing** — multi-region quorum witnesses, entangled state-diff sync, Lazarus auto-restore.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | `build: omega-build-v32-lazarus-self-healing` |
| `/witness/status` | GET | **Implemented** | Multi-region witness quorum stats |
| `/lazarus/status` | GET | **Implemented** | Lazarus checkpoint + golden master |
| `/lazarus/restore` | POST | **Implemented** | Trigger clean-room auto-restore |
| `/quorum/consensus` | GET | **Implemented** | Majority-quorum vote ledger |
| `/dht/consensus` | GET | **Implemented** | Golden + quorum combined |
| `/dht/challenge` | POST | **Implemented** | Swarm attestation challenge |
| `/attestation/quote` | GET | **Implemented** | RA-TLS TPM quote |
| `/registry/quotes` | GET | **Implemented** | Hardware quote registry |
| `/command` | POST | **Implemented** | Voice + claim + Lazarus checkpoint |
| `/app/{name}` | GET | **Implemented** | Tycoon 402 + UtahX RA-TLS |
| Full cloud parity | * | **Implemented** | S3, Lambda, RDS, containers |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **Quorum Witnesses (`quorum_witness.py`)** | **Implemented** | US/EU/Oceania/Asia regional tie-breakers |
| **Lazarus Auto-Restore (`lazarus_restore.py`)** | **Implemented** | Golden Master + kexec atomic restore |
| **State-Diff Engine (`state_diff_engine.py`)** | **Implemented** | Entangled delta mesh sync (<1KB) |
| **Quorum Engine (`dht_consensus_engine.py`)** | **Implemented** | 51%+ federated vote consensus |
| **PCR Drift (`drift_detector.py`)** | **Implemented** | kexec rollback + Lazarus trigger |
| **Genesis ISO v32** | **Implemented** | `utah_genesis_v32.iso` |

---

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_WITNESS_ENFORCE` | `1` | Multi-region witness quorum |
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Auto-restore after quarantine |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec load/execute during Lazarus restore |
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Entangled delta mesh sync |
| `UTAH_QUORUM_ENFORCE` | `1` | Majority quorum on quotes |

## Roadmap

All v31.0 items **implemented** in v32.0 (witnesses, Lazarus restore, state-diff).

Future: multi-region quorum witnesses on dedicated hardware, Lazarus OTA channel.

See [Quorum Witnesses](QUORUM_WITNESSES.md), [Lazarus Restore](LAZARUS_RESTORE.md), [State-Diff](STATE_DIFF_ENGINE.md), [CHANGELOG](CHANGELOG.md).
