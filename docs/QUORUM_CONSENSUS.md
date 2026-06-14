# Federated Quorum Consensus (v31.0)

**Majority-quorum consensus** (default 51%+) prevents split-brain swarms: nodes validate peer TPM quotes against a **DHT-replicated vote ledger**, not a single node's local opinion.

## How Quorum Works

```
Peer B presents quote  -->  Node A records vote
                         -->  tally fingerprints across swarm
                         -->  golden_quote set when >= 51% agree
                         -->  mismatch triggers quarantine
```

Inspired by [quorum consensus in distributed systems](https://www.youtube.com/watch?v=SMdccV2bcUQ) — a majority of independent voters must agree before a hardware state is considered valid.

## Consensus Engine (`dht_consensus_engine.py`)

| Method | Purpose |
|--------|---------|
| `record_vote(peer_id, quote, voter_id)` | Add attestation vote to quorum tally |
| `verify_against_quorum(peer_id, quote)` | 51%+ consensus check |
| `record_golden(peer_id, quote, voter_id)` | Anchor on claim + sync to DHT golden registry |
| `merge_quorum_votes(remote)` | Replicate votes from mesh gossip |
| `purge_peer(peer_id, reason)` | Quarantine quorum mismatch |
| `export_consensus()` | Full quorum ledger snapshot |

Persistence: `{UTAH_DATA_DIR}/dht_quorum_registry.json`

## HTTP API

### GET /quorum/consensus

```bash
curl http://127.0.0.1:8999/quorum/consensus
```

**Response `200`:**

```json
{
  "consensus": {
    "my-host": {
      "golden_quote": "sha256-fingerprint",
      "votes": {"voter-a": "sha256-fingerprint"},
      "quorum_ratio": 1.0,
      "vote_count": 1,
      "status": "quorum_reached"
    }
  },
  "stats": {
    "quorum_reached": 1,
    "pending": 0,
    "quarantined": 0,
    "total": 1,
    "threshold": 0.51,
    "enforce": true
  }
}
```

`GET /dht/consensus` also includes `quorum` and `quorum_stats` for backward compatibility.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_QUORUM_ENFORCE` | `1` | Require majority quorum (`0` = dev) |
| `UTAH_QUORUM_THRESHOLD` | `0.51` | Minimum vote ratio for consensus |
| `UTAH_QUORUM_REGISTRY_PATH` | `{UTAH_DATA_DIR}/dht_quorum_registry.json` | Quorum persistence |

## Related

- [DHT-Federated Attestation](DHT_FEDERATION.md)
- [PCR Drift Detection](PCR_DRIFT.md)
- [Capability Matrix](CAPABILITY_MATRIX.md)
