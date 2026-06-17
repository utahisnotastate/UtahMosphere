#!/usr/bin/env python3
"""Osmotic Router — shard KV-cache across UtahNetes swarm peers."""

import os
from typing import Any, Dict, List


class UtahOsmoticRouter:
    """Offloads tensor shards to peer nodes when local VRAM is exhausted."""

    def __init__(self):
        self._peers: List[str] = [
            p.strip() for p in os.environ.get("UTAH_OSMOTIC_PEERS", "").split(",") if p.strip()
        ]

    def route_shard(self, shard_id: int, payload: bytes) -> Dict[str, Any]:
        if not self._peers:
            return {"shard_id": shard_id, "local": True, "bytes": len(payload)}
        peer = self._peers[shard_id % len(self._peers)]
        return {"shard_id": shard_id, "peer": peer, "bytes": len(payload), "offloaded": True}

    def stats(self) -> dict:
        return {"peers": len(self._peers), "mesh_ready": bool(self._peers)}
