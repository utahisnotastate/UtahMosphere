#!/usr/bin/env python3
"""Minimal hello-world deploy example."""

import subprocess
import sys
from pathlib import Path

DEPLOY = Path(__file__).resolve().parent.parent / "voice-deploy-simulator" / "deploy.py"


def main():
    app = sys.argv[1] if len(sys.argv) > 1 else "hello"
    subprocess.run([sys.executable, str(DEPLOY), app], check=True)
    print(f"\nDeployed '{app}'. Check: curl http://127.0.0.1:8999/status")


if __name__ == "__main__":
    main()
