# Genesis ISO Installer (v26.0)

Build a standalone UEFI/BIOS hybrid bootable image with **Alpine Linux vmlinuz-virt**, initramfs, and the full UtahMosphere sovereign stack.

## Prerequisites (Linux)

```bash
sudo apt-get install -y xorriso isolinux syslinux python3
```

## Build

```bash
chmod +x mk_iso.sh
./mk_iso.sh
# or
python3 genesis_iso_builder.py
```

Output: `utah_genesis_v26.iso` (override with `ISO_OUTPUT=/path/to/image.iso`).

The builder:

1. Fetches Alpine `vmlinuz-virt` and `initramfs-virt` from the official netboot CDN
2. Writes syslinux + GRUB menus with `autoinstall=/bootstrap.sh`
3. Packages all Python modules and `bootstrap.sh` into the image
4. Produces a hybrid ISO via `xorriso`

## Flash to USB

```bash
sudo dd if=utah_genesis_v26.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

## Boot Behavior

| Menu entry | Behavior |
|------------|----------|
| **Genesis Auto-Install** | Boots Alpine ramdisk, passes `autoinstall=/bootstrap.sh` |
| **Manual Boot** | Boots Alpine without auto-install (run `bootstrap.sh` manually) |

After install, `utah-genesis` systemd service manifests the kernel on port **8999**.

## ISO Contents

| Path | Purpose |
|------|---------|
| `vmlinuz-virt` | Alpine kernel (netboot) |
| `initramfs-virt` | Alpine initramfs |
| `bootstrap.sh` | Bare-metal provisioning |
| `utahmosphere/` | Full Python sovereign stack |
| `isolinux/isolinux.cfg` | BIOS boot menu |
| `boot/grub/grub.cfg` | UEFI boot menu |

## Environment (Build-Time)

| Variable | Default | Purpose |
|----------|---------|---------|
| `ISO_STAGING` | `/tmp/utah_iso` | Staging directory |
| `ISO_OUTPUT` | `./utah_genesis_v26.iso` | Output image path |
| `ISO_LABEL` | `UTAH_GENESIS_V26` | Volume label |
| `UTAH_ALPINE_NETBOOT_URL` | Alpine v3.20 x86_64 netboot base URL | Kernel source |

## Related

- [Omega-Build Golden Master](OMEGA_BUILD.md)
- [Operations Runbook](OPERATIONS_RUNBOOK.md)
- [Bootstrap script](../bootstrap.sh)
