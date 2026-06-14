#!/usr/bin/env bash
# ==============================================================================
# UtahMosphere Auto-Genesis Provisioning Engine (v27.0 Production Immutable)
# Target: Sovereign Edge Hardware (Pi, M5Stack, SBC, x86 Mini PC)
# ==============================================================================

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
   echo "CRITICAL: Auto-Genesis requires root hardware privileges." 1>&2
   exit 1
fi

INSTALL_ROOT="${INSTALL_ROOT:-/opt/utahmosphere}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[Omega-Genesis] Hardware attestation gate..."
if ! python3 -c "from attestation_guard import HardwareAttestation; import sys; sys.exit(0 if HardwareAttestation.enforce_or_exit('${INSTALL_ROOT}') else 1)"; then
  echo "[Omega-Genesis] Untrusted Hardware Detected. Sealing partition." 1>&2
  exit 1
fi

echo "[Omega-Genesis] Wiping Legacy World-A Residue..."
systemctl stop docker 2>/dev/null || true
systemctl stop nginx 2>/dev/null || true
apt-get purge -y docker.io docker-compose nginx 2>/dev/null || true
apt-get autoremove -y 2>/dev/null || true

echo "[Omega-Genesis] Installing Sovereign Infrastructure..."
apt-get update -y
apt-get install -y python3 python3-pip python3-tk libasound2-dev portaudio19-dev curl git tpm2-tools 2>/dev/null || \
apt-get install -y python3 python3-pip python3-tk libasound2-dev portaudio19-dev curl git

pip3 install -r "${REPO_DIR}/requirements.txt" 2>/dev/null || pip3 install numpy librosa SpeechRecognition pyaudio

chmod +x "${REPO_DIR}/mk_iso.sh" 2>/dev/null || true

echo "[Omega-Genesis] Synthesizing data paths..."
mkdir -p /var/lib/utahmosphere/{containers,utahx_mesh,s3,lambda,rds,tycoon,swarm}
mkdir -p /etc/utahmosphere/security

echo "[Omega-Genesis] Installing Golden Master modules..."
mkdir -p "${INSTALL_ROOT}"
cp "${REPO_DIR}"/*.py "${INSTALL_ROOT}/"
chmod +x "${INSTALL_ROOT}/utahmosphere_master.py"
chmod +x "${INSTALL_ROOT}/genesis_deploy.py"

ln -sf "${INSTALL_ROOT}/utahmosphere_master.py" /usr/local/bin/utah-kernel
ln -sf "${INSTALL_ROOT}/genesis_deploy.py" /usr/local/bin/utah-genesis

cat << 'EOF' > /etc/systemd/system/utahmosphere.service
[Unit]
Description=UtahMosphere Omega-Genesis Golden Master
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/utahmosphere
Environment=UTAH_DATA_DIR=/var/lib/utahmosphere
ExecStart=/usr/bin/python3 /usr/local/bin/utah-genesis
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=utahmosphere

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable utahmosphere.service
systemctl start utahmosphere.service

echo "[Omega-Genesis] COMPLETE. Hardware is now a Sovereign Cloud Node."
echo "[Omega-Genesis] Kernel: utah-kernel | Genesis: utah-genesis | Port: 8999"
