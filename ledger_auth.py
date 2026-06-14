#!/usr/bin/env python3
"""
Utah-Kernel: Authorized Node Security Enforcement (v25.1)
Cryptographic HMAC validation for mesh gossip and delegated voice authority.
"""

import hmac
import hashlib
import json
from typing import Iterable, List, Optional


class AuthGuard:
    """Enforces biometric node whitelist from secure_registry / biometric ledger."""

    def __init__(self, authorized_nodes: Optional[Iterable[str]] = None, root_vibe_hash: Optional[str] = None):
        self.whitelist: List[str] = []
        if root_vibe_hash:
            self.whitelist.append(root_vibe_hash)
        if authorized_nodes:
            for node_hash in authorized_nodes:
                if node_hash and node_hash not in self.whitelist:
                    self.whitelist.append(node_hash)

    def refresh(self, authorized_nodes: Iterable[str], root_vibe_hash: Optional[str] = None):
        self.whitelist = []
        if root_vibe_hash:
            self.whitelist.append(root_vibe_hash)
        for node_hash in authorized_nodes:
            if node_hash and node_hash not in self.whitelist:
                self.whitelist.append(node_hash)

    def is_open_mode(self) -> bool:
        return len(self.whitelist) == 0

    def is_authorized(self, signature: str, data: str) -> bool:
        if not signature:
            return False
        for node_hash in self.whitelist:
            expected = hmac.new(
                node_hash.encode("utf-8"),
                data.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            if hmac.compare_digest(expected, signature):
                return True
        return False

    def is_node_authorized(self, node_hash: str) -> bool:
        if self.is_open_mode():
            return True
        return node_hash in self.whitelist

    def sign_payload(self, node_hash: str, data: str) -> str:
        return hmac.new(
            node_hash.encode("utf-8"),
            data.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def sign_message(self, node_hash: str, message: dict) -> dict:
        payload = json.dumps(message, sort_keys=True, separators=(",", ":"))
        signed = dict(message)
        signed["mesh_signature"] = self.sign_payload(node_hash, payload)
        signed["signer_hash"] = node_hash
        return signed

    def verify_message(self, message: dict) -> bool:
        signature = message.get("mesh_signature", "")
        signer = message.get("signer_hash", message.get("node", ""))
        if not signature or not signer:
            return self.is_open_mode()
        if not self.is_node_authorized(signer):
            return False
        unsigned = {k: v for k, v in message.items() if k not in ("mesh_signature", "signer_hash")}
        payload = json.dumps(unsigned, sort_keys=True, separators=(",", ":"))
        return self.is_authorized(signature, payload)
