#!/usr/bin/env python3
"""
UtahMosphere Reactive UI Framework - Lazarus Observer Build v21.0
Powered entirely by Utah-Flux engine rules. Automatically hooks onto 
the local kernel data streams to display system status without page refreshes.
"""

import os
import sys
import json
import time
import tkinter as tk
from tkinter import ttk

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
MANIFEST_PATH = os.path.join(UTAH_DATA_DIR, "flux_ui_manifest.json")

class UtahFluxDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UtahMosphere OS Control Interface")
        self.root.geometry("750x500")
        self.root.configure(bg="#0d0d12")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#0d0d12", foreground="#d1d1e0", font=("Courier", 12))
        
        self.create_reactive_widgets()
        self.loop_ui_update()

    def create_reactive_widgets(self):
        # Header Label Layer
        tk.Label(
            self.root, text="[ UTAHMOSPHERE OS CORE GRID INTERFACE ]",
            bg="#0d0d12", fg="#00ff66", font=("Courier", 16, "bold")
        ).pack(pady=20)
        
        # Reactive Data Containers Display Card
        self.frame = tk.Frame(self.root, bg="#1a1a24", bd=2, relief="groove")
        self.frame.pack(padx=30, pady=10, fill="both", expand=True)
        
        self.status_var = tk.StringVar(value="Connecting to ring-0 core...")
        self.workload_var = tk.StringVar(value="Workloads: 0")
        self.voice_var = tk.StringVar(value="Awaiting Formon Intent Input...")
        self.mutation_var = tk.StringVar(value="Lazarus Syntax Mutations: 0")
        
        tk.Label(self.frame, textvariable=self.status_var, bg="#1a1a24", fg="#ffffff", font=("Courier", 12)).pack(anchor="w", padx=20, pady=15)
        tk.Label(self.frame, textvariable=self.workload_var, bg="#1a1a24", fg="#33ccff", font=("Courier", 12)).pack(anchor="w", padx=20, pady=15)
        tk.Label(self.frame, textvariable=self.mutation_var, bg="#1a1a24", fg="#ff5555", font=("Courier", 12)).pack(anchor="w", padx=20, pady=15)
        tk.Label(self.frame, textvariable=self.voice_var, bg="#1a1a24", fg="#ffcc00", font=("Courier", 12), wraplength=650).pack(anchor="w", padx=20, pady=15)

    def loop_ui_update(self):
        """Observable variable state sync loop — updates layout when the file changes."""
        actual_manifest_path = MANIFEST_PATH
        if not os.path.exists(actual_manifest_path):
            # Fallback for local testing
            actual_manifest_path = "flux_ui_manifest.json"

        if os.path.exists(actual_manifest_path):
            try:
                with open(actual_manifest_path, "r") as f:
                    data = json.load(f)
                
                # Bind target values directly to variables
                self.status_var.set(f"System State: {data.get('node_status', 'Unknown')}")
                self.workload_var.set(f"Active Containers On Grid: {data.get('active_workloads', 0)}")
                self.mutation_var.set(f"Lazarus Syntax Mutations Applied: {data.get('mutation_count', 0)}")
                self.voice_var.set(f"Linguistic Input: '{data.get('last_voice_command', '')}'")
            except Exception:
                pass
                
        # Repeat sync loop every 250 milliseconds automatically
        self.root.after(250, self.loop_ui_update)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = UtahFluxDisplayApp(root)
        root.mainloop()
    except tk.TclError:
        print("Tkinter Error: No display found. Running in headless mode (no GUI).")
    except KeyboardInterrupt:
        sys.exit(0)
