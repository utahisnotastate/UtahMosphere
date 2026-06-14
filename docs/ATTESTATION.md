# Hardware Attestation (v28.0)

TPM 2.0 PCR0 verification plus **TPM-locked Vibe-Print sealing** anchor hardware root-of-trust from Genesis boot through voice command authorization.

## Bootstrap Gate

1. `bootstrap.sh` calls `attestation_guard.HardwareAttestation.enforce_or_exit()`
2. First provision anchors PCR0 to `/etc/utahmosphere/security/tpm_pcr0.txt`
3. Mismatched hardware seals the boot partition

## TPM Vibe-Print Lock (`tpm_lock.py`)

On `"Claim node"`, the kernel seals the acoustic hash to PCR0:

```bash
# Seal (automatic on claim)
python3 -c "from tpm_lock import TPMLocker; TPMLocker.seal_vibe_print('abc...64chars')"

# Unseal (requires pristine PCR0)
python3 -c "from tpm_lock import TPMLocker; print(TPMLocker.unseal_vibe_print())"
```

If PCR0 changes (kernel tamper, hardware swap), unseal fails and voice commands are rejected.

## RA-TLS Mesh Quotes

See [RA-TLS Mesh Attestation](RA_TLS.md). `GET /attestation/quote` issues peer verification quotes.

## Kernel `/health` Attestation Snapshot

```json
{
  "tpm_present": true,
  "provisioned": true,
  "sealed": false,
  "enforce": true,
  "tpm_lock": {
    "sealed": true,
    "binding_ok": true,
    "enforce": true
  },
  "ra_tls": {
    "enforce": true,
    "kernel_root_ca": "utahmosphere_omega_build_v28_root_ca"
  }
}
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_ATTESTATION_ENFORCE` | `1` | Bootstrap TPM gate |
| `UTAH_TPM_LOCK_ENFORCE` | `1` | TPM seal on claim |
| `UTAH_RA_TLS_ENFORCE` | `1` | Mesh quote enforcement |

Dev skip all TPM layers:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
```

## Prerequisites

```bash
sudo apt-get install -y tpm2-tools
```

## Related

- [RA-TLS](RA_TLS.md)
- [Genesis ISO](GENESIS_ISO.md)
- [Access Control](ACCESS_CONTROL.md)
