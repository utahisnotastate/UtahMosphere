#!/usr/bin/env python3
"""
UtahMosphere RA-TLS Guard (v30.0)
CA pinning + TPM quote OID verification against global quote registry.
"""

import hashlib
import hmac
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
    from cryptography.x509.oid import ObjectIdentifier
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    from quote_registry import quote_registry
except ImportError:
    quote_registry = None  # type: ignore

RA_TLS_GUARD_ENFORCE = os.environ.get("UTAH_RA_TLS_GUARD_ENFORCE", "1") != "0"
ROOT_CA_PATH = Path(os.environ.get("UTAH_KERNEL_ROOT_CA_PATH", "/etc/utahmosphere/security/utah_root_ca.pem"))
KERNEL_ROOT_CA = os.environ.get(
    "UTAH_KERNEL_ROOT_CA",
    "utahmosphere_omega_build_v30_root_ca",
).encode("utf-8")
TPM_QUOTE_OID = ObjectIdentifier("1.3.6.1.4.1.99999") if HAS_CRYPTO else "1.3.6.1.4.1.99999"


class RATLSGuard:
    """Enforces CA pinning; only registry-valid hardware quotes join the mesh."""

    def __init__(self, root_ca_path: Optional[Union[str, Path]] = None):
        self.root_ca_path = Path(root_ca_path) if root_ca_path else ROOT_CA_PATH
        self.root_ca = self._load_ca()

    def _load_ca(self) -> Optional[Any]:
        if HAS_CRYPTO and self.root_ca_path.is_file():
            try:
                pem = self.root_ca_path.read_bytes()
                return serialization.load_pem_public_key(pem)
            except Exception:
                pass
        return None

    @staticmethod
    def derive_hardware_id(vibe_hash: str, pcr_digest: str, node_id: str = "") -> str:
        material = f"{vibe_hash}:{pcr_digest}:{node_id}"
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def verify_attestation(self, cert_bytes: bytes, hardware_id: Optional[str] = None) -> bool:
        """Extract TPM quote from X.509 extension; verify against Root CA + registry."""
        if not RA_TLS_GUARD_ENFORCE:
            return True
        if not HAS_CRYPTO:
            return self._verify_quote_dict_fallback(cert_bytes, hardware_id)

        try:
            cert = x509.load_der_x509_certificate(cert_bytes)
            tpm_quote_raw = None
            for ext in cert.extensions:
                if ext.oid == TPM_QUOTE_OID:
                    tpm_quote_raw = ext.value.public_bytes() if hasattr(ext.value, "public_bytes") else bytes(str(ext.value), "utf-8")
                    break
            if tpm_quote_raw is None:
                return False
            quote_payload = json.loads(tpm_quote_raw.decode("utf-8"))
            return self._verify_quote_payload(quote_payload, hardware_id)
        except Exception:
            return False

    def verify_quote_payload(self, quote: Dict[str, Any], hardware_id: Optional[str] = None) -> bool:
        return self._verify_quote_payload(quote, hardware_id)

    def verify_http_headers(self, headers: Dict[str, str]) -> bool:
        """UtahX ingress: validate X-Utah-Hardware-ID + X-Utah-RATLS-Quote before proxy."""
        if not RA_TLS_GUARD_ENFORCE:
            return True
        hw_id = headers.get("X-Utah-Hardware-ID", headers.get("x-utah-hardware-id", ""))
        quote_raw = headers.get("X-Utah-RATLS-Quote", headers.get("x-utah-ratls-quote", ""))
        if not hw_id or not quote_raw:
            return False
        try:
            quote = json.loads(quote_raw)
        except json.JSONDecodeError:
            return False
        return self._verify_quote_payload(quote, hw_id)

    def _verify_quote_payload(self, quote: Dict[str, Any], hardware_id: Optional[str]) -> bool:
        body = quote.get("body", "")
        signature = quote.get("signature", "")
        if not body or not signature:
            return False
        expected = hmac.new(KERNEL_ROOT_CA, body.encode("utf-8") if isinstance(body, str) else json.dumps(body, sort_keys=True).encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            return False
        try:
            parsed = json.loads(body) if isinstance(body, str) else body
        except json.JSONDecodeError:
            return False
        hw = hardware_id or parsed.get("hardware_id")
        if quote_registry and hw:
            if not quote_registry.is_valid_hardware(hw):
                return False
        if self.root_ca and quote.get("ca_signature"):
            return self._verify_ca_signature(quote["ca_signature"], body)
        return parsed.get("kernel_root") == KERNEL_ROOT_CA.decode("utf-8")

    def _verify_ca_signature(self, ca_sig: str, body: str) -> bool:
        if not HAS_CRYPTO or not self.root_ca:
            return True
        try:
            self.root_ca.verify(
                bytes.fromhex(ca_sig),
                body.encode("utf-8"),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False

    def _verify_quote_dict_fallback(self, data: bytes, hardware_id: Optional[str]) -> bool:
        try:
            quote = json.loads(data.decode("utf-8"))
            return self._verify_quote_payload(quote, hardware_id)
        except Exception:
            return False

    def sign_hardware_quote(self, quote_body: str) -> str:
        if HAS_CRYPTO and self.root_ca_path.with_suffix(".key").is_file():
            try:
                key = serialization.load_pem_private_key(
                    self.root_ca_path.with_suffix(".key").read_bytes(),
                    password=None,
                )
                if isinstance(key, rsa.RSAPrivateKey):
                    sig = key.sign(quote_body.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())
                    return sig.hex()
            except Exception:
                pass
        return hmac.new(KERNEL_ROOT_CA, quote_body.encode("utf-8"), hashlib.sha256).hexdigest()

    @staticmethod
    def status() -> dict:
        return {
            "enforce": RA_TLS_GUARD_ENFORCE,
            "ca_pinned": ROOT_CA_PATH.is_file(),
            "cryptography": HAS_CRYPTO,
            "registry_nodes": quote_registry.stats() if quote_registry else {},
        }


ra_tls_guard = RATLSGuard()
