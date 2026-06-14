#!/usr/bin/env python3
"""Deploy an app to UtahMosphere via POST /command (no microphone required)."""

import json
import sys
import urllib.request

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8999
OPEN_MODE_HASH = "0" * 64


def deploy(app_name: str, host: str = DEFAULT_HOST, acoustic_hash: str = OPEN_MODE_HASH) -> dict:
    payload = json.dumps({
        "transcript": f"deploy application {app_name}",
        "acoustic_hash": acoustic_hash,
    }).encode()
    req = urllib.request.Request(
        f"http://{host}:{DEFAULT_PORT}/command",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy.py <app-name>")
        sys.exit(1)
    result = deploy(sys.argv[1])
    print(json.dumps(result, indent=2))
