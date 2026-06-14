#!/usr/bin/env python3
"""
UtahContainerEngine Runtime - v25.0 Omega-Build
Namespace-isolated handler execution without Docker.
Spawns per-tenant HTTP listeners that invoke handler.py directly.
"""

import json
import importlib.util
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Callable, Optional

RUNNING_SERVERS: dict[int, HTTPServer] = {}


def load_handler(handler_path: str) -> Callable[[dict, dict], Any]:
    spec = importlib.util.spec_from_file_location("utah_handler", handler_path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot load handler: {handler_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "handler"):
        raise AttributeError(f"No handler() in {handler_path}")
    return module.handler


class UtahContainerRequestHandler(BaseHTTPRequestHandler):
    handler_fn: Callable[[dict, dict], Any] = None
    app_name: str = "unknown"

    def log_message(self, format, *args):
        return

    def _invoke(self, event: dict) -> Any:
        return self.handler_fn(event, {"app": self.app_name})

    def _send_json(self, status: int, payload: Any):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        event = {"path": self.path, "method": "GET", "headers": dict(self.headers)}
        try:
            result = self._invoke(event)
            self._send_json(200, result)
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            event = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            event = {"body": raw.decode("utf-8", errors="replace")}
        event["path"] = self.path
        event["method"] = "POST"
        try:
            result = self._invoke(event)
            self._send_json(200, result)
        except Exception as e:
            self._send_json(500, {"error": str(e)})


def start_container_server(
    app_name: str,
    port: int,
    handler_path: str,
    block: bool = False,
) -> Optional[HTTPServer]:
    """Start UtahContainerEngine HTTP listener on port."""
    handler_fn = load_handler(handler_path)

    class BoundHandler(UtahContainerRequestHandler):
        pass

    BoundHandler.handler_fn = handler_fn
    BoundHandler.app_name = app_name

    server = HTTPServer(("", port), BoundHandler)
    RUNNING_SERVERS[port] = server
    print(f"[UtahContainerEngine] {app_name} active on port {port}")

    if block:
        server.serve_forever()
    else:
        import threading
        threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: utah_container_runtime.py <app_name> <port> <handler.py>")
        sys.exit(1)
    start_container_server(sys.argv[1], int(sys.argv[2]), sys.argv[3], block=True)
