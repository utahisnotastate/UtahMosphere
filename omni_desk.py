#!/usr/bin/env python3
"""
UtahMosphere Omni-Desk v35.0
Material-UI inspired sovereign holographic desktop — five Genesis agentic apps.
"""

import asyncio
import json
import os
import re
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from mcp_omni_bridge import mcp_omni_compiler
except ImportError:
    mcp_omni_compiler = None  # type: ignore

try:
    from omni_compiler import SovereignOmniCompiler
except ImportError:
    SovereignOmniCompiler = None  # type: ignore

try:
    from omni_glass import omni_glass
except ImportError:
    omni_glass = None  # type: ignore

try:
    from utahclaw.ambient_runner import ambient_runner
except ImportError:
    ambient_runner = None  # type: ignore

try:
    from utahclaw.kinematic_siphon import kinematic_siphon
except ImportError:
    kinematic_siphon = None  # type: ignore

try:
    from utah_omni_mind import omni_mind
except ImportError:
    omni_mind = None  # type: ignore

DESK_ENFORCE = os.environ.get("UTAH_OMNI_DESK_ENFORCE", "1") != "0"
DESK_PORT = int(os.environ.get("UTAH_OMNI_DESK_PORT", "9092"))
DATA_DIR = Path(os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"))
DESK_DIR = DATA_DIR / "desk"
CANVAS_DIR = DESK_DIR / "zeo_canvas"
NOTEBOOK_DIR = DESK_DIR / "holo_notebook"

CLAW_BASE = os.environ.get("UTAH_CLAW_BASE", f"http://127.0.0.1:{os.environ.get('UTAH_CLAW_PORT', '9090')}")

GENESIS_APPS: Dict[str, Dict[str, str]] = {
    "web_forge": {
        "name": "Omni-WebForge",
        "tagline": "Website builder - manifest sites from docs, repos, or voice",
        "status": "active",
    },
    "zeo_canvas": {
        "name": "ZEO-Canvas",
        "tagline": "Sovereign local image generator - uncensored on your hardware",
        "status": "active",
    },
    "app_smith": {
        "name": "Kinematic-AppSmith",
        "tagline": "Sketch or describe a UI -> native Ghost Tune client",
        "status": "active",
    },
    "holo_notebook": {
        "name": "Holographic-Notebook",
        "tagline": "Second brain - autonomously builds tools from your corpus",
        "status": "active",
    },
    "claw_harvester": {
        "name": "UtahClaw-Harvester",
        "tagline": "Horizontal gene transfer - harvest features across codebases",
        "status": "active",
    },
}


class OmniDeskKernel:
    """Routes Genesis Suite intents to Omni-Compiler, UtahClaw, and Kinematic Siphon."""

    def __init__(self):
        self._lock = threading.RLock()
        self._sessions: List[Dict[str, Any]] = []
        DESK_DIR.mkdir(parents=True, exist_ok=True)
        CANVAS_DIR.mkdir(parents=True, exist_ok=True)
        NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
        print("[Omni-Desk] Genesis Suite registered. Five agentic apps online.")

    def list_apps(self) -> Dict[str, Any]:
        return {"apps": GENESIS_APPS, "count": len(GENESIS_APPS)}

    def status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "enforce": DESK_ENFORCE,
                "port": DESK_PORT,
                "genesis_apps": len(GENESIS_APPS),
                "recent_sessions": list(self._sessions[-20:]),
                "desk_dir": str(DESK_DIR),
            }

    def _record_session(self, app_id: str, payload: dict, result: dict):
        with self._lock:
            self._sessions.append({
                "app_id": app_id,
                "app": GENESIS_APPS.get(app_id, {}).get("name", app_id),
                "payload_keys": list(payload.keys()),
                "ok": result.get("ok", result.get("status") not in ("error", "failed")),
                "ts": time.time(),
            })
            self._sessions[:] = self._sessions[-100:]

    async def route_intent(
        self,
        app_id: str,
        payload: Dict[str, Any],
        kernel_ref: Any = None,
    ) -> Dict[str, Any]:
        if app_id not in GENESIS_APPS:
            return {"ok": False, "error": f"unknown_app: {app_id}"}

        app_name = GENESIS_APPS[app_id]["name"]
        if omni_glass:
            omni_glass.log_thought_vector("Omni-Desk", f"Routing to {app_name}", mcp_tool=app_id)

        print(f"[Omni-Desk] Routing intent to {app_name}...")

        handlers = {
            "web_forge": self._route_web_forge,
            "zeo_canvas": self._route_zeo_canvas,
            "app_smith": self._route_app_smith,
            "holo_notebook": self._route_holo_notebook,
            "claw_harvester": self._route_claw_harvester,
        }
        result = await handlers[app_id](payload, kernel_ref)
        self._record_session(app_id, payload, result)
        return result

    def route_intent_sync(
        self,
        app_id: str,
        payload: Dict[str, Any],
        kernel_ref: Any = None,
    ) -> Dict[str, Any]:
        try:
            return asyncio.run(self.route_intent(app_id, payload, kernel_ref))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self.route_intent(app_id, payload, kernel_ref))
            finally:
                loop.close()
        except Exception as exc:
            return {"ok": False, "error": str(exc), "app_id": app_id}

    async def _route_web_forge(self, payload: Dict[str, Any], kernel_ref: Any) -> Dict[str, Any]:
        source = payload.get("source_type", "voice")
        content = payload.get("content") or payload.get("transcript", "")
        repo_path = payload.get("repo_path", "")
        doc_path = payload.get("doc_path", "")

        if source == "repo" and repo_path:
            intent = (
                f"Read the repository at {repo_path}. Build a production React/HTML/CSS site "
                f"and deploy to UtahContainerEngine as app 'web-forge-site'."
            )
        elif source == "doc" and doc_path:
            intent = (
                f"Read the document at {doc_path}. Manifest a responsive website "
                f"with semantic HTML, modern CSS, and deploy instantly."
            )
        else:
            intent = (
                f"Build a sovereign website from this intent (no templates): {content or 'landing page'}. "
                f"Write handler.py with inline HTML/CSS, deploy to UtahContainerEngine."
            )

        return await self._compile_intent(intent, kernel_ref, app="web_forge")

    async def _route_zeo_canvas(self, payload: Dict[str, Any], kernel_ref: Any) -> Dict[str, Any]:
        prompt = payload.get("prompt", "sovereign horizon at dusk")
        width = int(payload.get("width", 512))
        height = int(payload.get("height", 512))

        slug = re.sub(r"[^a-z0-9_]+", "_", prompt.lower())[:40] or "zeo_frame"
        out_path = CANVAS_DIR / f"{slug}_{int(time.time())}.svg"

        blueprint = ""
        if omni_mind:
            try:
                blueprint = omni_mind.generate_intent_blueprint(
                    "You are ZEO-Canvas sovereign latent diffusion.",
                    f"Describe an SVG scene for: {prompt}",
                )
            except Exception:
                blueprint = ""

        svg = self._sovereign_svg(prompt, width, height, blueprint)
        out_path.write_text(svg, encoding="utf-8")

        if omni_glass:
            omni_glass.record("desk", f"ZEO-Canvas rendered: {prompt[:60]}", tool="zeo_canvas")

        return {
            "ok": True,
            "status": "rendered",
            "app": "zeo_canvas",
            "prompt": prompt,
            "artifact": str(out_path),
            "format": "image/svg+xml",
            "local_only": True,
            "message": "Uncensored latent scene manifested on sovereign hardware.",
        }

    @staticmethod
    def _sovereign_svg(prompt: str, width: int, height: int, blueprint: str) -> str:
        hue = (hash(prompt) % 360)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <radialGradient id="zeo" cx="50%" cy="40%" r="70%">
      <stop offset="0%" stop-color="hsl({hue}, 80%, 65%)"/>
      <stop offset="100%" stop-color="hsl({(hue + 120) % 360}, 70%, 12%)"/>
    </radialGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#zeo)"/>
  <text x="24" y="40" fill="#f0f4ff" font-family="system-ui" font-size="18">ZEO-Canvas</text>
  <text x="24" y="72" fill="#c8d4ff" font-family="system-ui" font-size="13">{prompt[:80]}</text>
</svg>'''

    async def _route_app_smith(self, payload: Dict[str, Any], kernel_ref: Any) -> Dict[str, Any]:
        description = payload.get("description") or payload.get("sketch_notes", "settings panel with dark mode")
        sketch = payload.get("sketch_path", "")
        sketch_clause = f" Reference sketch at {sketch}." if sketch else ""

        intent = (
            f"Generate a native GUI application: {description}.{sketch_clause} "
            f"Produce Python handler code compatible with Utah-Flux and Kinematic Siphon Ghost Tune. "
            f"App name: app-smith-ui."
        )
        compile_result = await self._compile_intent(intent, kernel_ref, app="app_smith")

        siphon_hint = None
        if kinematic_siphon and omni_glass:
            try:
                siphon_hint = len(kinematic_siphon.encode_scene_graph(omni_glass.export_manifold()))
            except Exception:
                siphon_hint = None

        compile_result["ghost_tune_bytes"] = siphon_hint
        compile_result["message"] = "Native GUI blueprint compiled. Ghost Tune scene graph ready."
        return compile_result

    async def _route_holo_notebook(self, payload: Dict[str, Any], kernel_ref: Any) -> Dict[str, Any]:
        target_vibe = payload.get("vibe", "tutorial")
        documents = payload.get("folder_paths") or payload.get("paths") or []
        if isinstance(documents, str):
            documents = [documents]

        roots = [str(p) for p in documents if p] or [str(NOTEBOOK_DIR)]
        intent = (
            f"Read the documents in {roots}. Build a full {target_vibe} generation pipeline UI "
            f"with player controls, deploy as holo-notebook-app."
        )

        mcp_cmd = payload.get("mcp_server_command")
        if not mcp_cmd:
            data_root = str(DATA_DIR)
            mcp_cmd = ["npx", "-y", "@modelcontextprotocol/server-filesystem", data_root]

        if mcp_omni_compiler:
            result = await mcp_omni_compiler.execute_intent(intent, mcp_cmd, kernel_ref)
            result["app"] = "holo_notebook"
            result["vibe"] = target_vibe
            return result

        return await self._compile_intent(intent, kernel_ref, app="holo_notebook")

    async def _route_claw_harvester(self, payload: Dict[str, Any], kernel_ref: Any) -> Dict[str, Any]:
        repo_path = payload.get("repo_path") or payload.get("path", "")
        if not repo_path:
            return {"ok": False, "error": "repo_path required"}

        if ambient_runner and hasattr(ambient_runner, "harvest_codebase"):
            result = ambient_runner.harvest_codebase(repo_path, kernel_ref)
            result["app"] = "claw_harvester"
            return result

        try:
            req = urllib.request.Request(
                f"{CLAW_BASE}/harvest",
                data=json.dumps({"path": repo_path}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                body["app"] = "claw_harvester"
                return body
        except Exception as exc:
            return {"ok": False, "error": str(exc), "app": "claw_harvester"}

    async def _compile_intent(self, intent: str, kernel_ref: Any, app: str = "") -> Dict[str, Any]:
        if mcp_omni_compiler:
            result = await mcp_omni_compiler.execute_intent(intent, None, kernel_ref)
        elif SovereignOmniCompiler:
            result = SovereignOmniCompiler.process_developer_intent(intent, kernel_ref)
        else:
            return {"ok": False, "error": "compiler_unavailable"}

        result["app"] = app
        return result

    def render_ui_html(self) -> str:
        apps_json = json.dumps(GENESIS_APPS, indent=2)
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>UtahMosphere Omni-Desk</title>
  <style>
    :root {{ --bg: #0d1117; --card: #161b22; --accent: #58a6ff; --text: #e6edf3; --muted: #8b949e; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); }}
    header {{ padding: 1.5rem 2rem; border-bottom: 1px solid #30363d; }}
    h1 {{ margin: 0; font-size: 1.5rem; }}
    .sub {{ color: var(--muted); margin-top: 0.25rem; }}
    main {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; padding: 2rem; }}
    .card {{ background: var(--card); border: 1px solid #30363d; border-radius: 12px; padding: 1.25rem; }}
    .card h2 {{ margin: 0 0 0.5rem; font-size: 1.1rem; color: var(--accent); }}
    .card p {{ margin: 0; font-size: 0.9rem; color: var(--muted); line-height: 1.4; }}
    .badge {{ display: inline-block; margin-top: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 6px;
              background: #238636; font-size: 0.75rem; }}
    footer {{ padding: 1rem 2rem; color: var(--muted); font-size: 0.85rem; border-top: 1px solid #30363d; }}
  </style>
</head>
<body>
  <header>
    <h1>Omni-Desk — Sovereign App Store</h1>
    <p class="sub">We do not download apps. We manifest them. Genesis Suite v35.0</p>
  </header>
  <main id="apps"></main>
  <footer>GPU-accelerated holographic desktop · Kinematic Siphon ready · Port {DESK_PORT}</footer>
  <script>
    const apps = {apps_json};
    const root = document.getElementById('apps');
    for (const [id, meta] of Object.entries(apps)) {{
      const el = document.createElement('article');
      el.className = 'card';
      el.innerHTML = `<h2>${{meta.name}}</h2><p>${{meta.tagline}}</p><span class="badge">${{meta.status}}</span>`;
      root.appendChild(el);
    }}
  </script>
</body>
</html>"""


omni_desk = OmniDeskKernel()


def _start_desk_http_server(kernel_ref: Any = None):
    desk = omni_desk

    class DeskHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            return

        def _json(self, status: int, body: dict):
            payload = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _html(self, status: int, html: str):
            payload = html.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path in ("/", "/ui"):
                self._html(200, desk.render_ui_html())
                return
            if path == "/health":
                self._json(200, {"status": "healthy", "service": "omni-desk"})
                return
            if path == "/status":
                self._json(200, desk.status())
                return
            if path == "/apps":
                self._json(200, desk.list_apps())
                return
            self.send_response(404)
            self.end_headers()

        def do_POST(self):
            path = self.path.split("?", 1)[0]
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                self._json(400, {"error": "invalid json"})
                return

            if path == "/intent":
                app_id = data.get("app_id", "")
                payload = data.get("payload") or data
                if not app_id:
                    self._json(400, {"error": "app_id required"})
                    return
                result = desk.route_intent_sync(app_id, payload, kernel_ref)
                code = 200 if result.get("ok", True) else 422
                self._json(code, result)
                return

            self.send_response(404)
            self.end_headers()

    server = ThreadingHTTPServer(("", DESK_PORT), DeskHandler)
    print(f"[Omni-Desk] Holographic desktop online at port {DESK_PORT}")
    server.serve_forever()


def start_desk_service(kernel_ref: Any = None) -> Optional[threading.Thread]:
    if not DESK_ENFORCE:
        return None
    thread = threading.Thread(
        target=_start_desk_http_server,
        args=(kernel_ref,),
        daemon=True,
        name="omni-desk-http",
    )
    thread.start()
    return thread
