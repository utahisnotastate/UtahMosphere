#!/usr/bin/env python3
"""
UtahMosphere Multi-Region Quorum Witnesses (v32.0)
Lightweight regional observers that tie-break consensus during ISP/partition outages.
"""

import hashlib
import json
import os
import socket
import threading
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

WITNESS_ENFORCE = os.environ.get("UTAH_WITNESS_ENFORCE", "1") != "0"
WITNESS_THRESHOLD = float(os.environ.get("UTAH_WITNESS_THRESHOLD", "0.51"))
WITNESS_PATH = Path(
    os.environ.get(
        "UTAH_WITNESS_REGISTRY_PATH",
        os.path.join(
            os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"),
            "quorum_witness.json",
        ),
    )
)

DEFAULT_WITNESSES = [
    {"region": "us-east", "endpoint": "https://witness-us.utahmosphere.internal/consensus"},
    {"region": "eu-west", "endpoint": "https://witness-eu.utahmosphere.internal/consensus"},
    {"region": "oceania-apac", "endpoint": "https://witness-apac.utahmosphere.internal/consensus"},
]

_custom = os.environ.get("UTAH_WITNESS_NODES", "")
if _custom.strip():
    DEFAULT_WITNESSES = [
        {"region": f"witness-{i}", "endpoint": ep.strip()}
        for i, ep in enumerate(_custom.split(","))
        if ep.strip()
    ]


class WitnessNode:
    """Single regional witness stub."""

    def __init__(self, region: str, endpoint: str):
        self.region = region
        self.endpoint = endpoint
        self.last_seen: Optional[float] = None
        self.last_hash: Optional[str] = None

    def ping_and_verify(self, proposed_state_hash: str, timeout: float = 2.0) -> bool:
        if not proposed_state_hash:
            return False
        try:
            url = f"{self.endpoint}?hash={proposed_state_hash}"
            req = urllib.request.Request(url, headers={"User-Agent": "UtahMosphere-Witness/32.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status != 200:
                    return False
                data = json.loads(resp.read().decode("utf-8"))
                confirmed = data.get("confirmed_hash") == proposed_state_hash or data.get("ok") is True
                if confirmed:
                    self.last_seen = time.time()
                    self.last_hash = proposed_state_hash
                return confirmed
        except Exception:
            return self._local_verify(proposed_state_hash)

    def _local_verify(self, proposed_state_hash: str) -> bool:
        """Dev fallback: witness confirms hash if endpoint unreachable (partition sim)."""
        if not WITNESS_ENFORCE:
            self.last_seen = time.time()
            self.last_hash = proposed_state_hash
            return True
        return False


class QuorumWitness:
    """Nodes that verify consensus without processing application data."""

    def __init__(self, swarm_nodes: Optional[List[Dict[str, str]]] = None):
        self._lock = threading.RLock()
        nodes = swarm_nodes or DEFAULT_WITNESSES
        self.witnesses: List[WitnessNode] = [
            WitnessNode(n["region"], n["endpoint"]) for n in nodes
        ]
        self._confirmed_hashes: Dict[str, int] = {}
        self._load()

    def _load(self):
        if WITNESS_PATH.is_file():
            try:
                with open(WITNESS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._confirmed_hashes = data.get("hashes", {})
            except Exception:
                self._confirmed_hashes = {}

    def _save(self):
        try:
            WITNESS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(WITNESS_PATH, "w", encoding="utf-8") as f:
                json.dump({"hashes": self._confirmed_hashes, "epoch": time.time()}, f, indent=2)
        except PermissionError:
            pass

    def get_consensus(self, proposed_state: str) -> bool:
        """Return True when > threshold of witnesses confirm the state hash."""
        if not WITNESS_ENFORCE:
            return True
        if not self.witnesses:
            return True
        votes = 0
        for witness in self.witnesses:
            if witness.ping_and_verify(proposed_state):
                votes += 1
        ratio = votes / len(self.witnesses)
        if ratio > WITNESS_THRESHOLD:
            with self._lock:
                self._confirmed_hashes[proposed_state] = self._confirmed_hashes.get(proposed_state, 0) + 1
                self._save()
            return True
        return False

    def record_local_witness(self, state_hash: str) -> bool:
        """Local node acts as witness for its region when remote witnesses unavailable."""
        with self._lock:
            self._confirmed_hashes[state_hash] = self._confirmed_hashes.get(state_hash, 0) + 1
            self._save()
        return True

    def export_witnesses(self) -> List[dict]:
        return [
            {
                "region": w.region,
                "endpoint": w.endpoint,
                "last_seen": w.last_seen,
                "last_hash": w.last_hash,
            }
            for w in self.witnesses
        ]

    def stats(self) -> dict:
        with self._lock:
            return {
                "witnesses": len(self.witnesses),
                "confirmed_hashes": len(self._confirmed_hashes),
                "threshold": WITNESS_THRESHOLD,
                "enforce": WITNESS_ENFORCE,
                "regions": [w.region for w in self.witnesses],
            }


quorum_witness = QuorumWitness()
