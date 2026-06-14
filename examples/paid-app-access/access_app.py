#!/usr/bin/env python3
"""Demonstrate Utah-Tycoon HTTP 402 payment gate and settlement."""

import json
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8999"


def access_app(app_name: str, client_id: str) -> tuple[int, dict]:
    req = urllib.request.Request(
        f"{BASE}/app/{app_name}",
        headers={"X-Client-ID": client_id},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python access_app.py <app-name> [client-id]")
        sys.exit(1)

    app = sys.argv[1]
    client = sys.argv[2] if len(sys.argv) > 2 else "demo-client"

    code, body = access_app(app, client)
    print(f"Attempt 1 — HTTP {code}")
    print(json.dumps(body, indent=2))

    if code == 402:
        print("\nWaiting for simulated settlement (~60s)...")
        for _ in range(18):
            time.sleep(5)
            code, body = access_app(app, client)
            if code == 200:
                print(f"\nUnlocked — HTTP {code}")
                print(json.dumps(body, indent=2))
                break
        else:
            print("Timeout waiting for payment settlement.")
            sys.exit(1)
