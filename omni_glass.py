#!/usr/bin/env python3
"""
UtahMosphere Omni-Glass — real-time agentic action log for the Omni-Compiler mesh.
"""

import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

GLASS_PATH = Path(
    os.environ.get(
        "UTAH_OMNI_GLASS_PATH",
        os.path.join(os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"), "omni_glass_log.json"),
    )
)
MAX_EVENTS = int(os.environ.get("UTAH_OMNI_GLASS_MAX_EVENTS", "200"))


class OmniGlass:
    """Holographic-style dashboard feed: tool calls, thoughts, file mutations."""

    def __init__(self):
        self._lock = threading.RLock()
        self._events: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if GLASS_PATH.is_file():
            try:
                with open(GLASS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._events = data.get("events", [])[-MAX_EVENTS:]
            except Exception:
                self._events = []

    def _save(self):
        try:
            GLASS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(GLASS_PATH, "w", encoding="utf-8") as f:
                json.dump({"events": self._events[-MAX_EVENTS:], "epoch": time.time()}, f, indent=2)
        except PermissionError:
            pass

    def record(
        self,
        phase: str,
        message: str,
        *,
        tool: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ):
        event = {
            "ts": time.time(),
            "phase": phase,
            "message": message,
            "tool": tool,
            "payload": payload or {},
        }
        with self._lock:
            self._events.append(event)
            self._events = self._events[-MAX_EVENTS:]
            self._save()

    def export(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._events[-limit:])

    def stats(self) -> dict:
        with self._lock:
            return {"events": len(self._events), "path": str(GLASS_PATH)}


omni_glass = OmniGlass()
