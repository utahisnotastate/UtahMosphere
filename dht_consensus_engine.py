#!/usr/bin/env python3
"""
UtahMosphere DHT Consensus Engine (v31.0)
Majority-quorum (51%+) federated validation of TPM hardware quotes across the swarm.
"""

import hashlib
import json
import os
import threading
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Optional

QUORUM_ENFORCE = os.environ.get("UTAH_QUORUM_ENFORCE", "1") != "0"
QUORUM_THRESHOLD = float(os.environ.get("UTAH_QUORUM_THRESHOLD", "0.51"))
QUORUM_REGISTRY_PATH = Path(
    os.environ.get(
        "UTAH_QUORUM_REGISTRY_PATH",
        os.path.join(
            os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"),
            "dht_quorum_registry.json",
        ),
    )
)

try:
    from dht_quote_registry import GlobalQuoteRegistry, _quote_fingerprint, dht_quote_registry
except ImportError:
    GlobalQuoteRegistry = None  # type: ignore
    dht_quote_registry = None  # type: ignore

    def _quote_fingerprint(quote: Any) -> str:
        raw = json.dumps(quote, sort_keys=True) if isinstance(quote, dict) else str(quote)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class GlobalQuoteQuorum:
    """Manages the distributed DHT-federated registry with majority consensus."""

    def __init__(self, path: Optional[Path] = None):
        self._path = path or QUORUM_REGISTRY_PATH
        self._lock = threading.RLock()
        self.consensus_registry: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        if self._path.is_file():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.consensus_registry = data.get("consensus", {})
            except Exception:
                self.consensus_registry = {}

    def _save(self):
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump({
                    "consensus": self.consensus_registry,
                    "threshold": QUORUM_THRESHOLD,
                    "epoch": time.time(),
                }, f, indent=2)
        except PermissionError:
            pass

    def _recompute_consensus(self, peer_id: str):
        entry = self.consensus_registry.get(peer_id, {})
        votes: Dict[str, str] = entry.get("votes", {})
        if not votes:
            return
        counts = Counter(votes.values())
        fingerprint, tally = counts.most_common(1)[0]
        ratio = tally / len(votes)
        if ratio >= QUORUM_THRESHOLD:
            entry["golden_quote"] = fingerprint
            entry["quorum_ratio"] = round(ratio, 4)
            entry["vote_count"] = len(votes)
            entry["status"] = "quorum_reached"
            self.consensus_registry[peer_id] = entry

    def record_vote(self, peer_id: str, quote: Any, voter_id: str) -> bool:
        if not peer_id or not voter_id or quote is None:
            return False
        fingerprint = _quote_fingerprint(quote)
        with self._lock:
            entry = self.consensus_registry.setdefault(peer_id, {
                "votes": {},
                "golden_quote": None,
                "status": "pending",
            })
            entry["votes"][voter_id] = fingerprint
            self._recompute_consensus(peer_id)
            self._save()
        return True

    def record_golden(self, peer_id: str, quote: Any, voter_id: Optional[str] = None) -> bool:
        voter = voter_id or peer_id
        ok = self.record_vote(peer_id, quote, voter)
        if dht_quote_registry:
            try:
                body = json.loads(quote.get("body", "{}")) if isinstance(quote, dict) else {}
            except json.JSONDecodeError:
                body = {}
            dht_quote_registry.record_golden(
                peer_id,
                quote,
                pcr_digest=body.get("pcr0_digest") if isinstance(body, dict) else None,
                hardware_id=body.get("hardware_id") if isinstance(body, dict) else None,
            )
        return ok

    def verify_against_quorum(self, peer_id: str, quote: Any) -> bool:
        if not QUORUM_ENFORCE:
            return True
        if not peer_id or quote is None:
            return False
        presented = _quote_fingerprint(quote)
        with self._lock:
            entry = self.consensus_registry.get(peer_id, {})
            expected = entry.get("golden_quote")
            if expected:
                if presented != expected:
                    return False
                if entry.get("status") != "quorum_reached":
                    return tally_meets_quorum(entry)
                return True
        if dht_quote_registry:
            return dht_quote_registry.verify_against_swarm(peer_id, quote)
        return not QUORUM_ENFORCE

    def merge_quorum_votes(self, remote: Dict[str, Dict[str, Any]]):
        if not remote:
            return
        with self._lock:
            for peer_id, remote_entry in remote.items():
                local = self.consensus_registry.get(peer_id, {"votes": {}})
                remote_votes = remote_entry.get("votes", {})
                merged_votes = dict(local.get("votes", {}))
                merged_votes.update(remote_votes)
                self.consensus_registry[peer_id] = {
                    **local,
                    **{k: v for k, v in remote_entry.items() if k != "votes"},
                    "votes": merged_votes,
                }
                self._recompute_consensus(peer_id)
            self._save()

    def purge_peer(self, peer_id: str, reason: str = "quorum_mismatch") -> bool:
        with self._lock:
            if peer_id not in self.consensus_registry:
                return False
            self.consensus_registry[peer_id]["status"] = "quarantined"
            self.consensus_registry[peer_id]["quarantine_reason"] = reason
            self.consensus_registry[peer_id]["quarantined_at"] = time.time()
            self._save()
        if dht_quote_registry:
            dht_quote_registry.purge_peer(peer_id, reason)
        print(f"[Quorum] Peer {peer_id[:16]} quarantined ({reason}).")
        return True

    def export_consensus(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {k: dict(v) for k, v in self.consensus_registry.items()}

    def stats(self) -> dict:
        with self._lock:
            reached = sum(1 for v in self.consensus_registry.values() if v.get("status") == "quorum_reached")
            pending = sum(1 for v in self.consensus_registry.values() if v.get("status") == "pending")
            quarantined = sum(1 for v in self.consensus_registry.values() if v.get("status") == "quarantined")
            return {
                "quorum_reached": reached,
                "pending": pending,
                "quarantined": quarantined,
                "total": len(self.consensus_registry),
                "threshold": QUORUM_THRESHOLD,
                "enforce": QUORUM_ENFORCE,
            }


def tally_meets_quorum(entry: Dict[str, Any]) -> bool:
    votes = entry.get("votes", {})
    if not votes:
        return False
    counts = Counter(votes.values())
    _, tally = counts.most_common(1)[0]
    return (tally / len(votes)) >= QUORUM_THRESHOLD


dht_consensus_engine = GlobalQuoteQuorum()
