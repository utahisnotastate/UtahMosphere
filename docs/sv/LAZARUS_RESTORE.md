# Lazarus-kärnans automatiska återställning (v32.0)

När **PCR-driftdetektering** utlöser karantän (v31.0) automatiserar **Lazarus-demonen** **renrumsåterställning**: hämta verifierad Golden Master från DHT-konsensus, återapplicera kärntillstånd och återuppta beräkning.

## Flöde

```
PCR drift detected
  --> emergency_quarantine() (stop containers)
  --> perform_rollback() (kexec attempt)
  --> LazarusRestore.auto_restore()
        1. Fetch golden_master from checkpoint / DHT
        2. apply_state() — re-inject registry + quorum
        3. Resume compute
```

## Modul (`lazarus_restore.py`)

| Metod | Syfte |
|-------|-------|
| `auto_restore(kernel_ref)` | Full renrumsåterställning |
| `get_golden_master(kernel_ref)` | Ladda från kontrollpunkt eller DHT |
| `apply_state(kernel_ref, golden)` | Atomisk tillståndsåterinstansiering |
| `save_checkpoint(kernel_ref)` | Spara gyllene tillstånd till disk |
| `schedule_auto_restore(kernel_ref)` | Asynkron återställning efter karantän |

Kontrollpunkt: `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json`

## HTTP API

### GET /lazarus/status

### POST /lazarus/restore

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Autoåterställning efter karantän (`0` = utveckling) |
| `UTAH_LAZARUS_CHECKPOINT_PATH` | `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Golden Master-kontrollpunkt |

## Relaterat

- [PCR-driftdetektering](PCR_DRIFT.md)
- [DHT-federation](DHT_FEDERATION.md)
