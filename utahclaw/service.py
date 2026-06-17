#!/usr/bin/env python3
"""UtahClaw fast-socket HTTP service (port 9090) — void dispatch API."""

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Optional

CLAW_PORT = int(os.environ.get("UTAH_CLAW_PORT", "9090"))


def _start_claw_http_server(kernel_ref: Any = None):
    from utahclaw.ambient_runner import ambient_runner

    class ClawHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            return

        def _json(self, status: int, body: dict):
            payload = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_POST(self):
            if self.path != "/void":
                self.send_response(404)
                self.end_headers()
                return
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            data = json.loads(raw.decode("utf-8"))
            concept = data.get("concept", "")
            if not concept:
                self._json(400, {"error": "concept required"})
                return
            result = ambient_runner.dispatch_void(concept, kernel_ref)
            self._json(202, result)

        def do_GET(self):
            if self.path == "/health":
                self._json(200, {"status": "healthy", "service": "utah-claw"})
                return
            if self.path == "/status":
                self._json(200, ambient_runner.status())
                return
            self.send_response(404)
            self.end_headers()

    server = ThreadingHTTPServer(("", CLAW_PORT), ClawHandler)
    print(f"[UtahClaw] Fast-socket online at port {CLAW_PORT}")
    server.serve_forever()


def start_claw_service(kernel_ref: Any = None) -> Optional[threading.Thread]:
    if os.environ.get("UTAH_CLAW_ENFORCE", "1") == "0":
        return None
    thread = threading.Thread(
        target=_start_claw_http_server,
        args=(kernel_ref,),
        daemon=True,
        name="utah-claw-http",
    )
    thread.start()
    return thread
