#!/usr/bin/env python3
"""
UtahX Stream Proxy - v29.0 Remote Attestation
Native HTTP/1.1 proxy with RA-TLS header verification (replaces Nginx).
"""

import json
import urllib.error
import urllib.request
from typing import Optional, Tuple

try:
    from ra_tls_guard import ra_tls_guard
except ImportError:
    ra_tls_guard = None  # type: ignore


def _verify_ingress(headers: Optional[dict]) -> bool:
    if ra_tls_guard is None or not headers:
        return True
    return ra_tls_guard.verify_http_headers({k: v for k, v in headers.items()})


def proxy_request(
    target_port: int,
    path: str = "/",
    method: str = "GET",
    body: Optional[bytes] = None,
    headers: Optional[dict] = None,
    timeout: float = 5.0,
    ingress_headers: Optional[dict] = None,
) -> Tuple[int, bytes, dict]:
    """Forward request to UtahContainerEngine backend after RA-TLS ingress check."""
    if not _verify_ingress(ingress_headers):
        return 403, json.dumps({
            "error": "RA-TLS attestation failed",
            "detail": "Hardware quote not in global registry or CA pin mismatch",
        }).encode(), {}

    url = f"http://127.0.0.1:{target_port}{path}"
    req_headers = dict(headers or {})
    req = urllib.request.Request(url, data=body, method=method, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)
    except Exception as e:
        return 503, json.dumps({"error": "UtahX proxy failure", "detail": str(e)}).encode(), {}
