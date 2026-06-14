#!/usr/bin/env python3
"""
UtahMosphere PCR Drift Detector (v30.0)
Continuous TPM PCR0 monitoring; triggers emergency quarantine on kernel drift.
"""

import hashlib
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Any, Callable, Optional

DRIFT_ENFORCE = os.environ.get("UTAH_PCR_DRIFT_ENFORCE", "1") != "0"
DRIFT_INTERVAL_SEC = int(os.environ.get("UTAH_PCR_DRIFT_INTERVAL_SEC", "10"))
GOLDEN_PCR_PATH = Path(
    os.environ.get(
        "UTAH_GOLDEN_PCR_PATH",
        os.path.join(
            os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"),
            "golden_pcr0.txt",
        ),
    )
)

try:
    from attestation_guard import HardwareAttestation, ATTESTATION_STORE
except ImportError:
    HardwareAttestation = None  # type: ignore
    ATTESTATION_STORE = GOLDEN_PCR_PATH


class PCRDriftDetector:
    """Monitors PCR0; signals kernel quarantine when measurements drift."""

    def __init__(self):
        self._lock = threading.RLock()
        self._golden_digest: Optional[str] = None
        self._last_check: Optional[float] = None
        self._drift_detected = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._load_golden()

    @staticmethod
    def read_current_pcr() -> Optional[str]:
        if HardwareAttestation:
            return HardwareAttestation.read_pcr0()
        try:
            result = subprocess.check_output(
                ["tpm2_pcrread", "sha256:0"],
                stderr=subprocess.DEVNULL,
                timeout=10,
            ).decode("utf-8", errors="replace")
            return result.strip() if result else None
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None

    @staticmethod
    def digest_pcr(pcr_raw: Optional[str]) -> Optional[str]:
        if not pcr_raw:
            return None
        return hashlib.sha256(pcr_raw.encode("utf-8")).hexdigest()

    def _load_golden(self):
        golden_raw = None
        if ATTESTATION_STORE and Path(ATTESTATION_STORE).is_file():
            golden_raw = Path(ATTESTATION_STORE).read_text(encoding="utf-8").strip()
        elif GOLDEN_PCR_PATH.is_file():
            golden_raw = GOLDEN_PCR_PATH.read_text(encoding="utf-8").strip()
        if golden_raw:
            self._golden_digest = self.digest_pcr(golden_raw)
        else:
            current = self.read_current_pcr()
            if current:
                self._golden_digest = self.digest_pcr(current)
                self._persist_golden(current)

    def _persist_golden(self, pcr_raw: str):
        try:
            GOLDEN_PCR_PATH.parent.mkdir(parents=True, exist_ok=True)
            GOLDEN_PCR_PATH.write_text(pcr_raw, encoding="utf-8")
        except PermissionError:
            pass

    def anchor_golden(self, pcr_raw: Optional[str] = None) -> bool:
        raw = pcr_raw or self.read_current_pcr()
        if not raw:
            return False
        with self._lock:
            self._golden_digest = self.digest_pcr(raw)
            self._drift_detected = False
            self._persist_golden(raw)
        print("[PCRDrift] Golden PCR0 measurement anchored.")
        return True

    def is_expected(self, current_pcr: Optional[str] = None) -> bool:
        if not DRIFT_ENFORCE:
            return True
        raw = current_pcr or self.read_current_pcr()
        if not raw:
            return True
        digest = self.digest_pcr(raw)
        with self._lock:
            if not self._golden_digest:
                self._golden_digest = digest
                self._persist_golden(raw)
                return True
            return digest == self._golden_digest

    def check_once(self, on_drift: Optional[Callable[[], None]] = None) -> bool:
        current = self.read_current_pcr()
        self._last_check = time.time()
        if self.is_expected(current):
            return True
        with self._lock:
            self._drift_detected = True
        print("[Critical] PCR Drift Detected. Purging container silos.")
        if on_drift:
            on_drift()
        return False

    def monitor(self, kernel_ref: Any, interval: int = DRIFT_INTERVAL_SEC):
        def _loop():
            while not self._stop.is_set():
                if not self.is_expected():
                    print("[Critical] PCR Drift Detected. Purging container silos.")
                    with self._lock:
                        self._drift_detected = True
                    if hasattr(kernel_ref, "emergency_quarantine"):
                        kernel_ref.emergency_quarantine(reason="pcr_drift")
                self._last_check = time.time()
                self._stop.wait(interval)

        if self._monitor_thread and self._monitor_thread.is_alive():
            return
        self._monitor_thread = threading.Thread(target=_loop, daemon=True, name="pcr-drift")
        self._monitor_thread.start()
        print(f"[PCRDrift] Monitor online (interval {interval}s).")

    def stop(self):
        self._stop.set()

    def status(self) -> dict:
        with self._lock:
            return {
                "enforce": DRIFT_ENFORCE,
                "golden_set": bool(self._golden_digest),
                "drift_detected": self._drift_detected,
                "last_check": self._last_check,
                "interval_sec": DRIFT_INTERVAL_SEC,
            }


drift_detector = PCRDriftDetector()
