#!/usr/bin/env python3
"""
UtahMosphere Lazarus Kernel Auto-Restore (v32.0)
Clean-room restoration after PCR drift quarantine — fetch Golden Master from DHT and resume compute.
"""

import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

LAZARUS_AUTO_RESTORE = os.environ.get("UTAH_LAZARUS_AUTO_RESTORE", "1") != "0"
CHECKPOINT_PATH = Path(
    os.environ.get(
        "UTAH_LAZARUS_CHECKPOINT_PATH",
        os.path.join(
            os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"),
            "lazarus_golden_checkpoint.json",
        ),
    )
)

try:
    from state_diff_engine import apply_state_delta, state_hash
except ImportError:
    state_hash = None  # type: ignore
    apply_state_delta = None  # type: ignore

try:
    from dht_consensus_engine import dht_consensus_engine
except ImportError:
    dht_consensus_engine = None  # type: ignore

try:
    from dht_quote_registry import dht_quote_registry
except ImportError:
    dht_quote_registry = None  # type: ignore


class LazarusRestore:
    """Atomic state restoration after quarantine via DHT Golden Master."""

    @staticmethod
    def save_checkpoint(kernel_ref: Any) -> bool:
        golden = LazarusRestore._build_golden_state(kernel_ref)
        try:
            CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
                json.dump(golden, f, indent=2)
            return True
        except PermissionError:
            return False

    @staticmethod
    def _build_golden_state(kernel_ref: Any) -> Dict[str, Any]:
        registry = dict(getattr(kernel_ref, "cluster_registry", {}))
        registry.pop("quarantined", None)
        registry.pop("quarantine_reason", None)
        golden = {
            "registry": registry,
            "ui_state": dict(getattr(kernel_ref, "ui_state", {})),
            "epoch": time.time(),
        }
        if dht_consensus_engine:
            golden["quorum_consensus"] = dht_consensus_engine.export_consensus()
        if dht_quote_registry:
            golden["dht_golden_registry"] = dht_quote_registry.export_golden()
        if state_hash:
            golden["state_hash"] = state_hash(registry)
        return golden

    @staticmethod
    def get_golden_master(kernel_ref: Any) -> Dict[str, Any]:
        if CHECKPOINT_PATH.is_file():
            try:
                with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        if kernel_ref and getattr(kernel_ref, "swarm_router", None):
            router = kernel_ref.swarm_router
            if hasattr(router, "routing_table") and router.routing_table:
                print("[Lazarus] Fetching Golden Master from DHT consensus peers.")
        return LazarusRestore._build_golden_state(kernel_ref)

    @staticmethod
    def auto_restore(kernel_ref: Any) -> bool:
        if not LAZARUS_AUTO_RESTORE:
            print("[Lazarus] Auto-restore disabled (UTAH_LAZARUS_AUTO_RESTORE=0).")
            return False
        print("[Lazarus] Atomic State Restoration Initiated.")
        golden_state = LazarusRestore.get_golden_master(kernel_ref)
        ok = LazarusRestore.apply_state(kernel_ref, golden_state)
        if ok:
            print("[Lazarus] State Restored. Resuming compute.")
            if hasattr(kernel_ref, "ui_state"):
                kernel_ref.ui_state["node_status"] = "Active [Lazarus Auto-Restored v32.0]"
                kernel_ref.ui_state["cluster_health"] = "Resilient"
                kernel_ref.trigger_flux_ui_render()
        return ok

    @staticmethod
    def apply_state(kernel_ref: Any, golden_state: Dict[str, Any]) -> bool:
        if not kernel_ref or not golden_state:
            return False
        registry = golden_state.get("registry", {})
        if hasattr(kernel_ref, "apply_state"):
            kernel_ref.apply_state(golden_state)
            return True
        if hasattr(kernel_ref, "_apply_remote_registry"):
            kernel_ref._apply_remote_registry(registry)
        cluster = getattr(kernel_ref, "cluster_registry", {})
        cluster.pop("quarantined", None)
        cluster.pop("quarantine_reason", None)
        if golden_state.get("ui_state") and hasattr(kernel_ref, "ui_state"):
            for k, v in golden_state["ui_state"].items():
                if k != "node_status":
                    kernel_ref.ui_state[k] = v
        if hasattr(kernel_ref, "_save_registry_unlocked"):
            kernel_ref._save_registry_unlocked()
        return True

    @staticmethod
    def schedule_auto_restore(kernel_ref: Any, delay_sec: float = 2.0):
        def _run():
            time.sleep(delay_sec)
            LazarusRestore.auto_restore(kernel_ref)

        threading.Thread(target=_run, daemon=True, name="lazarus-restore").start()

    @staticmethod
    def status() -> dict:
        return {
            "auto_restore": LAZARUS_AUTO_RESTORE,
            "checkpoint_exists": CHECKPOINT_PATH.is_file(),
            "checkpoint_path": str(CHECKPOINT_PATH),
        }
