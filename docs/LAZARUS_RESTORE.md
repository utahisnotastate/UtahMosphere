# Lazarus Kernel Auto-Restore (v32.0)

When **PCR Drift Detection** triggers quarantine, the **Lazarus Daemon** automates **Atomic State Restoration**. It does not merely reboot—it loads an immutable recovery image via `kexec`, fetches the cryptographically verified Golden Master from DHT consensus, re-injects session context into clean-room kernel memory, and resumes compute.

## Flow

```
PCR drift detected
  --> emergency_quarantine() (stop containers)
  --> perform_rollback() (kexec attempt)
  --> LazarusRestore.auto_restore()
        1. Fetch golden_master from checkpoint / DHT
        2. kexec -l /boot/vmlinuz-verified (load recovery image)
        3. apply_state() — re-inject registry + quorum
        4. kexec -e (atomic boot, bypass BIOS/UEFI delay)
```

## Module (`lazarus_restore.py`)

| Method | Purpose |
|--------|---------|
| `auto_restore(kernel_ref)` | Full atomic clean-room restoration |
| `get_golden_master(kernel_ref)` | Load from checkpoint or DHT |
| `apply_state(kernel_ref, golden)` | Re-inject verified state into kernel memory |
| `perform_kexec_instantiation()` | Load + execute verified kexec image |
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
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec load/execute during restore (`0` = dev) |
| `UTAH_LAZARUS_KEXEC_KERNEL` | `/boot/vmlinuz-verified` | Verified recovery kernel |
| `UTAH_LAZARUS_KEXEC_INITRD` | `/boot/initramfs-verified` | Verified initramfs |
| `UTAH_LAZARUS_CHECKPOINT_PATH` | `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Golden Master checkpoint |

## Related

- [PCR Drift Detection](PCR_DRIFT.md)
- [DHT Federation](DHT_FEDERATION.md)
