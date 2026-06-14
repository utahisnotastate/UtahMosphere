#!/usr/bin/env python3
"""
UtahMosphere State-Diff Engine (v32.0)
Entangled state synchronization — minimal mathematical deltas for swarm registry sync.
"""

import hashlib
import json
import os
from typing import Any, Dict, Optional

STATE_DIFF_ENFORCE = os.environ.get("UTAH_STATE_DIFF_ENFORCE", "1") != "0"
MAX_DELTA_BYTES = int(os.environ.get("UTAH_STATE_DIFF_MAX_BYTES", "1024"))


def state_hash(state: Dict[str, Any]) -> str:
    canonical = json.dumps(state, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def get_state_delta(local_state: Dict[str, Any], remote_state: Dict[str, Any]) -> Dict[str, Any]:
    """Computes minimal mathematical diff for global state sync."""
    delta: Dict[str, Any] = {}
    for key, val in local_state.items():
        if remote_state.get(key) != val:
            delta[key] = val
    for key in remote_state:
        if key not in local_state:
            delta[key] = None
    return delta


def apply_state_delta(base_state: Dict[str, Any], delta: Dict[str, Any]) -> Dict[str, Any]:
    """Apply entangled delta to reconstruct synchronized state."""
    merged = dict(base_state)
    for key, val in delta.items():
        if val is None:
            merged.pop(key, None)
        else:
            merged[key] = val
    return merged


def encode_delta(local_state: Dict[str, Any], remote_state: Dict[str, Any]) -> Dict[str, Any]:
    """Package delta with hash for witness verification."""
    delta = get_state_delta(local_state, remote_state)
    payload = {
        "delta": delta,
        "base_hash": state_hash(remote_state),
        "target_hash": state_hash(apply_state_delta(remote_state, delta)),
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if STATE_DIFF_ENFORCE and len(raw) > MAX_DELTA_BYTES:
        payload["delta"] = {"_truncated": True, "keys": list(delta.keys())[:8]}
        payload["oversize"] = len(raw)
    payload["bytes"] = len(json.dumps(payload, sort_keys=True).encode("utf-8"))
    return payload


def should_use_delta(local_state: Dict[str, Any], remote_state: Dict[str, Any]) -> bool:
    if not STATE_DIFF_ENFORCE:
        return False
    full = json.dumps(local_state, sort_keys=True).encode("utf-8")
    delta_pkg = encode_delta(local_state, remote_state)
    return delta_pkg.get("bytes", len(full)) < len(full)
