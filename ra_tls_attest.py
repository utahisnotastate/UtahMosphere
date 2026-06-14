#!/usr/bin/env python3
"""
UtahMosphere RA-TLS Attestation (v31.0)
TPM quote verification + DHT majority-quorum before UtahNetes mesh gossip is accepted.
"""

import hashlib
import hmac
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from attestation_guard import HardwareAttestation
    from tpm_lock import TPMLocker
except ImportError:
    HardwareAttestation = None  # type: ignore
    TPMLocker = None  # type: ignore

RA_TLS_ENFORCE = os.environ.get("UTAH_RA_TLS_ENFORCE", "1") != "0"
KERNEL_ROOT_CA = os.environ.get(
    "UTAH_KERNEL_ROOT_CA",
    "utahmosphere_omega_build_v31_root_ca",
).encode("utf-8")
BUILD_ID = os.environ.get("UTAH_BUILD_ID", "omega-build-v31-federated-quorum")
QUOTE_STORE = Path(os.environ.get("UTAH_RA_TLS_QUOTE_DIR", "/etc/utahmosphere/security/ra_tls"))

try:
    from quote_registry import quote_registry
    from ra_tls_guard import RATLSGuard, ra_tls_guard
    from dht_quote_registry import dht_quote_registry
    from dht_consensus_engine import dht_consensus_engine
except ImportError:
    quote_registry = None  # type: ignore
    RATLSGuard = None  # type: ignore
    ra_tls_guard = None  # type: ignore
    dht_quote_registry = None  # type: ignore
    dht_consensus_engine = None  # type: ignore


class RATLSAttestation:
    """Verifies peer nodes present authentic TPM quotes before mesh sync."""

    EXTENSION_KEY = "ra_tls_quote"

    @staticmethod
    def generate_quote(
        node_id: str,
        build_id: str = BUILD_ID,
        vibe_hash: Optional[str] = None,
        hardware_id: Optional[str] = None,
    ) -> Dict[str, str]:
        pcr_digest = ""
        if HardwareAttestation:
            pcr = HardwareAttestation.read_pcr0() or ""
            pcr_digest = hashlib.sha256(pcr.encode("utf-8")).hexdigest()

        if RATLSGuard and vibe_hash and not hardware_id:
            hardware_id = RATLSGuard.derive_hardware_id(vibe_hash, pcr_digest, node_id)

        quote_body = json.dumps({
            "node_id": node_id,
            "hardware_id": hardware_id,
            "build": build_id,
            "pcr0_digest": pcr_digest,
            "vibe_hash": vibe_hash,
            "kernel_root": KERNEL_ROOT_CA.decode("utf-8"),
        }, sort_keys=True, separators=(",", ":"))

        signature = hmac.new(
            KERNEL_ROOT_CA,
            quote_body.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        quote = {"body": quote_body, "signature": signature}
        if ra_tls_guard:
            quote["ca_signature"] = ra_tls_guard.sign_hardware_quote(quote_body)

        if TPMLocker and TPMLocker._tpm_available():
            try:
                QUOTE_STORE.mkdir(parents=True, exist_ok=True)
                nonce = QUOTE_STORE / "quote.nonce"
                nonce.write_bytes(os.urandom(16))
                sig_path = QUOTE_STORE / "quote.sig"
                subprocess.run(
                    [
                        "tpm2_quote",
                        "-c", "0x81010001",
                        "-l", "sha256:0",
                        "-q", str(QUOTE_STORE / "quote.out"),
                        "-m", str(QUOTE_STORE / "quote.msg"),
                        "-g", str(nonce),
                        "-s", "ecc",
                        "-p", str(sig_path),
                    ],
                    capture_output=True,
                    timeout=15,
                )
                if sig_path.is_file():
                    quote["tpm_quote_sig"] = sig_path.read_bytes().hex()
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                pass

        return quote

    @staticmethod
    def verify_peer_quote(quote: Optional[Dict[str, Any]]) -> bool:
        if not quote:
            return not RA_TLS_ENFORCE
        body = quote.get("body")
        signature = quote.get("signature", "")
        if not body or not signature:
            return False
        expected = hmac.new(
            KERNEL_ROOT_CA,
            body.encode("utf-8") if isinstance(body, str) else json.dumps(body, sort_keys=True).encode(),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected, signature):
            return False
        try:
            parsed = json.loads(body) if isinstance(body, str) else body
        except json.JSONDecodeError:
            return False
        if parsed.get("kernel_root") != KERNEL_ROOT_CA.decode("utf-8"):
            return False
        hw_id = parsed.get("hardware_id")
        if quote_registry and hw_id and not quote_registry.is_valid_hardware(hw_id):
            return False
        peer_key = parsed.get("node_id") or hw_id or ""
        if dht_consensus_engine and peer_key and not dht_consensus_engine.verify_against_quorum(peer_key, quote):
            return False
        if dht_quote_registry and peer_key and not dht_quote_registry.verify_against_swarm(peer_key, quote):
            return False
        if ra_tls_guard and not ra_tls_guard.verify_quote_payload(quote, hw_id):
            return False
        if HardwareAttestation and parsed.get("pcr0_digest"):
            current_pcr = HardwareAttestation.read_pcr0() or ""
            current_digest = hashlib.sha256(current_pcr.encode("utf-8")).hexdigest()
            if RA_TLS_ENFORCE and parsed["pcr0_digest"] != current_digest:
                return False
        return True

    @staticmethod
    def verify_mesh_message(message: dict) -> bool:
        quote = message.get(RATLSAttestation.EXTENSION_KEY)
        if quote is None:
            return not RA_TLS_ENFORCE
        return RATLSAttestation.verify_peer_quote(quote)

    @staticmethod
    def attach_to_message(message: dict, node_id: str, vibe_hash: Optional[str] = None) -> dict:
        enriched = dict(message)
        enriched[RATLSAttestation.EXTENSION_KEY] = RATLSAttestation.generate_quote(
            node_id, vibe_hash=vibe_hash
        )
        if quote_registry:
            enriched["quote_registry"] = quote_registry.export_nodes()
        if dht_consensus_engine:
            enriched["quorum_consensus"] = dht_consensus_engine.export_consensus()
        if dht_quote_registry:
            enriched["dht_golden_registry"] = dht_quote_registry.export_golden()
        return enriched

    @staticmethod
    def status() -> dict:
        base = {
            "enforce": RA_TLS_ENFORCE,
            "kernel_root_ca": KERNEL_ROOT_CA.decode("utf-8"),
            "build": BUILD_ID,
        }
        if quote_registry:
            base["registry"] = quote_registry.stats()
        if dht_consensus_engine:
            base["quorum"] = dht_consensus_engine.stats()
        if dht_quote_registry:
            base["dht_federation"] = dht_quote_registry.stats()
        if ra_tls_guard:
            base["guard"] = RATLSGuard.status()
        return base
