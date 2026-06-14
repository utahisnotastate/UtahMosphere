#!/usr/bin/env python3
"""
UtahMosphere OS: Auto-Genesis Core Deployment [Omega-Release v25.0 Final]
Unified manifest: Golden Master Kernel, Tycoon, Swarm DHT, Utah-Flux UI.
"""

import os
import sys
import threading
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)


def deploy_sovereign_stack():
    print("[Genesis] Manifesting Sovereign Environment...")

    utah_data_dir = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
    for sub in ("containers", "utahx_mesh", "s3", "lambda", "rds", "tycoon", "swarm", "ota"):
        os.makedirs(os.path.join(utah_data_dir, sub), exist_ok=True)

    # Tycoon + Swarm initialize inside utahmosphere_master via imports;
    # pre-warm modules so settlement loop and DHT sockets bind early.
    print("[Genesis] Starting Tycoon Financial Engine...")
    import utah_tycoon  # noqa: F401

    print("[Genesis] Initializing Global Swarm DHT...")
    import utah_swarm_protocol  # noqa: F401

    print("[Genesis] Priming Golden Master Kernel Ingress...")
    kernel = subprocess.Popen([sys.executable, os.path.join(SCRIPT_DIR, "utahmosphere_master.py")], cwd=SCRIPT_DIR)

    print("[Genesis] Activating Utah-Flux UI...")
    gui = os.path.join(SCRIPT_DIR, "flux_gui.py")
    if os.path.exists(gui):
        try:
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
        print("CRITICAL: Auto-Genesis requires root hardware privileges.")
        sys.exit(1)

    proc = deploy_sovereign_stack()
    hold = threading.Event()
    try:
        hold.wait()
    except KeyboardInterrupt:
        print("[Genesis] Shutting down...")
        proc.terminate()
        sys.exit(0)
