# Capability Matrix

UtahMosphere OS **v33.0 Omni-Mind** — agentic Omni-Compiler, MCP context bridge, sovereign UtahVidia inference.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | `build: omega-build-v33-omni-mind` |
| `/omni/compile` | POST | **Implemented** | Agentic intent → live deployment |
| `/omni/status` | GET | **Implemented** | Omni-Mind + Omni-Glass stats |
| `/omni/glass` | GET | **Implemented** | Real-time agentic event log |
| `/witness/status` | GET | **Implemented** | Multi-region witness quorum stats |
| `/lazarus/status` | GET | **Implemented** | Lazarus checkpoint + golden master |
| `/lazarus/restore` | POST | **Implemented** | Trigger clean-room auto-restore |
| `/quorum/consensus` | GET | **Implemented** | Majority-quorum vote ledger |
| `/command` | POST | **Implemented** | Voice + `compile` / `omni` intents |
| Full cloud parity | * | **Implemented** | S3, Lambda, RDS, containers |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **Omni-Compiler (`omni_compiler.py`)** | **Implemented** | Intent → blueprint → manifest |
| **MCP Bridge (`mcp_omni_bridge.py`)** | **Implemented** | Context-aware filesystem MCP |
| **Utah-Omni-Mind (`utah_omni_mind.py`)** | **Implemented** | Sovereign local inference |
| **UtahVidia (`utahvidia/`)** | **Implemented** | ZEO-Shield + Osmotic Router |
| **Omni-Glass (`omni_glass.py`)** | **Implemented** | Agentic action dashboard feed |
| **Quorum Witnesses (`quorum_witness.py`)** | **Implemented** | US/EU/Oceania/Asia tie-breakers |
| **Lazarus Auto-Restore (`lazarus_restore.py`)** | **Implemented** | Golden Master + kexec restore |
| **Genesis ISO v33** | **Implemented** | `utah_genesis_v33.iso` |

---

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_OMNI_ENFORCE` | `1` | Enable Omni-Compiler |
| `UTAH_OMNI_PROVIDER` | `sovereign` | `sovereign` or `openai` |
| `UTAH_OMNI_MCP_ENFORCE` | `1` | MCP context before compile |
| `UTAH_OMNI_EXEC_ENFORCE` | `1` | Run post-deploy scripts |
| `UTAH_WITNESS_ENFORCE` | `1` | Multi-region witness quorum |
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Auto-restore after quarantine |

## Roadmap

All v32.0 items **implemented** in v33.0 (Omni-Compiler, MCP, Omni-Mind).

Future: Omni-Glass holographic UI, dedicated MCP Postgres/GitHub servers.

See [Omni-Compiler](OMNI_COMPILER.md), [MCP Bridge](MCP_OMNI_BRIDGE.md), [Utah-Omni-Mind](UTAH_OMNI_MIND.md), [CHANGELOG](CHANGELOG.md).
