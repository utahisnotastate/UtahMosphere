#!/usr/bin/env python3
"""
UtahMosphere Omni-Glass Engine
Holographic projection of the Agentic Mesh — replaces terminal logs with visual telemetry.
"""

import json
import os
import queue
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

GLASS_PATH = Path(
    os.environ.get(
        "UTAH_OMNI_GLASS_PATH",
        os.path.join(os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"), "omni_glass_log.json"),
    )
)
MAX_EVENTS = int(os.environ.get("UTAH_OMNI_GLASS_MAX_EVENTS", "200"))
GLASS_WS_PORT = int(os.environ.get("UTAH_OMNI_GLASS_PORT", "9091"))


class OmniGlassRelay:
    """FluxRelay — streams agentic manifold to subscribers at ~60 FPS."""

    def __init__(self):
        self._lock = threading.RLock()
        self._subscribers: List[queue.Queue] = []
        self.state_manifold: Dict[str, Any] = {
            "omni_mind_thoughts": [],
            "lazarus_mutations": [],
            "utah_claw_research": [],
            "tycoon_settlements": [],
            "notifications": [],
        }
        self._events: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if GLASS_PATH.is_file():
            try:
                with open(GLASS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._events = data.get("events", [])[-MAX_EVENTS:]
                if "manifold" in data:
                    self.state_manifold.update(data["manifold"])
            except Exception:
                self._events = []

    def _save(self):
        try:
            GLASS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(GLASS_PATH, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "events": self._events[-MAX_EVENTS:],
                        "manifold": self.state_manifold,
                        "epoch": time.time(),
                    },
                    f,
                    indent=2,
                )
        except PermissionError:
            pass

    def subscribe(self) -> queue.Queue:
        q: queue.Queue = queue.Queue(maxsize=64)
        with self._lock:
            self._subscribers.append(q)
        return q

    def unsubscribe(self, q: queue.Queue):
        with self._lock:
            if q in self._subscribers:
                self._subscribers.remove(q)

    def broadcast_state(self):
        with self._lock:
            payload = json.dumps(self.export_manifold())
            dead = []
            for sub in self._subscribers:
                try:
                    sub.put_nowait(payload)
                except queue.Full:
                    dead.append(sub)
            for d in dead:
                self._subscribers.remove(d)

    def log_thought_vector(self, agent: str, thought: str, mcp_tool: Optional[str] = None):
        entry = {"ts": time.time(), "agent": agent, "thought": thought, "tool": mcp_tool}
        with self._lock:
            self.state_manifold["omni_mind_thoughts"].insert(0, entry)
            self.state_manifold["omni_mind_thoughts"] = self.state_manifold["omni_mind_thoughts"][:10]
        self.record("thought", thought, tool=mcp_tool, payload={"agent": agent})
        self.broadcast_state()

    def log_lazarus_mutation(self, agent: str, detail: str):
        entry = {"ts": time.time(), "agent": agent, "mutation": detail}
        with self._lock:
            self.state_manifold["lazarus_mutations"].insert(0, entry)
            self.state_manifold["lazarus_mutations"] = self.state_manifold["lazarus_mutations"][:10]
        self.record("mutation", detail, payload={"agent": agent})
        self.broadcast_state()

    def log_claw_research(self, concept: str, phase: str):
        entry = {"ts": time.time(), "concept": concept, "phase": phase}
        with self._lock:
            self.state_manifold["utah_claw_research"].insert(0, entry)
            self.state_manifold["utah_claw_research"] = self.state_manifold["utah_claw_research"][:10]
        self.record("claw", f"{phase}: {concept[:80]}", payload=entry)
        self.broadcast_state()

    def notify_feature_ready(self, concept: str, tool_path: str):
        note = {
            "ts": time.time(),
            "title": "Feature compiled and injected",
            "concept": concept,
            "tool_path": tool_path,
        }
        with self._lock:
            self.state_manifold["notifications"].insert(0, note)
            self.state_manifold["notifications"] = self.state_manifold["notifications"][:5]
        self.broadcast_state()

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

    def export_manifold(self) -> Dict[str, Any]:
        with self._lock:
            return json.loads(json.dumps(self.state_manifold))

    def stats(self) -> dict:
        with self._lock:
            return {
                "events": len(self._events),
                "subscribers": len(self._subscribers),
                "path": str(GLASS_PATH),
                "ws_port": GLASS_WS_PORT,
            }


class OmniGlass(OmniGlassRelay):
    """Backward-compatible alias."""


omni_glass = OmniGlassRelay()
