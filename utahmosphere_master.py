#!/usr/bin/env python3
"""
UtahMosphere OS - Master Kernel v30.0 [DHT-Federated Attestation & Drift Healing]
DHT golden consensus, PCR drift detection, emergency quarantine.
"""

import os
import sys

# Ensure install directory is on path when run from /opt/utahmosphere
_INSTALL = os.path.dirname(os.path.abspath(__file__))
if _INSTALL not in sys.path:
    sys.path.insert(0, _INSTALL)

from utahmosphere_os import run_master_server, SYSTEM_INGRESS_PORT, UTAH_DATA_DIR


def manifest_golden_master():
    print("[UtahMosphere] Triangle of Manifestation: CALIBRATED")
    print("[UtahMosphere] Photon Quenching: DISABLED")
    print("[UtahMosphere] Formon Injection: OMEGA-BUILD V30.0 FINALIZED")
    print(f"[UtahMosphere] Data root: {UTAH_DATA_DIR}")
    run_master_server(SYSTEM_INGRESS_PORT)


if __name__ == "__main__":
    manifest_golden_master()
