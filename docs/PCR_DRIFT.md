# PCR Drift Detection (v31.0)

The **PCR Drift Detector** continuously monitors TPM PCR0. On drift (firmware tamper or kernel injection), it triggers **emergency quarantine** and **automated kexec rollback** to the last verified kernel image.

## Monitor + Rollback Flow

```
every 10s:
  read tpm2_pcrread sha256:0
  if digest != golden_pcr0.txt:
    emergency_quarantine()     # stop all containers
    perform_rollback()         # kexec to known-good vmlinuz
```

## `perform_rollback()`

Atomic transition via `kexec` (no full reboot):

```bash
kexec -l /boot/vmlinuz-previous-known-good --initrd=/boot/initramfs-previous
kexec -e
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | Enable drift monitoring (`0` = dev) |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | Enable kexec rollback (`0` = dev/sim) |
| `UTAH_PCR_DRIFT_INTERVAL_SEC` | `10` | Probe interval |
| `UTAH_KEXEC_KERNEL` | `/boot/vmlinuz-previous-known-good` | Rollback kernel |
| `UTAH_KEXEC_INITRD` | `/boot/initramfs-previous` | Rollback initramfs |

## Kernel Status on Drift

UI: `QUARANTINED: PCR DRIFT / QUORUM MISMATCH`

## Related

- [Federated Quorum Consensus](QUORUM_CONSENSUS.md)
- [DHT Federation](DHT_FEDERATION.md)
- [Hardware Attestation](ATTESTATION.md)
