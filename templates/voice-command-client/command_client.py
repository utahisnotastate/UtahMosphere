#!/usr/bin/env python3
"""Programmatic client for POST /command."""

import json
import sys
import urllib.request

HOST = "127.0.0.1"
PORT = 8999


def send_command(transcript: str, acoustic_hash: str = "0" * 64) -> dict:
    payload = json.dumps({
        "transcript": transcript,
        "acoustic_hash": acoustic_hash,
    }).encode()
    req = urllib.request.Request(
        f"http://{HOST}:{PORT}/command",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python command_client.py "deploy application my-app"')
        sys.exit(1)
    print(json.dumps(send_command(" ".join(sys.argv[1:])), indent=2))
