#!/usr/bin/env python3
"""Omni-Glass SSE stream server — real-time manifold broadcast."""

import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from omni_glass import omni_glass

STREAM_PORT = int(os.environ.get("UTAH_OMNI_GLASS_PORT", "9091"))


def _start_glass_stream_server():
    class GlassStreamHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            return

        def do_GET(self):
            if self.path.startswith("/stream"):
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.end_headers()
                sub = omni_glass.subscribe()
                try:
                    while True:
                        try:
                            payload = sub.get(timeout=15)
                        except Exception:
                            payload = json.dumps(omni_glass.export_manifold())
                        self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                        self.wfile.flush()
                finally:
                    omni_glass.unsubscribe(sub)
                return
            if self.path == "/manifold":
                body = json.dumps(omni_glass.export_manifold()).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            self.send_response(404)
            self.end_headers()

    server = ThreadingHTTPServer(("", STREAM_PORT), GlassStreamHandler)
    print(f"[Omni-Glass] FluxRelay stream online at port {STREAM_PORT}")
    server.serve_forever()


def start_glass_stream_service() -> threading.Thread | None:
    if os.environ.get("UTAH_OMNI_GLASS_STREAM", "1") == "0":
        return None
    thread = threading.Thread(target=_start_glass_stream_server, daemon=True, name="omni-glass-stream")
    thread.start()
    return thread
