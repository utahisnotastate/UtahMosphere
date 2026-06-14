#!/usr/bin/env python3
"""
Utah-Tycoon: Multi-Region Mempool Failover (v28.0)
Queries US / EU / global / Oceania mempool endpoints with silent failover.
"""

import json
import os
import urllib.request
from typing import List, Optional, Tuple

DEFAULT_NODES = [
    "https://mempool.space/api",            # Global / US
    "https://mempool.space/signet/api",     # EU
    "https://blockstream.info/api",         # Global
    "https://mempool.space/testnet/api",    # APAC / Oceania designated endpoint
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
                    headers={"User-Agent": "UtahMosphere-Tycoon/28.0"},
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
    def node_regions() -> List[dict]:
        labels = ["us-global", "eu-signet", "global-blockstream", "oceania-apac"]
        return [
            {"region": labels[i] if i < len(labels) else f"node-{i}", "url": url}
            for i, url in enumerate(MempoolFailover.NODES)
        ]
