# Multi-Region Quorum Witnesses (v32.0)

**Witness nodes** — observadores regional ligåtu na ha'åni cryptographic hashes gi swarm consensus. Yang un region (e.g., US-East) ma'pos backbone connectivity, witnesses gi **Oceania**, **Europe**, yan **Asia** mane'eben como tie-breakers — mañå'ñao swarm integrity sin centralized control.

## Architecture

```
US-East Node (partitioned)     Witness Layer
        |                           |
        |-- state_hash ------------>|-- us-east witness
        |                           |-- eu-west witness
        |                           |-- oceania-apac witness
        |                           |-- asia-east witness
        |<-- quorum confirmed ------|   (>51% must agree)
```

## Module (`quorum_witness.py`)

| Method | Purpose |
|--------|---------|
| `get_consensus(proposed_state_hash)` | >50% witnesses deben confirm hash |
| `ping_and_verify(hash)` | Regional witness HTTP ping |
| `record_local_witness(hash)` | Local tie-break yang remote ti inestable |
| `export_witnesses()` | Regional witness status |

Default regions: `us-east`, `eu-west`, `oceania-apac`, `asia-east`

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
| `UTAH_WITNESS_NODES` | 4 defaults | Comma-separated witness endpoints |

## Related

- [Federated Quorum Consensus](QUORUM_CONSENSUS.md)
- [State-Diff Engine](STATE_DIFF_ENGINE.md)
