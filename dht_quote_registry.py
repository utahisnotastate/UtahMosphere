#!/usr/bin/env python3
"""
UtahMosphere DHT-Federated Quote Registry (v30.0)
Global consensus ledger of golden TPM PCR measurements across the swarm DHT.
"""

import hashlib
import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

DHT_FEDERATION_ENFORCE = os.environ.get("UTAH_DHT_FEDERATION_ENFORCE", "1") != "0"
GOLDEN_REGISTRY_PATH = Path(
    os.environ.get(
        "UTAH_DHT_GOLDEN_REGISTRY_PATH",
        os.path.join(
            os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"),
            "dht_golden_registry.json",
        ),
    )
)

try:
    from quote_registry import quote_registry
except ImportError:
    quote_registry = None  # type: ignore


def _quote_fingerprint(quote: Any) -> str:
    if isinstance(quote, dict):
        body = quote.get("body", "")
        if isinstance(body, str):
            return hashlib.sha256(body.encode("utf-8")).hexdigest()
        return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
    if isinstance(quote, str):
        try:
            parsed = json.loads(quote)
            return _quote_fingerprint(parsed)
        except json.JSONDecodeError:
            return hashlib.sha256(quote.encode("utf-8")).hexdigest()
    return hashlib.sha256(str(quote).encode("utf-8")).hexdigest()


def _pcr_digest(pcr_raw: str) -> str:
    return hashlib.sha256(pcr_raw.encode("utf-8")).hexdigest()


class GlobalQuoteRegistry:
    """Manages the distributed registry of known-good TPM quotes (golden measurements)."""

    def __init__(self, path: Optional[Path] = None):
        self._path = path or GOLDEN_REGISTRY_PATH
        self._lock = threading.RLock()
        self.registry: Dict[str, Dict[str, Any]] = {}

    def _load(self):
        if self._path.is_file():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.registry = data.get("golden", {})
            except Exception:
                self.registry = {}

    def _save(self):
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump({"golden": self.registry, "epoch": time.time()}, f, indent=2)
        except PermissionError:
            pass

    def record_golden(
        self,
        peer_id: str,
        quote: Any,
        pcr_digest: Optional[str] = None,
        hardware_id: Optional[str] = None,
    ) -> bool:
        if not peer_id or quote is None:
            return False
        fingerprint = _quote_fingerprint(quote)
        with self._lock:
            self.registry[peer_id] = {
                "golden_quote": fingerprint,
                "pcr_digest": pcr_digest,
                "hardware_id": hardware_id,
                "quote_snapshot": quote if isinstance(quote, str) else json.dumps(quote),
                "recorded_at": time.time(),
                "status": "consensus",
            }
            self._save()
        print(f"[DHT-Golden] Recorded consensus for {peer_id[:16]}...")
        return True

    def verify_against_swarm(self, peer_id: str, quote: Any) -> bool:
        if not DHT_FEDERATION_ENFORCE:
            return True
        if not peer_id or quote is None:
            return False
        with self._lock:
            entry = self.registry.get(peer_id)
            if not entry:
                if quote_registry:
                    hw = peer_id
                    if isinstance(quote, dict):
                        try:
                            body = json.loads(quote.get("body", "{}"))
                            hw = body.get("hardware_id", peer_id)
                        except json.JSONDecodeError:
                            pass
                    if quote_registry.is_valid_hardware(hw):
                        return True
                return not DHT_FEDERATION_ENFORCE
            expected = entry.get("golden_quote")
            presented = _quote_fingerprint(quote)
            if expected != presented:
                return False
            if isinstance(quote, dict):
                try:
                    body = json.loads(quote.get("body", "{}"))
                    golden_pcr = entry.get("pcr_digest")
                    if golden_pcr and body.get("pcr0_digest") != golden_pcr:
                        return False
                except json.JSONDecodeError:
                    return False
            return True

    def merge_dht_consensus(self, remote_golden: Dict[str, Dict[str, Any]]):
        if not remote_golden:
            return
        with self._lock:
            for peer_id, entry in remote_golden.items():
                local = self.registry.get(peer_id, {})
                remote_ts = entry.get("recorded_at", 0)
                local_ts = local.get("recorded_at", 0)
                if peer_id not in self.registry or remote_ts >= local_ts:
                    self.registry[peer_id] = entry
            self._save()

    def federate_from_quote_registry(self):
        if not quote_registry:
            return
        with self._lock:
            for hw_id, entry in quote_registry.export_nodes().items():
                if entry.get("status") != "active":
                    continue
                peer = entry.get("node_id") or hw_id
                quote_raw = entry.get("public_quote")
                if not quote_raw:
                    continue
                self.registry.setdefault(peer, {
                    "golden_quote": _quote_fingerprint(quote_raw),
                    "pcr_digest": entry.get("pcr_digest"),
                    "hardware_id": hw_id,
                    "quote_snapshot": quote_raw,
                    "recorded_at": entry.get("registered_at", time.time()),
                    "status": "consensus",
                })
            self._save()

    def purge_peer(self, peer_id: str, reason: str = "drift") -> bool:
        with self._lock:
            if peer_id not in self.registry:
                return False
            self.registry[peer_id]["status"] = "quarantined"
            self.registry[peer_id]["quarantine_reason"] = reason
            self.registry[peer_id]["quarantined_at"] = time.time()
            self._save()
        print(f"[DHT-Golden] Quarantined peer {peer_id[:16]} ({reason}).")
        return True

    def export_golden(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {k: dict(v) for k, v in self.registry.items()}

    def stats(self) -> dict:
        with self._lock:
            consensus = sum(1 for v in self.registry.values() if v.get("status") == "consensus")
            quarantined = sum(1 for v in self.registry.values() if v.get("status") == "quarantined")
            return {
                "consensus": consensus,
                "quarantined": quarantined,
                "total": len(self.registry),
                "enforce": DHT_FEDERATION_ENFORCE,
            }


dht_quote_registry = GlobalQuoteRegistry()
dht_quote_registry._load()
