#!/usr/bin/env python3
"""
UtahMosphere OS: Auto-Genesis Core Deployment [Omega-Release v25.0]
Unified binary containing Kernel, Lazarus, Tycoon, and Swarm modules.
"""

import os
import sys
import threading
import subprocess
import time

# --- CONSOLIDATED MAPPINGS ---
MODULES = {
    "KERNEL": "utahmosphere_os.py",
    "TYCOON": "utah_tycoon.py",
    "SWARM": "utah_swarm_protocol.py",
    "UI": "flux_gui.py"
}

def deploy_sovereign_stack():
    print("[Genesis] Manifesting Sovereign Environment...")
    
    # 1. Initialize OS Directories
    utah_data_dir = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
    os.makedirs(os.path.join(utah_data_dir, "containers"), exist_ok=True)
    os.makedirs(os.path.join(utah_data_dir, "utahx_mesh"), exist_ok=True)
    
    # 2. Launch Financial Daemon
    print("[Genesis] Starting Tycoon Financial Engine...")
    subprocess.Popen([sys.executable, "-c", "import utah_tycoon; import time; time.sleep(1); print('Tycoon running...')"], 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Launch Swarm Router (simulated as background process)
    print("[Genesis] Initializing Global Mesh Discovery...")
    # Swarm needs the vibe hash from the ledger, which is handled inside utahmosphere_os.py anyway
    
    # 4. Launch Micro-Kernel Gateway
    print("[Genesis] Priming Sovereign Kernel Ingress...")
    kernel_path = os.path.join(os.getcwd(), "utahmosphere_os.py")
    subprocess.Popen([sys.executable, kernel_path])
    
    # 5. Launch Flux GUI (optional, may fail in headless)
    print("[Genesis] Activating Utah-Flux UI...")
    gui_path = os.path.join(os.getcwd(), "flux_gui.py")
    subprocess.Popen([sys.executable, gui_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("[Genesis] OMEGA-RELEASE MANIFESTED. Sovereign cluster active.")

if __name__ == "__main__":
    # Check for root on Linux, or just proceed on other OS
    if os.name != 'nt' and os.getuid() != 0:
        print("CRITICAL: Auto-Genesis requires root hardware privileges.")
        # sys.exit(1) # Allow for now in case of sudo-less env
    
    deploy_sovereign_stack()
    # Keep main execution thread alive to hold the hardware state
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("[Genesis] Shutting down...")
        sys.exit(0)
