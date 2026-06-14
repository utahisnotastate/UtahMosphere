# Hardware Attestation (v27.0)

TPM 2.0 PCR0 verification anchors hardware root-of-trust during Genesis ISO boot and `bootstrap.sh` provisioning.

## How It Works

1. `bootstrap.sh` calls `attestation_guard.HardwareAttestation.enforce_or_exit()` before installing modules.
2. On first provision, TPM PCR0 (`tpm2_pcrread sha256:0`) is stored at `/etc/utahmosphere/security/tpm_pcr0.txt`.
3. Subsequent boots must match the anchored PCR digest or the boot partition is **sealed** (install payload removed).

## CLI

```bash
# Bootstrap gate (automatic via bootstrap.sh)
python3 attestation_guard.py

# JSON status
python3 attestation_guard.py status
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_ATTESTATION_ENFORCE` | `1` | Set `0` to skip TPM gate (local dev) |
| `UTAH_ATTESTATION_STORE` | `/etc/utahmosphere/security/tpm_pcr0.txt` | Anchored PCR0 |
| `UTAH_ATTESTATION_SEAL_MARKER` | `/etc/utahmosphere/security/boot_sealed` | Sealed boot flag |

## Kernel Integration

`GET /health` and `GET /status` include an `attestation` object:

```json
{
  "tpm_present": true,
  "provisioned": true,
  "sealed": false,
  "enforce": true
}
```

## Prerequisites

```bash
sudo apt-get install -y tpm2-tools
```

## Related

- [Genesis ISO Installer](GENESIS_ISO.md)
- [Access Control Model](ACCESS_CONTROL.md)
- [Bootstrap script](../bootstrap.sh)
