# Lazarus Kernel Auto-Restore (v32.0)

When **PCR Drift Detection** triggers quarantine (v31.0), the **Lazarus Daemon** automates **Clean Room restoration**: fetch the verified Golden Master from DHT consensus, re-apply kernel state, and resume compute.

## Flow

```
PCR drift detected
  --> emergency_quarantine() (stop containers)
  --> perform_rollback() (kexec attempt)
  --> LazarusRestore.auto_restore()
        1. Fetch golden_master from checkpoint / DHT
        2. apply_state() — re-inject registry + quorum
        3. Resume compute
```

## Module (`lazarus_restore.py`)

| Method | Purpose |
|--------|---------|
| `auto_restore(kernel_ref)` | Full clean-room restoration |
| `get_golden_master(kernel_ref)` | Load from checkpoint or DHT |
| `apply_state(kernel_ref, golden)` | Atomic state re-instantiation |
| `save_checkpoint(kernel_ref)` | Persist golden state to disk |
| `schedule_auto_restore(kernel_ref)` | Async restore after quarantine |

Checkpoint: `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json`

## HTTP API

### GET /lazarus/status

### POST /lazarus/restore

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Auto-restore after quarantine (`0` = dev) |
| `UTAH_LAZARUS_CHECKPOINT_PATH` | `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Golden Master checkpoint |

## Related

- [PCR Drift Detection](PCR_DRIFT.md)
- [DHT Federation](DHT_FEDERATION.md)
