#!/usr/bin/env python3
"""
UtahMosphere Hardware Attestation Guard (v27.0)
TPM 2.0 PCR verification for Genesis ISO and bootstrap provisioning.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

ATTESTATION_ENFORCE = os.environ.get("UTAH_ATTESTATION_ENFORCE", "1") != "0"
ATTESTATION_STORE = Path(
    os.environ.get(
        "UTAH_ATTESTATION_STORE",
        "/etc/utahmosphere/security/tpm_pcr0.txt",
    )
)
SEAL_MARKER = Path(
    os.environ.get(
        "UTAH_ATTESTATION_SEAL_MARKER",
        "/etc/utahmosphere/security/boot_sealed",
    )
)


class HardwareAttestation:
    """Verifies Genesis nodes run on genuine, provisioned hardware via TPM PCR0."""

    @staticmethod
    def read_pcr0() -> Optional[str]:
        try:
            result = subprocess.check_output(
                ["tpm2_pcrread", "sha256:0"],
                stderr=subprocess.DEVNULL,
                timeout=10,
            ).decode("utf-8", errors="replace")
            if "sha256:" in result.lower() or "0 :" in result:
                return result.strip()
            return None
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None

    @staticmethod
    def verify_tpm_identity() -> bool:
        """Return True when TPM PCR0 is readable (hardware root-of-trust present)."""
        pcr = HardwareAttestation.read_pcr0()
        if not pcr:
            return False
        return "sha256" in pcr.lower() or len(pcr) > 8

    @staticmethod
    def load_provisioned_pcr() -> Optional[str]:
        if ATTESTATION_STORE.is_file():
            return ATTESTATION_STORE.read_text(encoding="utf-8").strip()
        return None

    @staticmethod
    def provision_root_identity() -> bool:
        """Anchor current TPM PCR0 as the provisioned root identity."""
        pcr = HardwareAttestation.read_pcr0()
        if not pcr:
            return False
        ATTESTATION_STORE.parent.mkdir(parents=True, exist_ok=True)
        ATTESTATION_STORE.write_text(pcr, encoding="utf-8")
        if SEAL_MARKER.is_file():
            SEAL_MARKER.unlink(missing_ok=True)
        print("[Attestation] TPM PCR0 anchored as hardware root-of-trust.")
        return True

    @staticmethod
    def matches_provisioned_identity() -> bool:
        current = HardwareAttestation.read_pcr0()
        expected = HardwareAttestation.load_provisioned_pcr()
        if not current:
            return False
        if not expected:
            return True
        return current == expected

    @staticmethod
    def seal_boot_partition(install_root: str = "/opt/utahmosphere") -> None:
        """Mark boot as sealed and remove sovereign install payload."""
        SEAL_MARKER.parent.mkdir(parents=True, exist_ok=True)
        SEAL_MARKER.write_text("sealed:untrusted_hardware\n", encoding="utf-8")
        root = Path(install_root)
        if root.is_dir():
            for child in root.glob("*.py"):
                try:
                    child.unlink()
                except OSError:
                    pass
        print("[Attestation] Untrusted hardware detected. Boot partition sealed.")

    @staticmethod
    def enforce_or_exit(install_root: str = "/opt/utahmosphere") -> bool:
        """
        Bootstrap gate: verify TPM and provisioned identity.
        Returns True when install may proceed; exits process when enforcement fails.
        """
        if not ATTESTATION_ENFORCE:
            print("[Attestation] Enforcement disabled (UTAH_ATTESTATION_ENFORCE=0).")
            return True
        if SEAL_MARKER.is_file():
            print("[Attestation] Boot partition sealed. Refusing provisioning.")
            return False
        if not HardwareAttestation.verify_tpm_identity():
            print("[Attestation] TPM PCR0 unavailable.")
            HardwareAttestation.seal_boot_partition(install_root)
            return False
        expected = HardwareAttestation.load_provisioned_pcr()
        if expected is None:
            HardwareAttestation.provision_root_identity()
            return True
        if not HardwareAttestation.matches_provisioned_identity():
            print("[Attestation] Hardware identity mismatch. Sealing partition.")
            HardwareAttestation.seal_boot_partition(install_root)
            return False
        print("[Attestation] Hardware root-of-trust verified.")
        return True

    @staticmethod
    def status() -> dict:
        return {
            "tpm_present": HardwareAttestation.verify_tpm_identity(),
            "provisioned": ATTESTATION_STORE.is_file(),
            "sealed": SEAL_MARKER.is_file(),
            "enforce": ATTESTATION_ENFORCE,
        }


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        import json
        print(json.dumps(HardwareAttestation.status()))
        return 0
    return 0 if HardwareAttestation.enforce_or_exit() else 1


if __name__ == "__main__":
    sys.exit(main())
