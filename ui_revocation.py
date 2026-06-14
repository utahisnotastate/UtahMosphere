#!/usr/bin/env python3
"""
Utah-Flux Revocation Panel (v26.0)
Administrative UI for authorized_nodes[] mesh governance.
"""

import json
import os
import urllib.error
import urllib.request
from typing import Callable, List, Optional

import tkinter as tk

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
REGISTRY_PATH = os.path.join(UTAH_DATA_DIR, "secure_registry.json")
KERNEL_URL = os.environ.get("UTAH_FLUX_KERNEL_URL", "http://127.0.0.1:8999")


class RevocationPanel:
    """Renders authorized node list with revoke actions."""

    def __init__(
        self,
        parent: tk.Misc,
        get_nodes: Callable[[], List[str]],
        on_revoke: Callable[[str], None],
        bg: str = "#1a1a24",
    ):
        self.parent = parent
        self.get_nodes = get_nodes
        self.on_revoke = on_revoke
        self.bg = bg
        self._rows_frame = tk.Frame(parent, bg=bg)
        self._rows_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def refresh(self):
        for child in self._rows_frame.winfo_children():
            child.destroy()
        nodes = self.get_nodes()
        if not nodes:
            tk.Label(
                self._rows_frame,
                text="No delegated nodes in authorized_nodes[].",
                bg=self.bg,
                fg="#888899",
                font=("Courier", 10),
            ).pack(anchor="w", pady=4)
            return
        for node_hash in nodes:
            self._render_row(node_hash)

    def _render_row(self, node_hash: str):
        row = tk.Frame(self._rows_frame, bg=self.bg)
        row.pack(fill="x", pady=5)
        tk.Label(
            row,
            text=f"Node: {node_hash[:12]}...",
            bg=self.bg,
            fg="#ffffff",
            font=("Courier", 10),
        ).pack(side="left")
        btn = tk.Button(
            row,
            text="Revoke",
            bg="#cc0000",
            fg="white",
            font=("Courier", 9, "bold"),
            command=lambda h=node_hash: self._revoke(h),
        )
        btn.pack(side="right")

    def _revoke(self, node_hash: str):
        self.on_revoke(node_hash)
        self.refresh()


def load_authorized_nodes() -> List[str]:
    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return list(data.get("authorized_nodes", []))
        except Exception:
            pass
    manifest = os.path.join(UTAH_DATA_DIR, "flux_ui_manifest.json")
    if os.path.exists(manifest):
        try:
            with open(manifest, "r", encoding="utf-8") as f:
                data = json.load(f)
            return list(data.get("authorized_nodes", []))
        except Exception:
            pass
    return []


def revoke_via_api(node_hash: str, acoustic_hash: str, base_url: str = KERNEL_URL) -> bool:
    payload = json.dumps({
        "node_hash": node_hash,
        "acoustic_hash": acoustic_hash,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/admin/revoke-node",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except urllib.error.HTTPError:
        return False
    except Exception:
        return False
