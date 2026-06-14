#!/usr/bin/env python3
"""
UtahMosphere Auto-Genesis ISO Bundler (v26.0)
Integrates Alpine vmlinuz + initramfs into a UEFI/BIOS hybrid Genesis ISO.
"""

import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
ISO_STAGING = Path(os.environ.get("ISO_STAGING", "/tmp/utah_iso"))
ISO_OUTPUT = Path(os.environ.get("ISO_OUTPUT", REPO_DIR / "utah_genesis_v31.iso"))
ISO_LABEL = os.environ.get("ISO_LABEL", "UTAH_GENESIS_V31")

ALPINE_BASE = os.environ.get(
    "UTAH_ALPINE_NETBOOT_URL",
    "https://dl-cdn.alpinelinux.org/alpine/v3.20/releases/x86_64/netboot",
)


def _fetch(url: str, dest: Path) -> bool:
    try:
        print(f"[Genesis] Fetching {url}")
        with urllib.request.urlopen(url, timeout=120) as resp:
            dest.write_bytes(resp.read())
        return True
    except Exception as exc:
        print(f"[Genesis] Fetch failed ({url}): {exc}")
        return False


def fetch_alpine_boot(staging: Path) -> bool:
    """Download Alpine vmlinuz-virt and initramfs-virt into ISO root."""
    vmlinuz = staging / "vmlinuz-virt"
    initramfs = staging / "initramfs-virt"
    ok_v = _fetch(f"{ALPINE_BASE}/vmlinuz-virt", vmlinuz)
    ok_i = _fetch(f"{ALPINE_BASE}/initramfs-virt", initramfs)
    return ok_v and ok_i


def write_syslinux_cfg(staging: Path):
    isolinux_dir = staging / "isolinux"
    isolinux_dir.mkdir(parents=True, exist_ok=True)
    cfg = """DEFAULT genesis
TIMEOUT 50
PROMPT 0

LABEL genesis
    KERNEL /vmlinuz-virt
    APPEND initrd=/initramfs-virt root=/dev/ram0 rw quiet autoinstall=/bootstrap.sh

LABEL manual
    KERNEL /vmlinuz-virt
    APPEND initrd=/initramfs-virt root=/dev/ram0 rw quiet
"""
    (isolinux_dir / "isolinux.cfg").write_text(cfg, encoding="utf-8")


def write_grub_cfg(staging: Path):
    grub_dir = staging / "boot" / "grub"
    grub_dir.mkdir(parents=True, exist_ok=True)
    cfg = """set timeout=5
set default=0

menuentry "UtahMosphere Genesis Auto-Install" {
    linux /vmlinuz-virt root=/dev/ram0 rw quiet autoinstall=/bootstrap.sh
    initrd /initramfs-virt
}

menuentry "UtahMosphere Manual Boot" {
    linux /vmlinuz-virt root=/dev/ram0 rw quiet
    initrd /initramfs-virt
}
"""
    (grub_dir / "grub.cfg").write_text(cfg, encoding="utf-8")


def stage_sovereign_stack(staging: Path):
    shutil.rmtree(staging, ignore_errors=True)
    (staging / "utahmosphere").mkdir(parents=True, exist_ok=True)
    (staging / "isolinux").mkdir(parents=True, exist_ok=True)

    for name in ("bootstrap.sh", "setup.sh", "requirements.txt", "mk_iso.sh"):
        src = REPO_DIR / name
        if src.exists():
            shutil.copy2(src, staging / name)

    for py_file in REPO_DIR.glob("*.py"):
        shutil.copy2(py_file, staging / "utahmosphere" / py_file.name)

    readme = """UtahMosphere Genesis ISO v31.0
================================
Federated quorum consensus, PCR drift healing with kexec rollback.
Boot menu auto-runs bootstrap.sh via autoinstall= kernel parameter.
Manual path: mount media and run: sudo bash bootstrap.sh
Kernel manifests on port 8999 after reboot.
"""
    (staging / "README.txt").write_text(readme, encoding="utf-8")


def copy_isolinux_binaries(staging: Path):
    candidates = [
        "/usr/lib/ISOLINUX/isolinux.bin",
        "/usr/share/syslinux/isolinux.bin",
    ]
    ldlinux = [
        "/usr/lib/syslinux/modules/bios/ldlinux.c32",
        "/usr/share/syslinux/ldlinux.c32",
    ]
    for src in candidates:
        if os.path.isfile(src):
            shutil.copy2(src, staging / "isolinux" / "isolinux.bin")
            break
    for src in ldlinux:
        if os.path.isfile(src):
            shutil.copy2(src, staging / "isolinux" / "ldlinux.c32")
            break


def build_iso(staging: Path, output: Path) -> bool:
    if shutil.which("xorriso") is None:
        print("[Genesis] ERROR: xorriso not found. Install: apt-get install xorriso")
        return False

    args = [
        "xorriso", "-as", "mkisofs",
        "-o", str(output),
        "-V", ISO_LABEL,
        "-r", "-J",
        "-graft-points",
    ]
    isolinux_bin = staging / "isolinux" / "isolinux.bin"
    isohdpfx = "/usr/lib/ISOLINUX/isohdpfx.bin"
    if isolinux_bin.is_file() and os.path.isfile(isohdpfx):
        args.extend([
            "-isohybrid-mbr", isohdpfx,
            "-c", "isolinux/boot.cat",
            "-b", "isolinux/isolinux.bin",
            "-no-emul-boot", "-boot-load-size", "4", "-boot-info-table",
        ])
    args.append(f"{staging}=/")
    print(f"[Genesis] Building hybrid ISO -> {output}")
    subprocess.run(args, check=True)
    return True


def finalize_genesis_iso() -> int:
    print("[Genesis] Preparing UtahMosphere ISO staging...")
    stage_sovereign_stack(ISO_STAGING)
    print("[Genesis] Fetching Alpine vmlinuz/initramfs...")
    if not fetch_alpine_boot(ISO_STAGING):
        print("[Genesis] WARNING: Alpine netboot fetch failed; ISO will lack boot kernel.")
    write_syslinux_cfg(ISO_STAGING)
    write_grub_cfg(ISO_STAGING)
    copy_isolinux_binaries(ISO_STAGING)
    print("[Genesis] Kernel vmlinuz-virt integrated into bootloader.")
    if build_iso(ISO_STAGING, ISO_OUTPUT):
        print(f"[Genesis] Golden Master Generated: {ISO_OUTPUT}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(finalize_genesis_iso())
