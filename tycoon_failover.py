#!/usr/bin/env python3
"""
Utah-Tycoon: Multi-Region Mempool Failover (v27.0)
Queries US / EU / ASIA mempool endpoints with silent regional failover.
"""

import json
import os
import urllib.request
from typing import List, Optional, Tuple

DEFAULT_NODES = [
    "https://mempool.space/api",
    "https://mempool.space/signet/api",
    "https://blockstream.info/api",
]

MEMPOOL_NODES: List[str] = [
    n.strip().rstrip("/")
    for n in os.environ.get("UTAH_MEMPOOL_NODES", "").split(",")
    if n.strip()
] or DEFAULT_NODES

FAILOVER_TIMEOUT_SEC = float(os.environ.get("UTAH_MEMPOOL_FAILOVER_TIMEOUT", "2"))


class MempoolFailover:
    NODES = MEMPOOL_NODES

    @staticmethod
    def get_status_with_failover(address: str) -> Tuple[bool, Optional[str]]:
        """Return (paid, winning_node_url)."""
        if not address:
            return False, None
        for node in MempoolFailover.NODES:
            try:
                url = f"{node}/address/{address}/txs"
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "UtahMosphere-Tycoon/27.0"},
                )
                with urllib.request.urlopen(req, timeout=FAILOVER_TIMEOUT_SEC) as resp:
                    if resp.status != 200:
                        continue
                    txs = json.loads(resp.read().decode("utf-8"))
                    if isinstance(txs, list) and len(txs) > 0:
                        return True, node
            except Exception:
                continue
        return False, None

    @staticmethod
    def node_regions() -> List[str]:
        return list(MempoolFailover.NODES)
