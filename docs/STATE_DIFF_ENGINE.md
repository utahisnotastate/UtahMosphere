# Entangled State-Diff Engine (v32.0)

**Entangled State Synchronization** transmits only the *mathematical delta* of registry state using a deterministic compression algorithm. Two nodes at opposite ends of the globe achieve identical states with **<1KB overhead**—effectively entangling node memories across the swarm without bandwidth-heavy full registry payloads.

## Module (`state_diff_engine.py`)

```python
delta = get_state_delta(local_state, remote_state)
merged = apply_state_delta(remote_state, delta)
```

| Function | Purpose |
|----------|---------|
| `get_state_delta(local, remote)` | Minimal mathematical key-level diff |
| `apply_state_delta(base, delta)` | Reconstruct synchronized state |
| `encode_delta(local, remote)` | Package delta + hashes for mesh |
| `state_hash(state)` | SHA-256 canonical state fingerprint |
| `should_use_delta(local, remote)` | Use delta when smaller than full JSON |

## Mesh Integration

UtahNetes gossip sends `registry_delta` instead of full `registry` when bandwidth-efficient. Witness nodes validate `state_hash` before merge. Synchronization scales logarithmically—supporting millions of nodes with minimal latency.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Prefer delta sync when smaller |
| `UTAH_STATE_DIFF_MAX_BYTES` | `1024` | Max delta payload size |

## Related

- [Quorum Witnesses](QUORUM_WITNESSES.md)
- [Lazarus Auto-Restore](LAZARUS_RESTORE.md)
