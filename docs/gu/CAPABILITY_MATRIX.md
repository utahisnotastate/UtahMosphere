# Matrisis Kapasidad

UtahMosphere OS **v34.0 Utah-Claw** — kompleto na sovereign trust chain.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Ma implement** | `build: omega-build-v34-utah-claw` + kompleto na attestation snapshot |
| `/attestation/quote` | GET | **Ma implement** | RA-TLS TPM quote para mesh peer verification |
| `/registry/quotes` | GET | **Ma implement** | Global hardware quote registry |
| `/registry/purge` | POST | **Ma implement** | Purge compromised hardware |
| `/claw/void` | POST | **Implemented** | Epistemic void dispatch |
| `/claw/status` | GET | **Implemented** | UtahClaw runner stats |
| `/chrono/status` | GET | **Implemented** | Chrono-State status |
| `/siphon/ghost-tune` | GET | **Implemented** | Ghost Tune binary |
| `/omni/compile` | POST | **Implemented** | Agentic intent compile |
| `/omni/status` | GET | **Implemented** | Omni-Mind stats |
| `/omni/glass` | GET | **Implemented** | Agentic event log |
| `/witness/status` | GET | **Implemented** | Multi-region witnesses |
| `/lazarus/status` | GET | **Implemented** | Lazarus checkpoint |
| `/lazarus/restore` | POST | **Implemented** | Golden Master restore |
| `/quorum/consensus` | GET | **Ma implement** | Majority-quorum ledger |
| `/dht/consensus` | GET | **Ma implement** | DHT golden ledger |
| `/dht/challenge` | POST | **Ma implement** | Swarm attestation challenge |
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
| **Omni-Compiler (`omni_compiler.py`)** | **Implemented** | Intent → deployment |
| **MCP Bridge (`mcp_omni_bridge.py`)** | **Implemented** | Context-aware MCP |
| **Utah-Omni-Mind (`utah_omni_mind.py`)** | **Implemented** | Sovereign inference |
| **Quorum Witnesses (`quorum_witness.py`)** | **Implemented** | US/EU/Oceania tie-breakers |
| **Lazarus Restore (`lazarus_restore.py`)** | **Implemented** | Auto-restore after quarantine |
| **State-Diff (`state_diff_engine.py`)** | **Implemented** | Entangled mesh deltas |
| **Quorum Engine (`dht_consensus_engine.py`)** | **Implemented** | 51%+ vote consensus |
| **DHT Golden Registry (`dht_quote_registry.py`)** | **Implemented** | Swarm consensus verify |
| **PCR Drift (`drift_detector.py`)** | **Implemented** | Auto-quarantine on drift |
| **Quote Registry (`quote_registry.py`)** | **Implemented** | Register, purge, merge hardware quotes |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Implemented** | CA pinning; UtahX ingress |
| **RA-TLS (`ra_tls_attest.py`)** | **Ma implement** | TPM quote gi mesh gossip; peer verification antes sync |
| **Mempool Failover (`tycoon_failover.py`)** | **Ma implement** | US / EU / global / **Oceania** 4-region failover |
| **Hardware Attestation (`attestation_guard.py`)** | **Ma implement** | Bootstrap PCR0 gate |
| **Voice Bridge Signed** | **Ma implement** | Auto nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Ma implement** | Mesh + voice security |
| **UtahNetes + Swarm DHT** | **Ma implement** | RA-TLS + signed gossip |
| **Genesis ISO v33** | **Ma implement** | `utah_genesis_v34.iso` |
| **Full cloud parity** | **Ma implement** | S3, Lambda, RDS, UtahX, containers |

---

## Deployment

| Method | Status |
|--------|--------|
| `python3 utahmosphere_master.py` | **Ma recommend** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v32 ISO** |

## Environment

| Variable | Default | Para håfa |
|----------|---------|-----------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Require TPM seal gi claim |
| `UTAH_QUORUM_ENFORCE` | `1` | Majority quorum |
| `UTAH_WITNESS_ENFORCE` | `1` | Multi-region witnesses |
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Auto-restore |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec Lazarus restore |
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Entangled delta sync |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | Require RA-TLS quotes gi mesh |
| `UTAH_MEMPOOL_NODES` | 4 defaults | Override mempool failover list |

## Roadmap

Todu i v28.0 roadmap items **ma implement** gi v34.0.

Futuru: remote RA-TLS CA pinning, hardware quote registry service.

Para mas detalle: [Referensia API](API_REFERENCE.md) · [Cookbook Desarrollador](DEVELOPER_COOKBOOK.md)
