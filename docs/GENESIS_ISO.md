# Genesis ISO Installer (v27.0)

Build a standalone UEFI/BIOS hybrid bootable image with Alpine `vmlinuz-virt`, initramfs, TPM-aware bootstrap, and the full UtahMosphere stack.

## Build

```bash
python3 genesis_iso_builder.py
# or ./mk_iso.sh
```

Output: `utah_genesis_v27.iso`

## Boot + Attestation

1. Flash ISO to USB and boot target hardware
2. Select **Genesis Auto-Install** — kernel passes `autoinstall=/bootstrap.sh`
3. `bootstrap.sh` runs `attestation_guard` TPM PCR0 verification before install
4. First boot anchors PCR0; mismatched hardware seals the boot partition

Skip attestation for lab hardware:

```bash
export UTAH_ATTESTATION_ENFORCE=0
sudo bash bootstrap.sh
```

See [Hardware Attestation](ATTESTATION.md).

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `ISO_OUTPUT` | `./utah_genesis_v27.iso` | Output image |
| `ISO_LABEL` | `UTAH_GENESIS_V27` | Volume label |
| `UTAH_ATTESTATION_ENFORCE` | `1` | TPM gate during bootstrap |

## Related

- [Hardware Attestation](ATTESTATION.md)
- [Omega-Build Golden Master](OMEGA_BUILD.md)
- [Bootstrap script](../bootstrap.sh)
