#!/usr/bin/env python3
"""Optional standalone runner — deploy handler.py to UtahMosphere for production."""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from handler import handler

class Adapter(BaseHTTPRequestHandler):
    def do_GET(self):
        result = handler({"path": self.path}, {})
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def log_message(self, *args):
        return

if __name__ == "__main__":
    print("Minimal API on http://127.0.0.1:8080")
    HTTPServer(("", 8080), Adapter).serve_forever()
