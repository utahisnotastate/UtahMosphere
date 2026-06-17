# Omni-Desk Sovereign App Store (v35.0)

The **Omni-Desk** is UtahMosphere's GPU-accelerated holographic desktop. In Time-3 we do not download apps from Apple, Google, or Microsoft — **we manifest them** via the Omni-Compiler and UtahClaw.

Five **Genesis Applications** ship pre-loaded. Each is an agentic ecosystem, not a static binary.

## Genesis Suite

| App ID | Name | Purpose |
|--------|------|---------|
| `web_forge` | **Omni-WebForge** | Drag a Word doc, GitHub repo, or speak — instant site on `UtahContainerEngine` |
| `zeo_canvas` | **ZEO-Canvas** | Local uncensored image generation on your hardware (sovereign SVG/latent pipeline) |
| `app_smith` | **Kinematic-AppSmith** | Sketch or describe a UI → native Ghost Tune / Utah-Flux client |
| `holo_notebook` | **Holographic-Notebook** | Drop PDFs/code/audio — autonomously builds transformation UIs (podcasts, tutorials) |
| `claw_harvester` | **UtahClaw-Harvester** | Crawl codebases, extract JWT/auth/payment logic → generalized MCP tools |

## Architecture

```
Omni-Desk UI (9092 /desk/ui)
       |
       v
+------------------+
| OmniDeskKernel   |  route_intent(app_id, payload)
+------------------+
   /    |     |    \
Web   ZEO   App   Holo   Harvester
Forge Canvas Smith Notebook → UtahClaw /harvest
       |
       v
MCPOmniCompiler + SovereignOmniCompiler + Kinematic Siphon
```

## Module (`omni_desk.py`)

| Method | Purpose |
|--------|---------|
| `route_intent(app_id, payload, kernel_ref)` | Dispatch Genesis app intent |
| `list_apps()` | Registry of five Genesis apps |
| `render_ui_html()` | Material-UI inspired dashboard HTML |
| `start_desk_service(kernel_ref)` | Fast-socket on port **9092** |

## HTTP API (kernel port 8999)

### GET /desk/apps

List Genesis Suite applications.

### GET /desk/status

Omni-Desk sessions, desk data directory, enforce flag.

### GET /desk/ui

Holographic desktop HTML (Genesis app cards).

### POST /desk/intent

```bash
curl -X POST http://127.0.0.1:8999/desk/intent \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "web_forge",
    "payload": {"source_type": "voice", "content": "Portfolio site for a photographer"}
  }'
```

**Harvester example:**

```bash
curl -X POST http://127.0.0.1:8999/desk/intent \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "claw_harvester",
    "payload": {"repo_path": "/path/to/open-source-payments-repo"}
  }'
```

## Direct fast-socket (port 9092)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` or `/ui` | GET | Desktop HTML |
| `/apps` | GET | Genesis registry |
| `/status` | GET | Desk stats |
| `/intent` | POST | Same as `/desk/intent` |

UtahClaw harvester also exposes `POST http://127.0.0.1:9090/harvest` with `{"path": "..."}`.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_OMNI_DESK_ENFORCE` | `1` | Start Omni-Desk on boot (`0` = dev) |
| `UTAH_OMNI_DESK_PORT` | `9092` | Holographic desktop port |
| `UTAH_CLAW_ENFORCE` | `1` | Required for Feature Harvester |
| `UTAH_OMNI_ENFORCE` | `1` | Required for WebForge / AppSmith / Notebook |

## Related

- [UtahClaw](UTAH_CLAW.md)
- [Omni-Compiler](OMNI_COMPILER.md)
- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [Kinematic Siphon](KINEMATIC_SIPHON.md)
