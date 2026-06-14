#!/usr/bin/env python3
"""
UtahMosphere Hardware Quote Registry (v30.0)
Distributed source of truth for TPM hardware quotes across the swarm.
"""

import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

REGISTRY_PATH = Path(
    os.environ.get(
        "UTAH_QUOTE_REGISTRY_PATH",
        os.path.join(
            os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"),
            "quote_registry.json",
        ),
    )
)


class QuoteRegistry:
    """Replicated registry: {hardware_id: public_quote_record}."""

    def __init__(self, path: Optional[Path] = None):
        self._path = path or REGISTRY_PATH
        self._lock = threading.RLock()
        self.registry: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        if self._path.is_file():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.registry = data.get("nodes", {})
            except Exception:
                self.registry = {}

    def _save(self):
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump({
                    "nodes": self.registry,
                    "epoch": time.time(),
                }, f, indent=2)
        except PermissionError:
            pass

    def register_node(
        self,
        hardware_id: str,
        public_quote: str,
        vibe_hash: Optional[str] = None,
        pcr_digest: Optional[str] = None,
        node_id: Optional[str] = None,
    ) -> bool:
        if not hardware_id or not public_quote:
            return False
        with self._lock:
            self.registry[hardware_id] = {
                "public_quote": public_quote,
                "vibe_hash": vibe_hash,
                "pcr_digest": pcr_digest,
                "node_id": node_id,
                "registered_at": time.time(),
                "status": "active",
            }
            self._save()
        print(f"[QuoteRegistry] Registered hardware {hardware_id[:16]}...")
        return True

    def is_valid_hardware(self, hardware_id: str) -> bool:
        with self._lock:
            entry = self.registry.get(hardware_id)
            return bool(entry and entry.get("status") == "active")

    def get_quote(self, hardware_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return dict(self.registry[hardware_id]) if hardware_id in self.registry else None

    def purge_node(self, hardware_id: str, reason: str = "compromised") -> bool:
        with self._lock:
            if hardware_id not in self.registry:
                return False
            self.registry[hardware_id]["status"] = "purged"
            self.registry[hardware_id]["purged_at"] = time.time()
            self.registry[hardware_id]["purge_reason"] = reason
            self._save()
        print(f"[QuoteRegistry] Purged hardware {hardware_id[:16]} ({reason}).")
        return True

    def merge_remote(self, remote_nodes: Dict[str, Dict[str, Any]]):
        if not remote_nodes:
            return
        with self._lock:
            for hw_id, entry in remote_nodes.items():
                local = self.registry.get(hw_id, {})
                remote_ts = entry.get("registered_at", 0)
                local_ts = local.get("registered_at", 0)
                if hw_id not in self.registry or remote_ts >= local_ts:
                    self.registry[hw_id] = entry
            self._save()

    def export_nodes(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {k: dict(v) for k, v in self.registry.items()}

    def list_active(self) -> List[str]:
        with self._lock:
            return [k for k, v in self.registry.items() if v.get("status") == "active"]

    def stats(self) -> dict:
        with self._lock:
            active = sum(1 for v in self.registry.values() if v.get("status") == "active")
            purged = sum(1 for v in self.registry.values() if v.get("status") == "purged")
            return {
                "active": active,
                "purged": purged,
                "total": len(self.registry),
            }


quote_registry = QuoteRegistry()
