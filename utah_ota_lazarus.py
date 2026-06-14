#!/usr/bin/env python3
"""
UtahMosphere OTA Lazarus Channel - Golden Master v25.0
Over-The-Air kernel updates pushed to swarm nodes via DHT routing.
"""

import json
import os
import hashlib
import urllib.request
from typing import Optional

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
DEFAULT_KERNEL_URL = os.environ.get("UTAH_OTA_KERNEL_URL", "")


def compute_payload_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def push_kernel_to_node(
    swarm_node,
    target_node_hash: str,
    kernel_path: str,
    version: str = "25.0",
) -> bool:
    """Push kernel bytecode manifest to a remote swarm peer via DHT."""
    with open(kernel_path, "rb") as f:
        data = f.read()
    payload = {
        "type": "OTA_LAZARUS",
        "artifact": "utahmosphere_master.py",
        "version": version,
        "hash": compute_payload_hash(data),
        "size": len(data),
        "message": "Golden Master kernel patch ready for Lazarus injection",
    }
    return swarm_node.route_payload_deterministic(target_node_hash, payload)


def pull_and_verify(local_path: str, expected_hash: str, url: str) -> bool:
    """Download OTA artifact and verify SHA-256."""
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    if compute_payload_hash(data) != expected_hash:
        return False
    os.makedirs(os.path.dirname(local_path) or ".", exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(data)
    return True


def apply_ota_patch(patch_manifest: dict, install_dir: Optional[str] = None) -> str:
    """Apply OTA Lazarus patch metadata (full binary pull done separately)."""
    install = install_dir or os.environ.get("UTAH_INSTALL_DIR", "/opt/utahmosphere")
    meta_path = os.path.join(UTAH_DATA_DIR, "ota", "last_patch.json")
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    with open(meta_path, "w") as f:
        json.dump(patch_manifest, f, indent=4)
    return f"OTA manifest recorded. Restart utah-kernel to apply from {install}."
