# Restauración automática del núcleo Lazarus (v32.0)

Cuando la **detección de deriva PCR** activa cuarentena (v31.0), el **demonio Lazarus** automatiza la **restauración en sala limpia**: obtener el Golden Master verificado del consenso DHT, reaplicar el estado del núcleo y reanudar el cómputo.

## Flujo

```
PCR drift detected
  --> emergency_quarantine() (stop containers)
  --> perform_rollback() (kexec attempt)
  --> LazarusRestore.auto_restore()
        1. Fetch golden_master from checkpoint / DHT
        2. apply_state() — re-inject registry + quorum
        3. Resume compute
```

## Módulo (`lazarus_restore.py`)

| Método | Propósito |
|--------|-----------|
| `auto_restore(kernel_ref)` | Restauración completa en sala limpia |
| `get_golden_master(kernel_ref)` | Cargar desde punto de control o DHT |
| `apply_state(kernel_ref, golden)` | Reinstanciación atómica del estado |
| `save_checkpoint(kernel_ref)` | Persistir estado dorado en disco |
| `schedule_auto_restore(kernel_ref)` | Restauración asíncrona tras cuarentena |

Punto de control: `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json`

## API HTTP

### GET /lazarus/status

### POST /lazarus/restore

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```

## Entorno

| Variable | Predeterminado | Propósito |
|----------|----------------|-----------|
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Restauración automática tras cuarentena (`0` = desarrollo) |
| `UTAH_LAZARUS_CHECKPOINT_PATH` | `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Punto de control Golden Master |

## Relacionado

- [Detección de deriva PCR](PCR_DRIFT.md)
- [Federación DHT](DHT_FEDERATION.md)
