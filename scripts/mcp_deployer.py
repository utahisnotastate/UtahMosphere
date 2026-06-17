#!/usr/bin/env python3
"""
Utah-Deployer MCP — autonomous DevOps for Cursor Level 6.
Deploys to UtahContainerEngine via live kernel HTTP API.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from mcp.server.fastmcp import FastMCP

KERNEL_BASE = os.environ.get("UTAH_KERNEL_BASE", "http://127.0.0.1:8999").rstrip("/")
REPO_ROOT = Path(os.environ.get("UTAH_REPO_ROOT", Path(__file__).resolve().parents[1]))
VERIFY_SCRIPT = REPO_ROOT / "examples" / "omega-build-verify" / "verify.py"

mcp = FastMCP("Utah-Deployer")


def _http_json(method: str, path: str, body: dict | None = None, timeout: int = 120) -> dict:
    data = None
    headers = {"Content-Type": "application/json", "User-Agent": "utah-deployer-mcp/1.0"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{KERNEL_BASE}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            if path == "/desk/ui" or "text/html" in resp.headers.get("Content-Type", ""):
                return {"ok": True, "status": resp.status, "body_preview": raw[:500]}
            try:
                return json.loads(raw) if raw else {"ok": True, "status": resp.status}
            except json.JSONDecodeError:
                return {"ok": True, "status": resp.status, "body": raw}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(detail)
            parsed["http_status"] = exc.code
            return parsed
        except json.JSONDecodeError:
            return {"ok": False, "error": detail or str(exc), "http_status": exc.code}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@mcp.tool()
def kernel_health() -> str:
    """Check UtahMosphere kernel liveness and build version."""
    return json.dumps(_http_json("GET", "/health"), indent=2)


@mcp.tool()
def deploy_to_container_engine(app_name: str) -> str:
    """Subagent: Deploy (manifest) an application on UtahContainerEngine via kernel /command."""
    result = _http_json("POST", "/command", {
        "transcript": f"deploy application {app_name}",
        "acoustic_hash": "0" * 64,
    })
    return json.dumps({
        "app_name": app_name,
        "deploy_result": result,
        "message": f"[Deployer] Hot-swapping {app_name} into sovereign memory.",
    }, indent=2)


@mcp.tool()
def omni_compile(intent: str, use_mcp: bool = False) -> str:
    """Compile natural-language intent into a live deployment via Omni-Compiler."""
    result = _http_json("POST", "/omni/compile", {
        "intent": intent,
        "mcp": use_mcp,
    })
    return json.dumps(result, indent=2)


@mcp.tool()
def desk_intent(app_id: str, payload_json: str = "{}") -> str:
    """Route intent to Omni-Desk Genesis app (web_forge, zeo_canvas, app_smith, holo_notebook, claw_harvester)."""
    try:
        payload = json.loads(payload_json) if payload_json else {}
    except json.JSONDecodeError:
        payload = {"raw": payload_json}
    result = _http_json("POST", "/desk/intent", {
        "app_id": app_id,
        "payload": payload,
    })
    return json.dumps(result, indent=2)


@mcp.tool()
def run_verify() -> str:
    """Run examples/omega-build-verify/verify.py against the live kernel."""
    if not VERIFY_SCRIPT.is_file():
        return json.dumps({"ok": False, "error": f"verify script not found: {VERIFY_SCRIPT}"})
    proc = subprocess.run(
        [sys.executable, str(VERIFY_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=180,
    )
    return json.dumps({
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "stdout": proc.stdout[-8000:],
        "stderr": proc.stderr[-2000:],
    }, indent=2)


@mcp.tool()
def patch_app(app_name: str, intent: str) -> str:
    """Lazarus AST patch via kernel voice command."""
    result = _http_json("POST", "/command", {
        "transcript": f"patch app {app_name} to {intent}",
        "acoustic_hash": "0" * 64,
    })
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
