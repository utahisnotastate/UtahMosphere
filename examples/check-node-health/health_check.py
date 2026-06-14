#!/usr/bin/env python3
"""Probe UtahMosphere /health and /status endpoints."""

import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8999"


def get(path: str) -> dict:
    with urllib.request.urlopen(f"{BASE}{path}") as resp:
        return json.loads(resp.read())


if __name__ == "__main__":
    try:
        health = get("/health")
        status = get("/status")
        print("Health:", json.dumps(health, indent=2))
        print("Status:", json.dumps(status, indent=2))
        if health.get("status") != "healthy":
            sys.exit(1)
    except Exception as e:
        print(f"FAIL: {e}")
        print("Is utahmosphere_os.py running on port 8999?")
        sys.exit(1)
