#!/usr/bin/env python3
"""
UtahNetes Mesh Engine - Golden Master v25.0
Unified LAN multicast gossip + Swarm DHT planetary sync.
"""

import json
import os
import socket
import struct
import threading
import hashlib
import time
from typing import Callable, Optional, Any

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
MASTER_REGISTRY_FILE = os.path.join(UTAH_DATA_DIR, "master_registry.json")
GOSSIP_PORT = 9001
MULTICAST_ADDR = "239.255.43.21"
MESH_INTERVAL_SEC = 5


class UtahNetesMesh:
    def __init__(
        self,
        node_id: str,
        get_registry: Callable[[], dict],
        apply_registry: Callable[[dict], None],
        swarm_broadcast: Optional[Callable[[dict], None]] = None,
    ):
        self.node_id = node_id
        self._get_registry = get_registry
        self._apply_registry = apply_registry
        self._swarm_broadcast = swarm_broadcast
        self._stop = threading.Event()
        threading.Thread(target=self._mesh_sync_loop, daemon=True).start()
        threading.Thread(target=self._mesh_listener, daemon=True).start()
        print(f"[UtahNetes] Mesh engine online. Multicast {MULTICAST_ADDR}:{GOSSIP_PORT}")

    def _persist_master_registry(self, registry: dict):
        try:
            os.makedirs(os.path.dirname(MASTER_REGISTRY_FILE), exist_ok=True)
            with open(MASTER_REGISTRY_FILE, "w") as f:
                json.dump({
                    "node": self.node_id,
                    "tenants": registry.get("tenants", {}),
                    "ledger": registry.get("ledger", {}),
                    "epoch": time.time(),
                }, f, indent=4)
        except PermissionError:
            pass

    def _mesh_sync_loop(self):
        """Broadcast state to planetary DHT every MESH_INTERVAL_SEC."""
        tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        tx.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        while not self._stop.is_set():
            try:
                registry = self._get_registry()
                payload = json.dumps({
                    "node": self.node_id,
                    "registry": registry,
                    "type": "MESH_SYNC",
                }).encode("utf-8")
                tx.sendto(payload, (MULTICAST_ADDR, GOSSIP_PORT))
                self._persist_master_registry(registry)
                if self._swarm_broadcast:
                    self._swarm_broadcast({
                        "type": "LEDGER_SYNC",
                        "registry": registry,
                        "origin_node": self.node_id,
                    })
            except Exception:
                pass
            self._stop.wait(MESH_INTERVAL_SEC)

    def _mesh_listener(self):
        rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        rx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            rx.bind(("", GOSSIP_PORT))
            mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_ADDR), socket.INADDR_ANY)
            rx.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception as e:
            print(f"[UtahNetes] Listener bind failed: {e}")
            return

        while not self._stop.is_set():
            try:
                data, _ = rx.recvfrom(65535)
                message = json.loads(data.decode("utf-8"))
                remote = message.get("node")
                if remote and remote != self.node_id:
                    self._apply_registry(message.get("registry", {}))
            except Exception:
                pass


def derive_node_hash(hostname: str, vibe_hash: Optional[str] = None) -> str:
    if vibe_hash:
        return vibe_hash.zfill(64)[:64]
    return hashlib.sha256(hostname.encode()).hexdigest()
