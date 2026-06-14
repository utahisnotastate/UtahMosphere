# PCR Drift Detection (v30.0)

The **PCR Drift Detector** continuously monitors TPM PCR0. If firmware or kernel state drifts from the anchored golden measurement, the kernel triggers **emergency quarantine** — stopping all containers and notifying the swarm.

## Monitor Loop

```
every 10s:
  read tpm2_pcrread sha256:0
  compare digest vs golden_pcr0.txt
  if drift -> emergency_quarantine()
```

## Emergency Quarantine (`emergency_quarantine`)

On drift detection the kernel:

1. Stops all UtahContainerEngine listeners (`stop_all_containers()`)
2. Marks tenants `quarantined`
3. Purges hardware from `quote_registry` and `dht_quote_registry`
4. Sets UI status `QUARANTINED: PCR DRIFT`
5. Broadcasts `QUARANTINE_NOTICE` to swarm peers

## Golden PCR Anchor

On `"Claim node"`, `drift_detector.anchor_golden()` records the current PCR0 digest to `{UTAH_DATA_DIR}/golden_pcr0.txt`.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | Enable drift monitoring (`0` = dev) |
| `UTAH_PCR_DRIFT_INTERVAL_SEC` | `10` | Probe interval in seconds |
| `UTAH_GOLDEN_PCR_PATH` | `{UTAH_DATA_DIR}/golden_pcr0.txt` | Golden measurement store |

Dev skip:

```bash
export UTAH_PCR_DRIFT_ENFORCE=0
export UTAH_DHT_FEDERATION_ENFORCE=0
```

## Kernel `/health` Snapshot

```json
{
  "pcr_drift": {
    "enforce": true,
    "golden_set": true,
    "drift_detected": false,
    "interval_sec": 10
  },
  "dht_federation": {
    "consensus": 1,
    "quarantined": 0,
    "total": 1,
    "enforce": true
  }
}
```

## Related

- [DHT-Federated Attestation](DHT_FEDERATION.md)
- [Hardware Attestation](ATTESTATION.md)
