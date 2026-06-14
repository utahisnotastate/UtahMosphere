#!/usr/bin/env python3
"""
UtahMosphere Global Swarm Protocol - Golden Master v25.0
Deterministic Kademlia-style DHT routing with iterative peer lookup.
"""

import os
import json
import time
import socket
import threading
import hashlib
from typing import Dict, Any, Optional, List, Callable

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")


def _resolve_swarm_dir() -> str:
    primary = os.path.join(UTAH_DATA_DIR, "swarm")
    try:
        os.makedirs(primary, exist_ok=True)
        return primary
    except PermissionError:
        fallback = "swarm"
        os.makedirs(fallback, exist_ok=True)
        return fallback


UTAH_SWARM_DIR = _resolve_swarm_dir()
ROUTING_TABLE_FILE = os.path.join(UTAH_SWARM_DIR, "dht_routing.json")
SWARM_PORT = 9055
K_BUCKET_SIZE = 8


class UtahSwarmNode:
    def __init__(
        self,
        node_hash: str,
        on_ledger_sync: Optional[Callable[[dict], None]] = None,
        on_attestation: Optional[Callable[[dict, str, tuple], None]] = None,
    ):
        self.node_hash = node_hash.zfill(64)[:64]
        self.routing_table: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._on_ledger_sync = on_ledger_sync
        self._on_attestation = on_attestation
        self._bootstrap_swarm_paths()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("", SWARM_PORT))
        except Exception as e:
            print(f"[Swarm Engine] Socket binding failed: {e}")
            self.sock = None

        print(f"[Swarm Engine] DHT Node Online. ID: {self.node_hash[:16]}...")

        if self.sock:
            threading.Thread(target=self._listen_for_swarm_packets, daemon=True).start()
            threading.Thread(target=self._ping_nearest_neighbors, daemon=True).start()

    def _bootstrap_swarm_paths(self):
        os.makedirs(UTAH_SWARM_DIR, exist_ok=True)
        if os.path.exists(ROUTING_TABLE_FILE):
            try:
                with open(ROUTING_TABLE_FILE, "r") as f:
                    self.routing_table = json.load(f)
            except Exception:
                self.routing_table = {}
        else:
            self.routing_table = {}
            self._save_routing_table()

    def _save_routing_table(self):
        try:
            with open(ROUTING_TABLE_FILE, "w") as f:
                json.dump(self.routing_table, f, indent=4)
        except PermissionError:
            pass

    @staticmethod
    def _xor_distance(hash1: str, hash2: str) -> int:
        h1 = hash1.zfill(64)[:64]
        h2 = hash2.zfill(64)[:64]
        return int(h1, 16) ^ int(h2, 16)

    def introduce_peer(self, peer_hash: str, ip: str, port: int):
        peer_hash = peer_hash.zfill(64)[:64]
        with self._lock:
            self.routing_table[peer_hash] = {
                "ip": ip,
                "port": port,
                "last_seen": time.time(),
                "distance": self._xor_distance(self.node_hash, peer_hash),
            }
            if len(self.routing_table) > 256:
                farthest = max(self.routing_table, key=lambda k: self.routing_table[k]["distance"])
                del self.routing_table[farthest]
            self._save_routing_table()

    def find_closest_peers(self, target_hash: str, count: int = K_BUCKET_SIZE) -> List[dict]:
        target_hash = target_hash.zfill(64)[:64]
        with self._lock:
            peers = sorted(
                self.routing_table.values(),
                key=lambda p: self._xor_distance(target_hash, hashlib.sha256(f"{p['ip']}:{p['port']}".encode()).hexdigest()),
            )
        return peers[:count]

    def route_payload_deterministic(self, target_hash: str, payload: dict) -> bool:
        """Iterative DHT routing: send to closest known peer toward target."""
        if not self.sock:
            return False
        target_hash = target_hash.zfill(64)[:64]

        with self._lock:
            if target_hash in self.routing_table:
                target_info = self.routing_table[target_hash]
                return self._send_to(target_info["ip"], target_info["port"], payload)

        closest = self.find_closest_peers(target_hash, count=3)
        if not closest:
            self._broadcast_find_node(target_hash)
            return False

        sent = False
        for peer in closest:
            if self._send_to(peer["ip"], peer["port"], {"type": "FIND_NODE", "target": target_hash, "payload": payload}):
                sent = True
        return sent

    def send_encrypted_payload(self, target_hash: str, payload: dict) -> bool:
        return self.route_payload_deterministic(target_hash, payload)

    def _send_to(self, ip: str, port: int, inner_payload: dict) -> bool:
        if not self.sock:
            return False
        data = json.dumps({
            "source_hash": self.node_hash,
            "timestamp": time.time(),
            "payload": inner_payload,
        }).encode("utf-8")
        try:
            self.sock.sendto(data, (ip, port))
            return True
        except Exception:
            return False

    def _broadcast_find_node(self, target_hash: str):
        with self._lock:
            for info in list(self.routing_table.values())[:K_BUCKET_SIZE]:
                self._send_to(info["ip"], info["port"], {"type": "FIND_NODE", "target": target_hash})

    def _listen_for_swarm_packets(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(65535)
                packet = json.loads(data.decode("utf-8"))
                source_hash = packet.get("source_hash")
                if not source_hash or source_hash == self.node_hash:
                    continue

                self.introduce_peer(source_hash, addr[0], addr[1])
                payload = packet.get("payload", {})

                if payload.get("type") == "PING":
                    continue

                if payload.get("type") == "FIND_NODE":
                    target = payload.get("target", "")
                    closest = self.find_closest_peers(target, count=3)
                    self._send_to(addr[0], addr[1], {
                        "type": "FIND_NODE_RESPONSE",
                        "target": target,
                        "peers": [{"ip": p["ip"], "port": p["port"]} for p in closest],
                    })
                    inner = payload.get("payload")
                    if inner:
                        self.route_payload_deterministic(target, inner)
                    continue

                if payload.get("type") == "FIND_NODE_RESPONSE":
                    for peer in payload.get("peers", []):
                        ph = hashlib.sha256(f"{peer['ip']}:{peer['port']}".encode()).hexdigest()
                        self.introduce_peer(ph, peer["ip"], peer["port"])
                    continue

                if payload.get("type") == "LEDGER_SYNC" and self._on_ledger_sync:
                    self._on_ledger_sync(payload)
                    continue

                if payload.get("type") == "DHT_GOLDEN_SYNC" and self._on_ledger_sync:
                    self._on_ledger_sync(payload)
                    continue

                if payload.get("type") in (
                    "ATTESTATION_CHALLENGE",
                    "ATTESTATION_RESPONSE",
                    "QUARANTINE_NOTICE",
                ) and self._on_attestation:
                    self._on_attestation(payload, source_hash, addr)
                    continue

            except Exception:
                pass

    def challenge_peer_attestation(self, target_hash: str) -> bool:
        return self.route_payload_deterministic(target_hash, {
            "type": "ATTESTATION_CHALLENGE",
            "challenger": self.node_hash,
            "timestamp": time.time(),
        })

    def _ping_nearest_neighbors(self):
        while True:
            time.sleep(30)
            if not self.sock:
                continue
            stale = []
            with self._lock:
                for peer_hash, info in self.routing_table.items():
                    if time.time() - info["last_seen"] > 300:
                        stale.append(peer_hash)
                    else:
                        self._send_to(info["ip"], info["port"], {"type": "PING"})
                for peer in stale:
                    del self.routing_table[peer]
                if stale:
                    self._save_routing_table()

    def peer_count(self) -> int:
        with self._lock:
            return len(self.routing_table)
