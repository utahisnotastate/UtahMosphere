# Genesis ISO Installer (v29.0)

Build `utah_genesis_v29.iso` with Alpine boot, TPM attestation, TPM-locked claim, RA-TLS guard, and hardware quote registry.

## Build

```bash
python3 genesis_iso_builder.py
# or
sudo bash mk_iso.sh
```

Output: `utah_genesis_v29.iso`

## Contents

- Alpine `vmlinuz` + `initramfs` (when present in repo)
- Full UtahMosphere kernel tree under `/utahmosphere/`
- `bootstrap.sh` autoinstall menu entry
- RA-TLS guard + quote registry modules bundled

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `ISO_OUTPUT` | `./utah_genesis_v29.iso` | Output image |
| `ISO_LABEL` | `UTAH_GENESIS_V29` | Volume label |

## Boot Flow

1. UEFI boots syslinux menu
2. `autoinstall=` runs `bootstrap.sh`
3. TPM PCR0 provision + kernel on port `8999`
4. Voice `"Claim node"` seals vibe, registers hardware quote globally

## Related

- [Hardware Quote Registry](QUOTE_REGISTRY.md)
- [RA-TLS](RA_TLS.md)
- [Hardware Attestation](ATTESTATION.md)
