#!/usr/bin/env python3
"""Kinematic Siphon — Ghost Tune binary protocol (B-Web) for native GPU clients."""

import json
import struct
import time
from typing import Any, Dict, List


class KinematicSiphon:
    """Encode Omni-Glass manifold as binary Ghost Tune — bypasses HTML/DOM."""

    MAGIC = b"UTAH\x01"

    @staticmethod
    def encode_scene_graph(manifold: Dict[str, Any]) -> bytes:
        """Pack state manifold into B-Web binary payload."""
        meta = json.dumps(
            {
                "ts": time.time(),
                "fps_target": 120,
                "ram_hint_mb": 4,
                "vertices": KinematicSiphon._scene_vertices(manifold),
            },
            separators=(",", ":"),
        ).encode("utf-8")
        return KinematicSiphon.MAGIC + struct.pack(">I", len(meta)) + meta

    @staticmethod
    def _scene_vertices(manifold: Dict[str, Any]) -> List[Dict[str, Any]]:
        vertices = []
        for i, thought in enumerate(manifold.get("omni_mind_thoughts", [])[:10]):
            vertices.append({"x": i * 0.1, "y": 0.8, "label": thought.get("thought", "")[:64]})
        for i, research in enumerate(manifold.get("utah_claw_research", [])[:10]):
            vertices.append({"x": i * 0.1, "y": 0.4, "label": research.get("concept", "")[:64]})
        return vertices

    @staticmethod
    def decode_scene_graph(payload: bytes) -> Dict[str, Any]:
        if not payload.startswith(KinematicSiphon.MAGIC):
            raise ValueError("invalid ghost tune magic")
        (size,) = struct.unpack(">I", payload[5:9])
        return json.loads(payload[9 : 9 + size].decode("utf-8"))


kinematic_siphon = KinematicSiphon()
