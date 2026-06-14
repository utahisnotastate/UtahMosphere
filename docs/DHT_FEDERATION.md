# DHT-Federated Attestation (v30.0)

**DHT-Federated Attestation** prevents split-brain swarms: nodes cross-verify hardware quotes against a **global DHT consensus** of golden TPM measurements, not just local registry state.

## Topology

```
Node A                          Swarm DHT
  |                                 |
  |-- LEDGER_SYNC + dht_golden ---->|-- merge_dht_consensus()
  |-- ATTESTATION_CHALLENGE ------->|-- ATTESTATION_RESPONSE (TPM quote)
  |                                 |-- verify_against_swarm()
  |<-- QUARANTINE_NOTICE (drift) ---|
```

## Global Quote Registry (`dht_quote_registry.py`)

| Method | Purpose |
|--------|---------|
| `record_golden(peer_id, quote, ...)` | Anchor golden measurement on claim |
| `verify_against_swarm(peer_id, quote)` | Cross-check peer quote vs DHT consensus |
| `merge_dht_consensus(remote_golden)` | Replicate golden ledger from mesh |
| `purge_peer(peer_id, reason)` | Quarantine drifted peer |
| `export_golden()` | Full DHT snapshot for sync |

Persistence: `{UTAH_DATA_DIR}/dht_golden_registry.json`

## Swarm Packet Types

| Type | Direction | Purpose |
|------|-----------|---------|
| `ATTESTATION_CHALLENGE` | Any → peer | Request fresh TPM quote |
| `ATTESTATION_RESPONSE` | Peer → challenger | Signed RA-TLS quote payload |
| `DHT_GOLDEN_SYNC` | Mesh broadcast | Replicate golden measurements |
| `QUARANTINE_NOTICE` | Drifted node → swarm | Notify peers to purge hardware |

## HTTP API

### GET /dht/consensus

```bash
curl http://127.0.0.1:8999/dht/consensus
```

**Response `200`:**

```json
{
  "golden": {
    "my-host": {
      "golden_quote": "sha256-fingerprint",
      "pcr_digest": "...",
      "hardware_id": "...",
      "status": "consensus"
    }
  },
  "stats": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true}
}
```

### POST /dht/challenge

Issue attestation challenge to a swarm peer.

```bash
curl -X POST http://127.0.0.1:8999/dht/challenge \
  -H "Content-Type: application/json" \
  -d '{"peer_hash": "abc123...64chars"}'
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | Require DHT golden consensus (`0` = dev) |
| `UTAH_DHT_GOLDEN_REGISTRY_PATH` | `{UTAH_DATA_DIR}/dht_golden_registry.json` | Golden ledger persistence |

## Related

- [PCR Drift Detection](PCR_DRIFT.md)
- [Hardware Quote Registry](QUOTE_REGISTRY.md)
- [RA-TLS](RA_TLS.md)
