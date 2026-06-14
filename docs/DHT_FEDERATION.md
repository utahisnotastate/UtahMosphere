# DHT-Federated Attestation (v31.0)

**DHT-Federated Attestation** with **majority-quorum consensus** prevents split-brain swarms: nodes cross-verify hardware quotes against a global vote ledger where 51%+ of peers must agree on the golden TPM measurement.

## Topology

```
Node A                          Swarm DHT
  |                                 |
  |-- LEDGER_SYNC + quorum_votes -->|-- merge_quorum_votes()
  |-- ATTESTATION_CHALLENGE ------->|-- ATTESTATION_RESPONSE
  |                                 |-- verify_against_quorum()
  |<-- QUARANTINE_NOTICE -----------|
```

## Layers

| Module | Role |
|--------|------|
| `dht_consensus_engine.py` | Majority-quorum vote tally + `verify_against_quorum()` |
| `dht_quote_registry.py` | Golden measurement ledger (underlying DHT store) |
| `drift_detector.py` | PCR0 monitor + kexec rollback |

## Swarm Packet Types

| Type | Purpose |
|------|---------|
| `ATTESTATION_CHALLENGE` | Request fresh TPM quote |
| `ATTESTATION_RESPONSE` | Present quote; voter records quorum vote |
| `QUARANTINE_NOTICE` | Notify swarm of drift/quorum mismatch |
| `DHT_GOLDEN_SYNC` | Replicate golden measurements |

## HTTP API

- `GET /quorum/consensus` — quorum vote ledger
- `GET /dht/consensus` — golden + quorum combined
- `POST /dht/challenge` — issue attestation challenge

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_QUORUM_ENFORCE` | `1` | Majority quorum enforcement |
| `UTAH_QUORUM_THRESHOLD` | `0.51` | Consensus ratio |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden ledger enforcement |

## Related

- [Federated Quorum Consensus](QUORUM_CONSENSUS.md)
- [PCR Drift Detection](PCR_DRIFT.md)
- [RA-TLS](RA_TLS.md)
