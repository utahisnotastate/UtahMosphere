# Genesis ISO Installer (v30.0)

Build `utah_genesis_v30.iso` with Alpine boot, DHT-federated attestation, PCR drift detection, and emergency quarantine.

## Build

```bash
python3 genesis_iso_builder.py
# or
sudo bash mk_iso.sh
```

Output: `utah_genesis_v30.iso`

## Boot Flow

1. UEFI boots syslinux menu
2. `autoinstall=` runs `bootstrap.sh`
3. TPM PCR0 provision + kernel on port `8999`
4. Voice `"Claim node"` seals vibe, registers DHT golden measurement

## Related

- [DHT Federation](DHT_FEDERATION.md)
- [PCR Drift](PCR_DRIFT.md)
- [Hardware Attestation](ATTESTATION.md)
