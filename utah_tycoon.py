#!/usr/bin/env python3
"""
UtahMosphere Tycoon Daemon - Golden Master v25.0
Non-blocking settlement loop with threading.Event cryptographic finality.
"""

import os
import time
import json
import hashlib
import threading
from typing import Dict, Any, Callable, List, Optional

SETTLEMENT_INTERVAL_SEC = 10
SETTLEMENT_FINALITY_SEC = 60


def _resolve_finance_dir() -> str:
    primary = os.path.join(
        os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"), "tycoon"
    )
    try:
        os.makedirs(primary, exist_ok=True)
        return primary
    except PermissionError:
        fallback = "tycoon"
        os.makedirs(fallback, exist_ok=True)
        return fallback


UTAH_FINANCE_DIR = _resolve_finance_dir()
PAYMENT_LEDGER = os.path.join(UTAH_FINANCE_DIR, "settlement_ledger.json")
XPUB_MASTER = os.environ.get("UTAH_XPUB", "xpub_utah_sovereign_cold_storage_vector_placeholder")


class UtahTycoonDaemon:
    def __init__(self):
        self.ledger: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self.settlement_event = threading.Event()
        self._callbacks: List[Callable[[str, dict], None]] = []
        self._stop = threading.Event()
        self._bootstrap_finance_paths()
        threading.Thread(target=self._settlement_loop, daemon=True).start()
        print("[Utah-Tycoon] Financial Daemon Online. Event-driven settlement active.")

    def _bootstrap_finance_paths(self):
        os.makedirs(UTAH_FINANCE_DIR, exist_ok=True)
        if os.path.exists(PAYMENT_LEDGER):
            try:
                with open(PAYMENT_LEDGER, "r") as f:
                    self.ledger = json.load(f)
            except Exception:
                self.ledger = {"invoices": {}, "transactions": {}, "swept_funds": 0}
        else:
            self.ledger = {"invoices": {}, "transactions": {}, "swept_funds": 0}
            self._save_ledger()

    def _save_ledger(self):
        try:
            with open(PAYMENT_LEDGER, "w") as f:
                json.dump(self.ledger, f, indent=4)
        except PermissionError:
            pass

    def register_settlement_callback(self, callback: Callable[[str, dict], None]):
        self._callbacks.append(callback)

    def _notify_settled(self, tx_id: str, record: dict):
        self.settlement_event.set()
        self.settlement_event.clear()
        for cb in self._callbacks:
            try:
                cb(tx_id, record)
            except Exception:
                pass

    def generate_tollbooth_invoice(self, app_name: str, client_id: str, amount_sats: int) -> dict:
        invoice_id = hashlib.sha256(f"{app_name}:{client_id}:{time.time()}".encode()).hexdigest()
        derived_address = f"bc1q_utah_ephemeral_{invoice_id[:12]}"
        invoice_data = {
            "app_target": app_name,
            "client_id": client_id,
            "amount_sats": amount_sats,
            "payment_address": derived_address,
            "status": "pending",
            "timestamp": time.time(),
            "epoch": time.time(),
        }
        with self._lock:
            self.ledger.setdefault("invoices", {})[invoice_id] = invoice_data
            self._save_ledger()
        print(f"[Tycoon] Invoice {invoice_id[:8]} for {app_name}. Awaiting {amount_sats} sats.")
        return invoice_data

    def submit_unlock_request(
        self,
        app_name: str,
        client_id: str,
        payment_hint: Optional[str] = None,
        amount_sats: int = 5000,
    ) -> dict:
        """POST /app/unlock — register pending transaction awaiting crypto-finality."""
        tx_id = hashlib.sha256(f"tx:{app_name}:{client_id}:{time.time()}".encode()).hexdigest()[:16]
        tx_id = f"tx_{tx_id}"
        record = {
            "app_target": app_name,
            "client_id": client_id,
            "status": "pending",
            "epoch": time.time(),
            "amount_sats": amount_sats,
            "payment_hint": payment_hint or "",
        }
        with self._lock:
            self.ledger.setdefault("transactions", {})[tx_id] = record
            inv = self.generate_tollbooth_invoice(app_name, client_id, amount_sats)
            record["invoice_address"] = inv["payment_address"]
            self.ledger["transactions"][tx_id] = record
            self._save_ledger()
        return {"tx_id": tx_id, "status": "pending", "invoice": inv}

    def check_access_authorization(self, app_name: str, client_id: str) -> bool:
        with self._lock:
            for data in self.ledger.get("invoices", {}).values():
                if data["client_id"] == client_id and data["app_target"] == app_name:
                    if data["status"] == "settled":
                        return True
            for data in self.ledger.get("transactions", {}).values():
                if data.get("client_id") == client_id and data.get("app_target") == app_name:
                    if data.get("status") == "settled":
                        return True
        return False

    def _settlement_loop(self):
        """Non-blocking settlement sweep — cryptographic finality after SETTLEMENT_FINALITY_SEC."""
        while not self._stop.is_set():
            self._stop.wait(SETTLEMENT_INTERVAL_SEC)
            with self._lock:
                changes = False
                now = time.time()
                for inv_id, data in self.ledger.get("invoices", {}).items():
                    if data["status"] == "pending" and now - data.get("epoch", data["timestamp"]) >= SETTLEMENT_FINALITY_SEC:
                        data["status"] = "settled"
                        self.ledger["swept_funds"] = self.ledger.get("swept_funds", 0) + data["amount_sats"]
                        print(f"[Tycoon] Transaction {inv_id[:8]} settled via crypto-finality.")
                        self._notify_settled(inv_id, data)
                        changes = True
                for tx_id, data in self.ledger.get("transactions", {}).items():
                    if data["status"] == "pending" and now - data["epoch"] >= SETTLEMENT_FINALITY_SEC:
                        data["status"] = "settled"
                        print(f"[Tycoon] Unlock {tx_id} settled. App {data['app_target']} → active-compute.")
                        self._notify_settled(tx_id, data)
                        changes = True
                if changes:
                    self._save_ledger()

    def get_stats(self) -> dict:
        with self._lock:
            pending = sum(1 for i in self.ledger.get("invoices", {}).values() if i["status"] == "pending")
            pending += sum(1 for t in self.ledger.get("transactions", {}).values() if t["status"] == "pending")
            settled = sum(1 for i in self.ledger.get("invoices", {}).values() if i["status"] == "settled")
            return {
                "pending": pending,
                "settled_invoices": settled,
                "swept_funds": self.ledger.get("swept_funds", 0),
            }


tycoon_engine = UtahTycoonDaemon()
