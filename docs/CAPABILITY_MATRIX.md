# Capability Matrix

UtahMosphere OS **v34.0 Utah-Claw** — ambient epistemic void resolver, Omni-Glass FluxRelay, Chrono-State rewind, Kinematic Siphon.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | `build: omega-build-v34-utah-claw` |
| `/claw/void` | POST | **Implemented** | Dispatch UtahClaw research |
| `/claw/status` | GET | **Implemented** | Ambient runner + forged tools |
| `/chrono/status` | GET | **Implemented** | Chrono-State rewind stats |
| `/siphon/ghost-tune` | GET | **Implemented** | B-Web Ghost Tune binary |
| `/omni/compile` | POST | **Implemented** | Agentic intent compile |
| `/omni/glass` | GET | **Implemented** | Manifold + event log |
| `/omni/status` | GET | **Implemented** | Omni-Mind stats |
| Full v33 stack | * | **Implemented** | Omni-Mind, witnesses, Lazarus |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **UtahClaw (`utahclaw/`)** | **Implemented** | Non-blocking void research + MCP forge |
| **Holographic Memory** | **Implemented** | Concept interference patterns |
| **Chrono-State (`chrono_state.py`)** | **Implemented** | Live mutation rewind |
| **Omni-Glass FluxRelay** | **Implemented** | SSE stream port 9091 |
| **Kinematic Siphon** | **Implemented** | Ghost Tune GPU protocol |
| **Omni-Compiler** | **Implemented** | Void-aware intent compilation |
| **Genesis ISO v34** | **Implemented** | `utah_genesis_v34.iso` |

---

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_CLAW_ENFORCE` | `1` | UtahClaw ambient runner |
| `UTAH_CLAW_PORT` | `9090` | UtahClaw fast-socket |
| `UTAH_CHRONO_ENFORCE` | `1` | Chrono-State rewind |
| `UTAH_OMNI_GLASS_STREAM` | `1` | Omni-Glass SSE relay |
| `UTAH_OMNI_ENFORCE` | `1` | Omni-Compiler |

See [UtahClaw](UTAH_CLAW.md), [Omni-Glass UI](OMNI_GLASS_UI.md), [CHANGELOG](CHANGELOG.md).
