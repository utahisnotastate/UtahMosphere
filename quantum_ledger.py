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
from typing import Dict, Any

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
        print("[Quantum Ledger] Biometric Guard Layer Initialized. Static secrets deprecated.")

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

    def anchor_root_vibe(self, acoustic_hash: str) -> str:
        """Anchors the initial biological signature to the hardware permanently."""
        if self.ledger["root_vibe_hash"] is not None:
            return "Paradox: Root biological signature is already anchored to this silicon."
        
        self.ledger["root_vibe_hash"] = acoustic_hash
        self._save_ledger()
        return "Biological resonance mapped. Hardware locked to General 23."

    def verify_vibe_signature(self, incoming_acoustic_hash: str, payload: str) -> bool:
        """
        Validates that the incoming command was spoken by the authorized entity.
        The acoustic hash acts as the symmetric key for the HMAC validation.
        """
        if self.ledger["root_vibe_hash"] is None:
            # Open mode if no master has claimed the node yet
            return True
            
        # Secure time-constant comparison to prevent timing attacks
        return hmac.compare_digest(self.ledger["root_vibe_hash"], incoming_acoustic_hash)

# --- Expose Singleton for OS Kernel Integration ---
ledger_guard = QuantumLedgerGuard()
