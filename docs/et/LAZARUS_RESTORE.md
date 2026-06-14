# Lazarus tuuma automaatne taastamine (v32.0)

Kui **PCR triivi tuvastus** käivitab karantiini (v31.0), automatiseerib **Lazarus deemon** **puhastoa taastamise**: laadi kinnitatud Golden Master DHT konsensusest, rakenda tuuma olek uuesti ja jätkake arvutust.

## Voog

```
PCR drift detected
  --> emergency_quarantine() (stop containers)
  --> perform_rollback() (kexec attempt)
  --> LazarusRestore.auto_restore()
        1. Fetch golden_master from checkpoint / DHT
        2. apply_state() — re-inject registry + quorum
        3. Resume compute
```

## Moodul (`lazarus_restore.py`)

| Meetod | Eesmärk |
|--------|---------|
| `auto_restore(kernel_ref)` | Täielik puhastoa taastamine |
| `get_golden_master(kernel_ref)` | Laadi kontrollpunktist või DHT-st |
| `apply_state(kernel_ref, golden)` | Aatomiline oleku taasesitus |
| `save_checkpoint(kernel_ref)` | Salvesta kuldne olek kettale |
| `schedule_auto_restore(kernel_ref)` | Asünkroonne taastamine pärast karantiini |

Kontrollpunkt: `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json`

## HTTP API

### GET /lazarus/status

### POST /lazarus/restore

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```

## Keskkond

| Muutuja | Vaikimisi | Eesmärk |
|---------|-----------|---------|
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Automaatne taastamine pärast karantiini (`0` = arendus) |
| `UTAH_LAZARUS_CHECKPOINT_PATH` | `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Golden Master kontrollpunkt |

## Seotud

- [PCR triivi tuvastus](PCR_DRIFT.md)
- [DHT föderatsioon](DHT_FEDERATION.md)
