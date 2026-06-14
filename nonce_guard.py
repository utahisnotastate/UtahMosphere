#!/usr/bin/env python3
"""
UtahMosphere Nonce-Guard (v26.0)
Prevents voice command replay attacks via monotonic nonce + HMAC binding.
"""

import os
import time
import hmac
import hashlib
import threading
from typing import Set

NONCE_WINDOW_SEC = int(os.environ.get("UTAH_NONCE_WINDOW_SEC", "30"))
NONCE_ENFORCE = os.environ.get("UTAH_NONCE_ENFORCE", "1") != "0"


class NonceGuard:
    def __init__(self, window_sec: int = NONCE_WINDOW_SEC):
        self.used_nonces: Set[int] = set()
        self.window_sec = window_sec
        self._lock = threading.Lock()

    def issue_nonce(self) -> int:
        return int(time.time())

    def _prune_stale(self, now: float):
        cutoff = int(now) - self.window_sec
        self.used_nonces = {n for n in self.used_nonces if n >= cutoff}

    @staticmethod
    def compute_signature(signing_key: str, nonce: int, transcript: str) -> str:
        payload = f"{nonce}:{transcript}"
        return hmac.new(
            signing_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def validate_and_process(
        self,
        transcript: str,
        nonce: int,
        signature: str,
        signing_key: str,
    ) -> bool:
        if not signature or not signing_key:
            return False
        now = time.time()
        with self._lock:
            if nonce in self.used_nonces:
                return False
            if abs(now - nonce) > self.window_sec:
                return False
            expected = self.compute_signature(signing_key, nonce, transcript)
            if not hmac.compare_digest(expected, signature):
                return False
            self.used_nonces.add(nonce)
            self._prune_stale(now)
            return True

    def enforcement_required(self, claimed: bool) -> bool:
        return NONCE_ENFORCE and claimed


nonce_guard = NonceGuard()
