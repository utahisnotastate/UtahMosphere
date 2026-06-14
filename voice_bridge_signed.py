#!/usr/bin/env python3
"""
UtahMosphere Voice Bridge — Automatic Nonce Signing (v27.0)
Builds replay-safe /command payloads with server-issued nonces.
"""

import hashlib
import hmac
import json
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Union

from nonce_guard import NonceGuard

KERNEL_URL = "http://127.0.0.1:8999"


def fetch_server_nonce(base_url: str = KERNEL_URL) -> Optional[int]:
    try:
        with urllib.request.urlopen(f"{base_url}/nonce", timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return int(data["nonce"])
    except Exception:
        return None


def get_signed_payload(
    transcript: str,
    secret_key: Union[str, bytes],
    nonce: Optional[int] = None,
    use_server_nonce: bool = True,
    kernel_url: str = KERNEL_URL,
) -> Dict[str, Any]:
    """
    Build a nonce-signed voice command payload.
    secret_key: 64-char acoustic_hash (vibe-print) used as HMAC key.
    """
    if isinstance(secret_key, bytes):
        signing_key = secret_key.decode("utf-8", errors="replace")
    else:
        signing_key = secret_key

    normalized = transcript.lower()
    issued = nonce
    if issued is None and use_server_nonce:
        issued = fetch_server_nonce(kernel_url)
    if issued is None:
        issued = int(time.time())

    command_signature = NonceGuard.compute_signature(signing_key, issued, normalized)
    return {
        "transcript": transcript,
        "acoustic_hash": signing_key,
        "nonce": issued,
        "command_signature": command_signature,
        "signature": command_signature,
    }


def post_signed_command(
    transcript: str,
    acoustic_hash: str,
    kernel_url: str = f"{KERNEL_URL}/command",
) -> Dict[str, Any]:
    payload = get_signed_payload(transcript, acoustic_hash, kernel_url=kernel_url.rsplit("/command", 1)[0])
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        kernel_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))
