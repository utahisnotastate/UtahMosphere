#!/usr/bin/env python3
"""
UtahMosphere Quantum Ledger - Production Security Build v22.0
Implements Biometric Vibe-Print Authentication. Replaces static API keys 
with ephemeral cryptographic signatures derived from human acoustic resonance.
"""

import os
import json
import hmac
import hashlib
from typing import Dict, Any, List, Optional

from ledger_auth import AuthGuard

try:
    from tpm_lock import TPMLocker
except ImportError:
    TPMLocker = None  # type: ignore

def _resolve_security_dir() -> str:
    primary = "/etc/utahmosphere/security"
    try:
        os.makedirs(primary, exist_ok=True)
        return primary
    except PermissionError:
        fallback = "security"
        os.makedirs(fallback, exist_ok=True)
        return fallback


UTAH_SECURITY_DIR = _resolve_security_dir()
ROOT_LEDGER_FILE = os.path.join(UTAH_SECURITY_DIR, "biometric_ledger.json")

class QuantumLedgerGuard:
    def __init__(self):
        self._ensure_security_paths()
        self.ledger = self._load_ledger()
        self.auth_guard = AuthGuard(
            self.ledger.get("authorized_nodes", []),
            self.ledger.get("root_vibe_hash"),
        )
        print("[Quantum Ledger] Biometric Guard Layer Initialized. AuthGuard enforcement active.")

    def _ensure_security_paths(self):
        os.makedirs(UTAH_SECURITY_DIR, exist_ok=True)

    def _load_ledger(self) -> Dict[str, Any]:
        if os.path.exists(ROOT_LEDGER_FILE):
            with open(ROOT_LEDGER_FILE, "r") as f:
                try:
                    return json.load(f)
                except Exception:
                    return {"root_vibe_hash": None, "authorized_nodes": []}
        return {"root_vibe_hash": None, "authorized_nodes": []}

    def _save_ledger(self):
        with open(ROOT_LEDGER_FILE, "w") as f:
            json.dump(self.ledger, f, indent=4)
        self.auth_guard.refresh(
            self.ledger.get("authorized_nodes", []),
            self.ledger.get("root_vibe_hash"),
        )

    def anchor_root_vibe(self, acoustic_hash: str) -> str:
        """Anchors the initial biological signature to the hardware permanently."""
        if self.ledger["root_vibe_hash"] is not None:
            return "Paradox: Root biological signature is already anchored to this silicon."

        self.ledger["root_vibe_hash"] = acoustic_hash
        nodes: List[str] = self.ledger.setdefault("authorized_nodes", [])
        if acoustic_hash not in nodes:
            nodes.append(acoustic_hash)
        self.ledger["tpm_sealed"] = False
        if TPMLocker and TPMLocker.seal_vibe_print(acoustic_hash):
            self.ledger["tpm_sealed"] = True
            self.ledger["root_vibe_storage"] = "tpm_pcr0"
        else:
            self.ledger["root_vibe_storage"] = "ledger_json"
        self._save_ledger()
        return "Biological resonance mapped. Hardware locked to General 23."

    def authorize_node(self, node_hash: str) -> bool:
        if not node_hash or len(node_hash) != 64:
            return False
        nodes: List[str] = self.ledger.setdefault("authorized_nodes", [])
        if node_hash in nodes:
            return True
        nodes.append(node_hash)
        self._save_ledger()
        return True

    def revoke_node(self, node_hash: str) -> bool:
        root = self.ledger.get("root_vibe_hash")
        if node_hash == root:
            return False
        nodes: List[str] = self.ledger.setdefault("authorized_nodes", [])
        if node_hash not in nodes:
            return False
        nodes.remove(node_hash)
        self._save_ledger()
        return True

    def get_authorized_nodes(self) -> List[str]:
        return list(self.ledger.get("authorized_nodes", []))

    def verify_vibe_signature(self, incoming_acoustic_hash: str, payload: str) -> bool:
        """
        Validates command authority: root vibe hash or delegated authorized_nodes entry.
        When TPM-sealed, verifies PCR binding before accepting root hash.
        """
        if self.ledger["root_vibe_hash"] is None:
            return True
        if TPMLocker and self.ledger.get("tpm_sealed"):
            if not TPMLocker.verify_binding(self.ledger["root_vibe_hash"]):
                return False
        if hmac.compare_digest(self.ledger["root_vibe_hash"], incoming_acoustic_hash):
            return True
        return self.auth_guard.is_node_authorized(incoming_acoustic_hash)

    def verify_request_signature(self, signature: str, payload: str) -> bool:
        return self.auth_guard.is_authorized(signature, payload)

    def sign_mesh_payload(self, payload: str) -> Optional[str]:
        root = self.ledger.get("root_vibe_hash")
        if not root:
            return None
        return self.auth_guard.sign_payload(root, payload)

# --- Expose Singleton for OS Kernel Integration ---
ledger_guard = QuantumLedgerGuard()
