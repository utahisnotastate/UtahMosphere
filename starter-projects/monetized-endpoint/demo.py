#!/usr/bin/env python3
"""End-to-end monetized endpoint demo."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEPLOY = ROOT / "examples" / "voice-deploy-simulator" / "deploy.py"
ACCESS = ROOT / "examples" / "paid-app-access" / "access_app.py"
HANDLER = Path(__file__).parent / "handler.py"


def main():
    app = "premium-api"
    subprocess.run([sys.executable, str(DEPLOY), app], check=True)
    data_dir = ROOT / ".utah-data" / "containers" / app
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "handler.py").write_text(HANDLER.read_text())
    print(f"Handler copied to {data_dir}")
    subprocess.run([sys.executable, str(ACCESS), app, "premium-client"])


if __name__ == "__main__":
    main()
