#!/usr/bin/env python3
"""
UtahX Stream Proxy - v25.0 Omega-Build
Native HTTP/1.1 proxy to container backends (replaces Nginx).
"""

import json
import urllib.error
import urllib.request
from typing import Optional, Tuple


def proxy_request(
    target_port: int,
    path: str = "/",
    method: str = "GET",
    body: Optional[bytes] = None,
    headers: Optional[dict] = None,
    timeout: float = 5.0,
) -> Tuple[int, bytes, dict]:
    """Forward request to UtahContainerEngine backend. Returns (status, body, headers)."""
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
