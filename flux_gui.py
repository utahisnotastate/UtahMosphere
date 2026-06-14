#!/usr/bin/env python3
"""
UtahMosphere Reactive UI Framework - Utah-Flux v26.0
Status dashboard + authorized node revocation panel.
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from ui_revocation import RevocationPanel, load_authorized_nodes, revoke_via_api

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
MANIFEST_PATH = os.path.join(UTAH_DATA_DIR, "flux_ui_manifest.json")
KERNEL_URL = os.environ.get("UTAH_FLUX_KERNEL_URL", "http://127.0.0.1:8999")


class UtahFluxDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UtahMosphere OS Control Interface v26.0")
        self.root.geometry("800x620")
        self.root.configure(bg="#0d0d12")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#0d0d12", foreground="#d1d1e0", font=("Courier", 12))

        self._authorized_nodes: list = []
        self.create_reactive_widgets()
        self.loop_ui_update()

    def create_reactive_widgets(self):
        tk.Label(
            self.root, text="[ UTAHMOSPHERE OS CORE GRID INTERFACE ]",
            bg="#0d0d12", fg="#00ff66", font=("Courier", 16, "bold")
        ).pack(pady=15)

        self.frame = tk.Frame(self.root, bg="#1a1a24", bd=2, relief="groove")
        self.frame.pack(padx=30, pady=8, fill="both", expand=True)

        self.status_var = tk.StringVar(value="Connecting to ring-0 core...")
        self.workload_var = tk.StringVar(value="Workloads: 0")
        self.voice_var = tk.StringVar(value="Awaiting Formon Intent Input...")
        self.mutation_var = tk.StringVar(value="Lazarus Syntax Mutations: 0")
        self.nodes_var = tk.StringVar(value="Authorized Nodes: 0")

        tk.Label(self.frame, textvariable=self.status_var, bg="#1a1a24", fg="#ffffff", font=("Courier", 12)).pack(anchor="w", padx=20, pady=10)
        tk.Label(self.frame, textvariable=self.workload_var, bg="#1a1a24", fg="#33ccff", font=("Courier", 12)).pack(anchor="w", padx=20, pady=10)
        tk.Label(self.frame, textvariable=self.mutation_var, bg="#1a1a24", fg="#ff5555", font=("Courier", 12)).pack(anchor="w", padx=20, pady=10)
        tk.Label(self.frame, textvariable=self.voice_var, bg="#1a1a24", fg="#ffcc00", font=("Courier", 12), wraplength=700).pack(anchor="w", padx=20, pady=10)
        tk.Label(self.frame, textvariable=self.nodes_var, bg="#1a1a24", fg="#aa88ff", font=("Courier", 12)).pack(anchor="w", padx=20, pady=5)

        revoke_header = tk.Label(
            self.root, text="[ AUTHORIZED NODE REVOCATION PANEL ]",
            bg="#0d0d12", fg="#ff6666", font=("Courier", 12, "bold")
        )
        revoke_header.pack(pady=(10, 0))

        self.revoke_frame = tk.Frame(self.root, bg="#1a1a24", bd=2, relief="groove")
        self.revoke_frame.pack(padx=30, pady=10, fill="both", expand=True)

        self.revocation_panel = RevocationPanel(
            self.revoke_frame,
            get_nodes=lambda: self._authorized_nodes,
            on_revoke=self._handle_revoke,
        )

    def _handle_revoke(self, node_hash: str):
        acoustic_hash = os.environ.get("UTAH_FLUX_ACOUSTIC_HASH", "")
        if not acoustic_hash:
            acoustic_hash = simpledialog.askstring(
                "Root Vibe Required",
                "Enter 64-char root acoustic_hash to authorize revocation:",
                parent=self.root,
            ) or ""
        if len(acoustic_hash) != 64:
            messagebox.showerror("Revocation Failed", "Valid root acoustic_hash required.")
            return
        if revoke_via_api(node_hash, acoustic_hash, KERNEL_URL):
            self._authorized_nodes = [n for n in self._authorized_nodes if n != node_hash]
            messagebox.showinfo("Revoked", f"Node {node_hash[:12]}... removed from mesh.")
        else:
            messagebox.showerror("Revocation Failed", "Kernel rejected revocation request.")

    def loop_ui_update(self):
        actual_manifest_path = MANIFEST_PATH
        if not os.path.exists(actual_manifest_path):
            actual_manifest_path = "flux_ui_manifest.json"

        if os.path.exists(actual_manifest_path):
            try:
                with open(actual_manifest_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.status_var.set(f"System State: {data.get('node_status', 'Unknown')}")
                self.workload_var.set(f"Active Containers On Grid: {data.get('active_workloads', 0)}")
                self.mutation_var.set(f"Lazarus Syntax Mutations Applied: {data.get('mutation_count', 0)}")
                self.voice_var.set(f"Linguistic Input: '{data.get('last_voice_command', '')}'")
                nodes = data.get("authorized_nodes") or load_authorized_nodes()
                self._authorized_nodes = list(nodes)
                self.nodes_var.set(f"Authorized Nodes: {len(self._authorized_nodes)}")
                self.revocation_panel.refresh()
            except Exception:
                pass

        self.root.after(250, self.loop_ui_update)


if __name__ == "__main__":
    root = tk.Tk()
    try:
        UtahFluxDisplayApp(root)
        root.mainloop()
    except tk.TclError:
        print("Tkinter Error: No display found. Running in headless mode (no GUI).")
    except KeyboardInterrupt:
        sys.exit(0)
