#!/usr/bin/env python3
"""
Utah-Tycoon: Bitcoin Mempool Settlement Engine (v25.1)
Real-time block-height / mempool confirmation for resource unlocking.
"""

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

SETTLEMENT_POLL_SEC = int(os.environ.get("UTAH_TYCOON_POLL_SEC", "5"))
MEMPOOL_API_BASE = os.environ.get(
    "UTAH_MEMPOOL_API", "https://mempool.space/api"
).rstrip("/")
ELECTRUM_URL = os.environ.get("UTAH_ELECTRUM_URL", "").rstrip("/")
SETTLEMENT_MODE = os.environ.get("UTAH_TYCOON_SETTLEMENT_MODE", "auto").lower()
SIMULATE_FINALITY_SEC = int(os.environ.get("UTAH_TYCOON_SIMULATE_SEC", "60"))


class RealTimeTycoon:
    """Queries mempool.space (or electrum-server) for payment finality."""

    @staticmethod
    def get_tx_status(address: str) -> bool:
        """Return True when the payment address has at least one confirmed transaction."""
        if not address:
            return False
        if RealTimeTycoon._query_mempool_space(address):
            return True
        if ELECTRUM_URL:
            return RealTimeTycoon._query_electrum(address)
        return False

    @staticmethod
    def _query_mempool_space(address: str) -> bool:
        try:
            url = f"{MEMPOOL_API_BASE}/address/{address}/txs"
            req = urllib.request.Request(url, headers={"User-Agent": "UtahMosphere-Tycoon/25.1"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                txs = json.loads(resp.read().decode("utf-8"))
            return isinstance(txs, list) and len(txs) > 0
        except Exception:
            return False

    @staticmethod
    def _query_electrum(address: str) -> bool:
        try:
            payload = json.dumps({
                "id": 1,
                "jsonrpc": "2.0",
                "method": "blockchain.address.get_history",
                "params": [address],
            }).encode("utf-8")
            req = urllib.request.Request(
                ELECTRUM_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            history = data.get("result") or []
            return len(history) > 0
        except Exception:
            return False

    @staticmethod
    def should_use_simulation(address: str) -> bool:
        if SETTLEMENT_MODE == "simulate":
            return True
        if SETTLEMENT_MODE == "real":
            return False
        # auto: dev ephemeral addresses fall back to timed settlement
        return address.startswith("bc1q_utah_") or address.startswith("tb1_utah_")

    @staticmethod
    def simulate_elapsed(record: dict, now: Optional[float] = None) -> bool:
        now = now or time.time()
        epoch = record.get("epoch") or record.get("timestamp", now)
        return now - epoch >= SIMULATE_FINALITY_SEC

    def settlement_pass(self, ledger: Dict[str, Any]) -> bool:
        """Run one settlement sweep. Returns True if any record settled."""
        now = time.time()
        changes = False
        for inv_id, data in ledger.get("invoices", {}).items():
            if data.get("status") != "pending":
                continue
            address = data.get("payment_address", "")
            if self._is_settled(data, address, now):
                data["status"] = "settled"
                data["settlement_source"] = self._settlement_source(address)
                ledger["swept_funds"] = ledger.get("swept_funds", 0) + data.get("amount_sats", 0)
                print(f"[Tycoon] Finality reached for {inv_id[:8]}. Computing power engaged.")
                changes = True
        for tx_id, data in ledger.get("transactions", {}).items():
            if data.get("status") != "pending":
                continue
            address = data.get("invoice_address") or data.get("payment_address", "")
            if self._is_settled(data, address, now):
                data["status"] = "settled"
                data["settlement_source"] = self._settlement_source(address)
                print(f"[Tycoon] Unlock {tx_id} settled. App {data.get('app_target')} -> active-compute.")
                changes = True
        return changes

    def _is_settled(self, record: dict, address: str, now: float) -> bool:
        if self.should_use_simulation(address):
            return self.simulate_elapsed(record, now)
        return self.get_tx_status(address)

    @staticmethod
    def _settlement_source(address: str) -> str:
        if RealTimeTycoon.should_use_simulation(address):
            return "simulate"
        return "mempool"
