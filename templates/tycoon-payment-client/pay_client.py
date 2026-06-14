#!/usr/bin/env python3
"""Client for Utah-Tycoon HTTP 402 payment flow."""

import json
import time
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8999"


def access(app_name: str, client_id: str) -> tuple[int, dict]:
    req = urllib.request.Request(
        f"{BASE}/app/{app_name}",
        headers={"X-Client-ID": client_id},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def wait_for_unlock(app_name: str, client_id: str, timeout: int = 90) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        code, body = access(app_name, client_id)
        if code == 200:
            return body
        time.sleep(5)
    raise TimeoutError("Payment not settled in time")


if __name__ == "__main__":
    import sys
    app = sys.argv[1] if len(sys.argv) > 1 else "demo"
    client = sys.argv[2] if len(sys.argv) > 2 else "tycoon-client"
    code, body = access(app, client)
    print(f"HTTP {code}: {json.dumps(body)}")
    if code == 402:
        print("Waiting for settlement...")
        print(json.dumps(wait_for_unlock(app, client), indent=2))
