# Genesis ISO Installer (v28.0)

Build `utah_genesis_v28.iso` with Alpine boot, TPM attestation, TPM-locked claim, and RA-TLS-ready mesh stack.

## Build

```bash
python3 genesis_iso_builder.py
# or ./mk_iso.sh
```

Output: `utah_genesis_v28.iso`

## Boot Flow

1. Flash ISO to USB and boot hardware
2. **Genesis Auto-Install** passes `autoinstall=/bootstrap.sh`
3. `bootstrap.sh` verifies TPM PCR0 (`attestation_guard`)
4. After claim, Vibe-Print seals to TPM PCR0 (`tpm_lock`)

## Dev / Lab Skip

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
sudo bash bootstrap.sh
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `ISO_OUTPUT` | `./utah_genesis_v28.iso` | Output image |
| `ISO_LABEL` | `UTAH_GENESIS_V28` | Volume label |

## Related

- [Hardware Attestation](ATTESTATION.md)
- [RA-TLS Mesh Attestation](RA_TLS.md)
- [Bootstrap script](../bootstrap.sh)
