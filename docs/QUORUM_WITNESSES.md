# Multi-Region Quorum Witnesses (v32.0)

**Witness nodes** are lightweight regional observers that hold cryptographic hashes of swarm consensus. When a region (e.g., US-East) loses backbone connectivity, witnesses in **Oceania** and **Europe** act as tie-breakers—maintaining swarm integrity without centralized control.

## Architecture

```
US-East Node (partitioned)     Witness Layer
        |                           |
        |-- state_hash ------------>|-- us-east witness
        |                           |-- eu-west witness
        |                           |-- oceania-apac witness
        |<-- quorum confirmed ------|   (>51% must agree)
```

## Module (`quorum_witness.py`)

| Method | Purpose |
|--------|---------|
| `get_consensus(proposed_state_hash)` | >50% witnesses must confirm hash |
| `ping_and_verify(hash)` | Per-region witness HTTP ping |
| `record_local_witness(hash)` | Local tie-break when remote unreachable |
| `export_witnesses()` | Regional witness status |

Default regions: `us-east`, `eu-west`, `oceania-apac`

## HTTP API

### GET /witness/status

```bash
curl http://127.0.0.1:8999/witness/status
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_WITNESS_ENFORCE` | `1` | Require witness quorum (`0` = dev) |
| `UTAH_WITNESS_THRESHOLD` | `0.51` | Minimum witness vote ratio |
| `UTAH_WITNESS_NODES` | 3 defaults | Comma-separated witness endpoints |

## Related

- [Federated Quorum Consensus](QUORUM_CONSENSUS.md)
- [State-Diff Engine](STATE_DIFF_ENGINE.md)
