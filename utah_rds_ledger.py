#!/usr/bin/env python3
"""
Utah RDS Ledger - v25.0 Omega-Build
Distributed consensus key-value store (local ledger file).
"""

import json
import os
import threading
import time
from typing import Any, Optional

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
RDS_FILE = os.path.join(UTAH_DATA_DIR, "rds", "ledger.json")
_lock = threading.Lock()


def _ensure_store():
    os.makedirs(os.path.dirname(RDS_FILE), exist_ok=True)
    if not os.path.exists(RDS_FILE):
        with open(RDS_FILE, "w") as f:
            json.dump({"records": {}, "epoch": time.time()}, f)


def _load() -> dict:
    _ensure_store()
    with open(RDS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"records": {}, "epoch": time.time()}


def _save(data: dict):
    data["epoch"] = time.time()
    with open(RDS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def write(key: str, value: Any) -> dict:
    with _lock:
        data = _load()
        data["records"][key] = value
        _save(data)
    return {"key": key, "status": "written", "epoch": data["epoch"]}


def read(key: str) -> Optional[Any]:
    data = _load()
    return data["records"].get(key)


def read_all(prefix: str = "") -> dict:
    data = _load()
    if not prefix:
        return data["records"]
    return {k: v for k, v in data["records"].items() if k.startswith(prefix)}


def delete(key: str) -> bool:
    with _lock:
        data = _load()
        if key in data["records"]:
            del data["records"][key]
            _save(data)
            return True
    return False
