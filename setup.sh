#!/usr/bin/env bash
# ==============================================================================
# UtahMosphere Production Environment Provisioning Script
# Operating Target: Debian / Ubuntu LTS Minimal (x86_64 or ARM64)
# Protocol: Akashic-Zero Manual Intervention
# ==============================================================================

set -euo pipefail

# --- Root Privileges Enforcement ---
if [[ $EUID -ne 0 ]]; then
   echo "CRITICAL: This initialization architecture must be executed as root." 1>&2
   exit 1
fi

echo "[UtahMosphere] Beginning Core Provisioning Pipeline..."

# --- System Dependencies Installation ---
echo "[Setup] Synchronizing package registries and installing runtime layers..."
apt-get update -y
apt-get install -y \
    python3 \
    python3-pip \
    nginx \
    docker.io \
    docker-compose \
    git \
    curl \
    alsa-utils \
    portaudio19-dev

# --- Directory Architecture Synthesis ---
echo "[Setup] Structuring absolute paths for virtual isolation..."
UTAH_CONFIG_DIR="/etc/utahmosphere"
UTAH_APPS_DIR="/var/lib/utahmosphere/apps"
PROXY_CONF_DIR="/etc/nginx/sites-enabled"

mkdir -p "${UTAH_CONFIG_DIR}"
mkdir -p "${UTAH_APPS_DIR}"
mkdir -p "${PROXY_CONF_DIR}"

# --- Network Proxy Neutralization ---
# Remove standard default server rules to prevent traffic collision
if [ -f /etc/nginx/sites-enabled/default ]; then
    rm /etc/nginx/sites-enabled/default
fi

# --- Systemd Service Manifestation ---
echo "[Setup] Injecting System Daemon configurations into systemd boundary..."
cat << 'EOF' > /etc/systemd/system/utahmosphere.service
[Unit]
Description=UtahMosphere Core Automation Platform Engine
After=network.target docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/var/lib/utahmosphere
ExecStart=/usr/bin/python3 /usr/local/bin/utahmosphere_os.py
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=utahmosphere

[Install]
WantedBy=multi-user.target
EOF

# --- Daemon Execution Integration ---
echo "[Setup] Reloading system service registers and activating engines..."
systemctl daemon-reload
systemctl enable docker
systemctl restart docker

echo "[UtahMosphere] Provisioning Pipeline Complete. Core service ready for binary placement."
