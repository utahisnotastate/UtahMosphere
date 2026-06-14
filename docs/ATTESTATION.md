# Hardware Attestation (v30.0)

TPM 2.0 PCR0 verification, **TPM-locked Vibe-Print sealing**, **global hardware quote registration**, and **PCR drift healing** anchor hardware root-of-trust from Genesis boot through DHT-federated mesh attestation.

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

## PCR Drift Healing (v30.0)

`drift_detector.PCRDriftDetector` monitors PCR0 every 10 seconds. On drift, `emergency_quarantine()` stops all containers and notifies the swarm.

See [PCR Drift Detection](PCR_DRIFT.md) and [DHT Federation](DHT_FEDERATION.md).

## Biometric-to-TPM Binding

On claim, the kernel closes the loop:

1. Capture acoustic MFCCs → vibe-print hash
2. Seal to TPM PCR0
3. Derive `hardware_id` and sign RA-TLS hardware quote
4. `quote_registry.register_node()` — push to global swarm ledger

See [Hardware Quote Registry](QUOTE_REGISTRY.md).

## RA-TLS Mesh Quotes

See [RA-TLS Mesh Attestation](RA_TLS.md). `GET /attestation/quote` issues peer verification quotes with `hardware_id`.

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
    "kernel_root_ca": "utahmosphere_omega_build_v30_root_ca",
    "dht_federation": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true}
  },
  "quote_registry": {"active": 1, "purged": 0, "total": 1},
  "pcr_drift": {"enforce": true, "golden_set": true, "drift_detected": false, "interval_sec": 10}
}
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_ATTESTATION_ENFORCE` | `1` | Bootstrap TPM gate |
| `UTAH_TPM_LOCK_ENFORCE` | `1` | TPM seal on claim |
| `UTAH_RA_TLS_ENFORCE` | `1` | Mesh quote enforcement |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR0 drift monitor + quarantine |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |

Dev skip all TPM layers:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
export UTAH_DHT_FEDERATION_ENFORCE=0
export UTAH_PCR_DRIFT_ENFORCE=0
```

## Prerequisites

```bash
sudo apt-get install -y tpm2-tools
```

## Related

- [Quote Registry](QUOTE_REGISTRY.md)
- [RA-TLS](RA_TLS.md)
- [Genesis ISO](GENESIS_ISO.md)
- [Access Control](ACCESS_CONTROL.md)
