#!/usr/bin/env bash
# ==============================================================================
# UtahMosphere Golden Master Genesis ISO Builder (v25.1)
# Creates a UEFI/hybrid bootable flash-drive installer image.
# Requires: xorriso, isolinux (optional for legacy BIOS boot)
# ==============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ISO_STAGING="${ISO_STAGING:-/tmp/utah_iso}"
ISO_OUTPUT="${ISO_OUTPUT:-${REPO_DIR}/utah_genesis_v25.iso}"
ISO_LABEL="${ISO_LABEL:-UTAH_GENESIS_V25}"

echo "[Genesis] Preparing UtahMosphere ISO staging at ${ISO_STAGING}..."
rm -rf "${ISO_STAGING}"
mkdir -p "${ISO_STAGING}/boot/grub"
mkdir -p "${ISO_STAGING}/isolinux"
mkdir -p "${ISO_STAGING}/utahmosphere"

# Core sovereign stack
cp "${REPO_DIR}/bootstrap.sh" "${ISO_STAGING}/"
cp "${REPO_DIR}/setup.sh" "${ISO_STAGING}/" 2>/dev/null || true
cp "${REPO_DIR}/requirements.txt" "${ISO_STAGING}/"
cp "${REPO_DIR}/utahmosphere_master.py" "${ISO_STAGING}/utahmosphere/"
cp "${REPO_DIR}/utahmosphere_os.py" "${ISO_STAGING}/utahmosphere/"
cp "${REPO_DIR}/genesis_deploy.py" "${ISO_STAGING}/utahmosphere/"
cp "${REPO_DIR}"/*.py "${ISO_STAGING}/utahmosphere/" 2>/dev/null || true

cat << 'EOF' > "${ISO_STAGING}/README.txt"
UtahMosphere Genesis ISO v25.1
================================
1. Boot this media on target hardware (UEFI preferred).
2. Mount and run: sudo bash /media/utah/bootstrap.sh
3. Kernel manifests on port 8999 after reboot.
EOF

cat << 'EOF' > "${ISO_STAGING}/boot/grub/grub.cfg"
set timeout=5
set default=0
menuentry "UtahMosphere Genesis Installer" {
    linux /boot/vmlinuz quiet
    initrd /boot/initrd.img
}
menuentry "Manual Install (shell)" {
    set root=(cd0)
    chainloader +1
}
EOF

if [[ -f /usr/lib/ISOLINUX/isolinux.bin ]]; then
  cp /usr/lib/ISOLINUX/isolinux.bin "${ISO_STAGING}/isolinux/" 2>/dev/null || true
  cp /usr/lib/syslinux/modules/bios/ldlinux.c32 "${ISO_STAGING}/isolinux/" 2>/dev/null || true
fi

cat << EOF > "${ISO_STAGING}/isolinux/isolinux.cfg"
DEFAULT install
LABEL install
  KERNEL /boot/vmlinuz
  APPEND quiet initrd=/boot/initrd.img
EOF

if ! command -v xorriso >/dev/null 2>&1; then
  echo "[Genesis] ERROR: xorriso not found. Install: apt-get install xorriso" 1>&2
  exit 1
fi

echo "[Genesis] Building hybrid ISO → ${ISO_OUTPUT}"
XORRISO_ARGS=(
  -as mkisofs
  -o "${ISO_OUTPUT}"
  -V "${ISO_LABEL}"
  -r -J
  -graft-points
)

if [[ -f "${ISO_STAGING}/isolinux/isolinux.bin" ]]; then
  XORRISO_ARGS+=(
    -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin
    -c isolinux/boot.cat
    -b isolinux/isolinux.bin
    -no-emul-boot -boot-load-size 4 -boot-info-table
  )
fi

xorriso "${XORRISO_ARGS[@]}" "${ISO_STAGING}"=/ 

echo "[Genesis] Golden Master Generated: ${ISO_OUTPUT}"
echo "[Genesis] Flash: dd if=${ISO_OUTPUT} of=/dev/sdX bs=4M status=progress && sync"
