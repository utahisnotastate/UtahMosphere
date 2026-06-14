# Restauration automatique du noyau Lazarus (v32.0)

Lorsque la **détection de dérive PCR** déclenche une quarantaine (v31.0), le **démon Lazarus** automatise la **restauration en salle blanche** : récupérer le Golden Master vérifié depuis le consensus DHT, réappliquer l'état du noyau et reprendre le calcul.

## Flux

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

| Méthode | Rôle |
|---------|------|
| `auto_restore(kernel_ref)` | Restauration complète en salle blanche |
| `get_golden_master(kernel_ref)` | Chargement depuis point de contrôle ou DHT |
| `apply_state(kernel_ref, golden)` | Réinstanciation atomique de l'état |
| `save_checkpoint(kernel_ref)` | Persistance de l'état doré sur disque |
| `schedule_auto_restore(kernel_ref)` | Restauration asynchrone après quarantaine |

Point de contrôle : `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json`

## API HTTP

### GET /lazarus/status

### POST /lazarus/restore

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```

## Environnement

| Variable | Défaut | Rôle |
|----------|--------|------|
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Restauration auto après quarantaine (`0` = dev) |
| `UTAH_LAZARUS_CHECKPOINT_PATH` | `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Point de contrôle Golden Master |

## Voir aussi

- [Détection de dérive PCR](PCR_DRIFT.md)
- [Fédération DHT](DHT_FEDERATION.md)
