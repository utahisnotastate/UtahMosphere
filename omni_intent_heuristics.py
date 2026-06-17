#!/usr/bin/env python3
"""Heuristic intent → blueprint translation when no frontier API or weights are available."""

import re
from typing import Any, Dict


def slugify(text: str) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(words[:4]) or "omni-app"


def heuristic_blueprint(user_intent: str) -> Dict[str, Any]:
    """Translate common cloud-developer intents into executable blueprints."""
    intent = user_intent.lower()
    app_name = slugify(user_intent)

    if "redis" in intent and ("node" in intent or "backend" in intent):
        app_name = "omni-redis-node"
        return {
            "app_name": app_name,
            "files_to_write": [
                {
                    "path": "handler.py",
                    "content": (
                        "import json\nimport time\n\n"
                        "_CACHE = {}\n\n"
                        "def handler(event, context):\n"
                        "    op = event.get('op', 'get')\n"
                        "    key = event.get('key', 'default')\n"
                        "    if op == 'set':\n"
                        "        _CACHE[key] = event.get('value')\n"
                        "        return {'status': 'ok', 'backend': 'node', 'cache': 'redis-sim'}\n"
                        "    return {'status': 'ok', 'value': _CACHE.get(key), 'cache': 'redis-sim', 'ts': time.time()}\n"
                    ),
                },
                {
                    "path": "README.md",
                    "content": "# Omni-compiled HA Redis + Node backend (simulated edge cache)\n",
                },
            ],
            "post_deploy_script": "",
        }

    if "react" in intent or "live-updating" in intent or "live updating" in intent:
        app_name = "omni-react-live"
        return {
            "app_name": app_name,
            "files_to_write": [
                {
                    "path": "handler.py",
                    "content": (
                        "def handler(event, context):\n"
                        "    html = '''<!DOCTYPE html><html><head><title>Omni Live</title>"
                        "<script>setInterval(()=>fetch('/app/omni-react-live/').then(r=>r.json()).then(d=>"
                        "document.getElementById('s').textContent=JSON.stringify(d)),2000)</script>"
                        "</head><body><h1>Live Omni Site</h1><pre id='s'></pre></body></html>'''\n"
                        "    if event.get('accept_html'):\n"
                        "        return {'statusCode': 200, 'body': html, 'content_type': 'text/html'}\n"
                        "    return {'status': 'live', 'app': 'omni-react-live', 'tick': event}\n"
                    ),
                }
            ],
            "post_deploy_script": "",
        }

    if "health" in intent or "load balancer" in intent:
        app_name = "omni-health"
        return {
            "app_name": app_name,
            "files_to_write": [
                {
                    "path": "handler.py",
                    "content": (
                        "import json\nimport socket\nimport time\n\n"
                        "def handler(event, context):\n"
                        "    return {\n"
                        "        'status': 'healthy',\n"
                        "        'node': socket.gethostname(),\n"
                        "        'timestamp': time.time(),\n"
                        "        'check': 'omni-compiler-health',\n"
                        "    }\n"
                    ),
                }
            ],
            "post_deploy_script": "",
        }

    if "database" in intent or "column" in intent or "migration" in intent:
        app_name = "omni-db-migration"
        return {
            "app_name": app_name,
            "files_to_write": [
                {
                    "path": "handler.py",
                    "content": (
                        "def handler(event, context):\n"
                        "  return {'status': 'migration_ready', 'hint': 'Use MCP schema read before ALTER'}\n"
                    ),
                },
                {
                    "path": "migrations/001_add_column.py",
                    "content": (
                        "# MCP-informed migration stub\n"
                        "def upgrade(conn):\n"
                        "    conn.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS omni_meta JSON')\n"
                    ),
                },
            ],
            "post_deploy_script": "",
        }

    return {
        "app_name": app_name,
        "files_to_write": [
            {
                "path": "handler.py",
                "content": (
                    f"def handler(event, context):\n"
                    f"    return {{'status': 'active', 'intent': {user_intent!r}, 'event': event}}\n"
                ),
            }
        ],
        "post_deploy_script": "",
    }


def heuristic_blueprint_from_context(context_vector: str) -> Dict[str, Any]:
    """Extract user intent from Omni-Mind prompt envelope."""
    match = re.search(r"<\|user\|>\s*(.*?)\s*<\|assistant\|>", context_vector, re.DOTALL)
    user = match.group(1).strip() if match else context_vector
    # strip system noise
    if "The user says:" in user:
        user = user.split("The user says:", 1)[-1].strip()
    return heuristic_blueprint(user)
