# Capability Matrix

UtahMosphere OS **v35.0 Omni-Desk** — sovereign holographic desktop, five Genesis agentic apps, full v34 Utah-Claw stack.

---

## HTTP API Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/health` | GET | **Implemented** | `build: omega-build-v35-omni-desk` |
| `/desk/apps` | GET | **Implemented** | Genesis Suite registry |
| `/desk/status` | GET | **Implemented** | Omni-Desk sessions + desk dir |
| `/desk/ui` | GET | **Implemented** | Holographic desktop HTML |
| `/desk/intent` | POST | **Implemented** | Route Genesis app intent |
| `/claw/void` | POST | **Implemented** | Dispatch UtahClaw research |
| `/claw/status` | GET | **Implemented** | Ambient runner + forged tools |
| `/chrono/status` | GET | **Implemented** | Chrono-State rewind stats |
| `/siphon/ghost-tune` | GET | **Implemented** | B-Web Ghost Tune binary |
| `/omni/compile` | POST | **Implemented** | Agentic intent compile |
| `/omni/glass` | GET | **Implemented** | Manifold + event log |
| Full v34 stack | * | **Implemented** | UtahClaw, Omni-Glass, witnesses, Lazarus |

---

## Core Subsystems

| Component | Status | What works today |
|-----------|--------|------------------|
| **Omni-Desk (`omni_desk.py`)** | **Implemented** | Five Genesis apps on port 9092 |
| **Feature Harvester** | **Implemented** | `POST /harvest` + `claw_harvester` app |
| **UtahClaw (`utahclaw/`)** | **Implemented** | Void research + codebase harvest |
| **Omni-Glass FluxRelay** | **Implemented** | SSE stream port 9091 |
| **Chrono-State** | **Implemented** | Live mutation rewind |
| **Kinematic Siphon** | **Implemented** | Ghost Tune GPU protocol |
| **Genesis ISO v35** | **Implemented** | `utah_genesis_v35.iso` |

---

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_OMNI_DESK_ENFORCE` | `1` | Omni-Desk holographic desktop |
| `UTAH_OMNI_DESK_PORT` | `9092` | Desk fast-socket |
| `UTAH_CLAW_ENFORCE` | `1` | UtahClaw + harvester |
| `UTAH_OMNI_ENFORCE` | `1` | WebForge / AppSmith / Notebook |

See [Omni-Desk](OMNI_DESK.md), [UtahClaw](UTAH_CLAW.md), [CHANGELOG](CHANGELOG.md).
