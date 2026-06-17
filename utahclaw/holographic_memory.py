#!/usr/bin/env python3
"""Holographic Memory — superposed concept interference patterns (UtahClaw)."""

import hashlib
import json
import os
import threading
from pathlib import Path
from typing import Dict, List, Optional

MEMORY_PATH = Path(
    os.environ.get(
        "UTAH_CLAW_MEMORY_PATH",
        os.path.join(os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"), "claw_holographic_memory.json"),
    )
)


class HolographicMemory:
    """Fold documentation into interference patterns; reconstruct concepts from partial data."""

    def __init__(self):
        self._lock = threading.RLock()
        self._patterns: Dict[str, List[float]] = {}
        self._raw: Dict[str, str] = {}
        self._load()

    def _load(self):
        if MEMORY_PATH.is_file():
            try:
                data = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
                self._patterns = data.get("patterns", {})
                self._raw = data.get("raw", {})
            except Exception:
                self._patterns = {}
                self._raw = {}

    def _save(self):
        try:
            MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
            MEMORY_PATH.write_text(
                json.dumps({"patterns": self._patterns, "raw": self._raw}, indent=2),
                encoding="utf-8",
            )
        except PermissionError:
            pass

    def calculate_interference(self, data: str) -> List[float]:
        digest = hashlib.sha256(data.encode("utf-8")).digest()
        return [((b / 127.5) - 1.0) for b in digest[:32]]

    def absorb_concept(self, concept: str, raw_data: str) -> List[float]:
        pattern = self.calculate_interference(raw_data)
        with self._lock:
            existing = self._patterns.get(concept)
            if existing and len(existing) == len(pattern):
                pattern = [(a + b) / 2.0 for a, b in zip(existing, pattern)]
            self._patterns[concept] = pattern
            self._raw[concept] = raw_data[:65536]
            self._save()
        return pattern

    def recall(self, concept: str) -> Optional[str]:
        with self._lock:
            return self._raw.get(concept)

    def export_patterns(self) -> Dict[str, List[float]]:
        with self._lock:
            return dict(self._patterns)

    def stats(self) -> dict:
        with self._lock:
            return {"concepts": len(self._patterns), "path": str(MEMORY_PATH)}


holographic_memory = HolographicMemory()
