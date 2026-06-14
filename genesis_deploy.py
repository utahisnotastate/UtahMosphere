#!/usr/bin/env python3
"""
UtahMosphere OS: Auto-Genesis Core Deployment [Omega-Release v25.0]
Unified manifest: Kernel, Lazarus, Tycoon, Swarm, and Utah-Flux UI.
"""

import os
import sys
import threading
import subprocess
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES = {
    "KERNEL": "utahmosphere_master.py",
    "TYCOON": "utah_tycoon.py",
    "SWARM": "utah_swarm_protocol.py",
    "UI": "flux_gui.py",
}


def _popen_module(name: str, extra_env: dict = None):
    path = os.path.join(SCRIPT_DIR, MODULES[name])
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    return subprocess.Popen([sys.executable, path], cwd=SCRIPT_DIR, env=env)


def deploy_sovereign_stack():
    print("[Genesis] Manifesting Sovereign Environment...")

    utah_data_dir = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
    for sub in ("containers", "utahx_mesh", "s3", "lambda", "rds", "tycoon", "swarm"):
        os.makedirs(os.path.join(utah_data_dir, sub), exist_ok=True)

    print("[Genesis] Starting Tycoon Financial Engine...")
    subprocess.Popen(
        [sys.executable, "-c", "import utah_tycoon; import time; time.sleep(86400)"],
        cwd=SCRIPT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("[Genesis] Initializing Global Mesh Discovery...")
    root_hash = "0" * 64
    try:
        from quantum_ledger import ledger_guard
        if ledger_guard.ledger.get("root_vibe_hash"):
            root_hash = ledger_guard.ledger["root_vibe_hash"]
    except Exception:
        pass
    subprocess.Popen(
        [sys.executable, "-c", f"import utah_swarm_protocol; utah_swarm_protocol.UtahSwarmNode('{root_hash}'); import time; time.sleep(86400)"],
        cwd=SCRIPT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("[Genesis] Priming Golden Master Kernel Ingress...")
    kernel = _popen_module("KERNEL")

    print("[Genesis] Activating Utah-Flux UI...")
    try:
        gui = os.path.join(SCRIPT_DIR, MODULES["UI"])
        subprocess.Popen(
            [sys.executable, gui],
            cwd=SCRIPT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        print("[Genesis] Utah-Flux skipped (headless).")

    print("[Genesis] OMEGA-RELEASE MANIFESTED. Sovereign cluster active.")
    return kernel


if __name__ == "__main__":
    if os.name != "nt" and hasattr(os, "getuid") and os.getuid() != 0:
        print("[Genesis] Warning: root privileges recommended for production.")

    proc = deploy_sovereign_stack()
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("[Genesis] Shutting down...")
        proc.terminate()
        sys.exit(0)
