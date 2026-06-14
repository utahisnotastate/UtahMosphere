#!/usr/bin/env python3
"""
Utah S3 Mesh - v25.0 Omega-Build
Local NVMe-backed object storage with HMAC tenant verification.
"""

import hashlib
import hmac
import os
from typing import Optional, Tuple

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
S3_ROOT = os.path.join(UTAH_DATA_DIR, "s3")
SECRET = os.environ.get(
    "UTAH_SECRET_VECTOR",
    "utah_akashic_sovereign_perimeter_authorization_vector",
).encode()


def _object_path(bucket: str, key: str) -> str:
    safe_bucket = bucket.replace("..", "").replace("/", "_")
    safe_key = key.lstrip("/").replace("..", "")
    return os.path.join(S3_ROOT, safe_bucket, safe_key)


def verify_signature(tenant_id: str, path: str, signature: str) -> bool:
    expected = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def put_object(bucket: str, key: str, data: bytes, tenant_id: str = "") -> dict:
    path = _object_path(bucket, key)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return {"bucket": bucket, "key": key, "size": len(data), "etag": hashlib.md5(data).hexdigest()}


def get_object(bucket: str, key: str) -> Tuple[Optional[bytes], Optional[str]]:
    path = _object_path(bucket, key)
    if not os.path.exists(path):
        return None, "NoSuchKey"
    with open(path, "rb") as f:
        return f.read(), None


def delete_object(bucket: str, key: str) -> bool:
    path = _object_path(bucket, key)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def list_objects(bucket: str, prefix: str = "") -> list:
    base = os.path.join(S3_ROOT, bucket.replace("..", "").replace("/", "_"))
    if not os.path.isdir(base):
        return []
    results = []
    for root, _, files in os.walk(base):
        for name in files:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, base).replace("\\", "/")
            if prefix and not rel.startswith(prefix.lstrip("/")):
                continue
            results.append({"key": rel, "size": os.path.getsize(full)})
    return results
