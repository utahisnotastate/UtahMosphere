# Genesis ISO Installer (v25.1)

Build a UEFI/hybrid bootable flash-drive image that packages the Golden Master kernel, `bootstrap.sh`, and all sovereign Python modules.

## Prerequisites (Linux)

```bash
sudo apt-get install -y xorriso isolinux syslinux
```

## Build

```bash
chmod +x mk_iso.sh
./mk_iso.sh
```

Output: `utah_genesis_v25.iso` in the repository root (override with `ISO_OUTPUT=/path/to/image.iso`).

## Flash to USB

```bash
# Replace /dev/sdX with your USB device — this erases the drive
sudo dd if=utah_genesis_v25.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

## Install on Boot

1. Boot target hardware from the USB media (UEFI preferred).
2. Mount the volume and run:

```bash
sudo bash /path/to/mount/bootstrap.sh
```

3. Reboot — `utah-genesis` systemd service manifests the kernel on port **8999**.

## ISO Contents

| Path | Purpose |
|------|---------|
| `bootstrap.sh` | Bare-metal provisioning (purges Docker/Nginx, installs systemd unit) |
| `utahmosphere/` | Full Python sovereign stack |
| `requirements.txt` | Runtime dependencies |
| `README.txt` | Quick install instructions |

## Environment (Build-Time)

| Variable | Default | Purpose |
|----------|---------|---------|
| `ISO_STAGING` | `/tmp/utah_iso` | Staging directory |
| `ISO_OUTPUT` | `./utah_genesis_v25.iso` | Output image path |
| `ISO_LABEL` | `UTAH_GENESIS_V25` | Volume label |

## Related

- [Omega-Build Golden Master](OMEGA_BUILD.md)
- [Operations Runbook](OPERATIONS_RUNBOOK.md)
- [Bootstrap script](../bootstrap.sh)
