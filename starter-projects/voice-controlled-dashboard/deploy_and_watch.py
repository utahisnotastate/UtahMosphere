#!/usr/bin/env python3
"""Send deploy commands while watching dashboard status."""

import json
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8999"


def command(transcript: str):
    payload = json.dumps({"transcript": transcript, "acoustic_hash": "0" * 64}).encode()
    req = urllib.request.Request(
        f"{BASE}/command", data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def status():
    with urllib.request.urlopen(f"{BASE}/status") as resp:
        return json.loads(resp.read())


if __name__ == "__main__":
    app = sys.argv[1] if len(sys.argv) > 1 else "dashboard-demo"
    print(command(f"deploy application {app}"))
    for _ in range(3):
        time.sleep(2)
        print(json.dumps(status(), indent=2))
