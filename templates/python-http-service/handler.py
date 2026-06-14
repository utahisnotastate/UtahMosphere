#!/usr/bin/env python3
"""Standalone HTTP microservice template for UtahMosphere environments."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

PORT = int(os.environ.get("PORT", "8080"))


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = {"status": "ok"}
        else:
            body = {"status": "running", "environment": "UtahMosphere", "path": self.path}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    print(f"UtahMosphere service starting on port {PORT}...")
    HTTPServer(("", PORT), SimpleHandler).serve_forever()
