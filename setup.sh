#!/usr/bin/env bash
# ==============================================================================
# UtahMosphere Auto-Genesis Provisioning Engine (v25.0)
# Target: Sovereign Edge Hardware (Pi, M5Stack, SBC, x86 Mini PC)
# Final State: Zero-Manual-Management Cloud Node
# Protocol: Pure Privilege Zero Layer Infrastructure Setup
# ==============================================================================

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
   echo "CRITICAL error: This environment configuration tool requires root access parameters." 1>&2
   exit 1
fi

echo "[Omega-Genesis] Wiping Legacy World-A Residue..."
# Stop and remove legacy container engines and proxies (if they exist)
systemctl stop docker || true
systemctl stop nginx || true
apt-get purge -y docker.io docker-compose nginx || true
apt-get autoremove -y || true

echo "[Omega-Genesis] Installing Sovereign Infrastructure Dependencies..."
apt-get update -y
apt-get install -y python3 python3-pip python3-tk libasound2-dev portaudio19-dev curl git

# Install Python requirements
pip3 install numpy librosa SpeechRecognition pyaudio

echo "[Omega-Genesis] Synthesizing baseline data paths natively..."
mkdir -p "/var/lib/utahmosphere/containers"
mkdir -p "/etc/utahmosphere/utahx_mesh"
mkdir -p "/var/lib/utahmosphere/apps"

# Inject the platform daemon engine unit service parameters
cat << 'EOF' > /etc/systemd/system/utahmosphere.service
[Unit]
Description=UtahMosphere Omega-Genesis Core
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/lib/utahmosphere
ExecStart=/usr/bin/python3 /usr/local/bin/utah-genesis
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=utahmosphere

[Install]
WantedBy=multi-user.target
EOF

# Move scripts to local bin
cp ./utahmosphere_os.py /usr/local/bin/
cp ./utah_tycoon.py /usr/local/bin/
cp ./utah_swarm_protocol.py /usr/local/bin/
cp ./quantum_ledger.py /usr/local/bin/
cp ./flux_gui.py /usr/local/bin/
cp ./genesis_deploy.py /usr/local/bin/utah-genesis
chmod +x /usr/local/bin/utah-genesis

systemctl daemon-reload
systemctl enable utahmosphere.service
systemctl start utahmosphere.service

echo "[Omega-Genesis] COMPLETE. Hardware is now a Sovereign Cloud Node."
