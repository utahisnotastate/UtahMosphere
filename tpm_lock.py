#!/usr/bin/env python3
"""
UtahMosphere TPM Locker (v28.0)
Seals Vibe-Print hash to TPM PCR0 — unseal fails on hardware/kernel tamper.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

try:
    from attestation_guard import HardwareAttestation, ATTESTATION_STORE
except ImportError:
    HardwareAttestation = None  # type: ignore
    ATTESTATION_STORE = Path("/etc/utahmosphere/security/tpm_pcr0.txt")

TPM_LOCK_ENFORCE = os.environ.get("UTAH_TPM_LOCK_ENFORCE", "1") != "0"
SECURITY_DIR = Path(os.environ.get("UTAH_TPM_SECURITY_DIR", "/etc/utahmosphere/security/tpm_seal"))
VIBE_INPUT = SECURITY_DIR / "vibe_seal_input.bin"
SEALED_CTX = SECURITY_DIR / "pcr.ctx"
SEALED_PUB = SECURITY_DIR / "vibe.pub"
SEALED_PRIV = SECURITY_DIR / "vibe.priv"
SEALED_MARKER = SECURITY_DIR / "vibe_tpm_sealed"
FALLBACK_SEAL = SECURITY_DIR / "vibe_sealed_fallback.bin"


class TPMLocker:
    """Seals the Vibe-Print hash to TPM PCR0 (Static Root of Trust for Measurement)."""

    @staticmethod
    def _tpm_available() -> bool:
        if HardwareAttestation is None:
            return False
        return HardwareAttestation.verify_tpm_identity()

    @staticmethod
    def seal_vibe_print(vibe_hash: str) -> bool:
        if not vibe_hash or len(vibe_hash) != 64:
            return False
        SECURITY_DIR.mkdir(parents=True, exist_ok=True)
        VIBE_INPUT.write_bytes(vibe_hash.encode("utf-8"))

        if TPMLocker._tpm_available():
            try:
                subprocess.run(
                    ["tpm2_createprimary", "-C", "o", "-g", "sha256", "-G", "rsa", "-c", str(SEALED_CTX)],
                    check=True,
                    capture_output=True,
                    timeout=30,
                )
                subprocess.run(
                    [
                        "tpm2_create",
                        "-C", str(SEALED_CTX),
                        "-u", str(SEALED_PUB),
                        "-r", str(SEALED_PRIV),
                        "-L", "sha256:0",
                        "-i", str(VIBE_INPUT),
                    ],
                    check=True,
                    capture_output=True,
                    timeout=30,
                )
                SEALED_MARKER.write_text("tpm_sealed:pcr0\n", encoding="utf-8")
                try:
                    VIBE_INPUT.unlink(missing_ok=True)
                except OSError:
                    pass
                print("[TPM-Lock] Vibe-Print sealed to PCR0.")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
                print(f"[TPM-Lock] tpm2 seal failed: {exc}")

        if not TPM_LOCK_ENFORCE:
            FALLBACK_SEAL.write_bytes(vibe_hash.encode("utf-8"))
            SEALED_MARKER.write_text("fallback_sealed\n", encoding="utf-8")
            print("[TPM-Lock] Vibe-Print sealed (fallback mode, UTAH_TPM_LOCK_ENFORCE=0).")
            return True
        return False

    @staticmethod
    def unseal_vibe_print() -> Optional[str]:
        if not SEALED_MARKER.is_file():
            return None
        if HardwareAttestation and not HardwareAttestation.matches_provisioned_identity():
            print("[TPM-Lock] PCR0 mismatch. Unseal refused.")
            return None

        marker = SEALED_MARKER.read_text(encoding="utf-8").strip()
        if marker.startswith("tpm_sealed") and SEALED_CTX.is_file() and SEALED_PRIV.is_file():
            try:
                out = subprocess.check_output(
                    [
                        "tpm2_load",
                        "-C", str(SEALED_CTX),
                        "-u", str(SEALED_PUB),
                        "-r", str(SEALED_PRIV),
                        "-c", str(SECURITY_DIR / "vibe_load.ctx"),
                    ],
                    stderr=subprocess.DEVNULL,
                    timeout=30,
                )
                del out
                raw = subprocess.check_output(
                    ["tpm2_unseal", "-c", str(SECURITY_DIR / "vibe_load.ctx")],
                    stderr=subprocess.DEVNULL,
                    timeout=30,
                )
                return raw.decode("utf-8").strip()
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                if TPM_LOCK_ENFORCE:
                    return None

        if FALLBACK_SEAL.is_file() and not TPM_LOCK_ENFORCE:
            return FALLBACK_SEAL.read_text(encoding="utf-8").strip()
        return None

    @staticmethod
    def verify_binding(expected_hash: Optional[str] = None) -> bool:
        unsealed = TPMLocker.unseal_vibe_print()
        if unsealed is None:
            return not TPM_LOCK_ENFORCE or not SEALED_MARKER.is_file()
        if expected_hash:
            return unsealed == expected_hash
        return len(unsealed) == 64

    @staticmethod
    def status() -> dict:
        return {
            "sealed": SEALED_MARKER.is_file(),
            "tpm_seal": SEALED_MARKER.read_text(encoding="utf-8").strip() if SEALED_MARKER.is_file() else None,
            "enforce": TPM_LOCK_ENFORCE,
            "binding_ok": TPMLocker.verify_binding(),
        }
