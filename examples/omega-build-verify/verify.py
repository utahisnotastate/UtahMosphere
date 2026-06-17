#!/usr/bin/env python3
"""End-to-end Omega-Build verification: S3, RDS, Lambda, container proxy."""

import json
import sys
import time
import socket
import urllib.request
import urllib.error

socket.setdefaulttimeout(15)
BASE = "http://127.0.0.1:8999"


def post(path, data):
    payload = json.dumps(data).encode()
    req = urllib.request.Request(
        f"{BASE}{path}", data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return r.status, json.loads(r.read())


def get(path, headers=None):
    req = urllib.request.Request(f"{BASE}{path}", headers=headers or {})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def main():
    print("=== UtahMosphere Omega-Build Verification ===")

    code, body = get("/health")
    print(f"Health: {code} {body.decode()[:120]}")
    if code != 200:
        sys.exit(1)

    # Deploy container
    code, data = post("/command", {
        "transcript": "deploy application omega-test",
        "acoustic_hash": "0" * 64,
    })
    print(f"Deploy: {data.get('response', '')[:80]}")

    # RDS
    post("/rds/write", {"key": "user:1", "value": {"name": "Alice"}})
    code, body = get("/rds/read/user:1")
    print(f"RDS: {code} {body.decode()[:80]}")

    # S3
    req = urllib.request.Request(
        f"{BASE}/s3/test-bucket/hello.txt",
        data=b"omega-build",
        method="PUT",
    )
    urllib.request.urlopen(req)
    code, body = get("/s3/test-bucket/hello.txt")
    print(f"S3: {code} {body[:20]}")

    # Lambda invoke
    code, data = post("/lambda/omega-test/invoke", {"name": "General 23"})
    print(f"Lambda: {data}")

    # Tycoon unlock (payment gate)
    code, body = post("/app/unlock", {"app": "omega-test"})
    msg = body.get("message", body) if isinstance(body, dict) else str(body)
    print(f"Unlock: {code} {str(msg)[:80]}")

    # Omni-Compiler health check
    code, data = post("/omni/compile", {
        "intent": "I need a live Python web server health check like AWS load balancer",
        "mcp": False,
    })
    print(f"Omni: {code} {str(data)[:100]}")

    # UtahClaw epistemic void
    code, data = post("/claw/void", {"concept": "Integrate with Stripe GraphQL API"})
    print(f"Claw: {code} {str(data)[:100]}")

    code, body = get("/siphon/ghost-tune")
    print(f"Siphon: {code} {len(body)} bytes")

    # Omni-Desk Genesis Suite
    code, body = get("/desk/apps")
    print(f"Desk apps: {code} {body.decode()[:100]}")
    code, data = post("/desk/intent", {
        "app_id": "zeo_canvas",
        "payload": {"prompt": "sovereign aurora over salt flats"},
    })
    print(f"Desk ZEO: {code} {str(data)[:100]}")

    print("=== Verification complete ===")


if __name__ == "__main__":
    main()
