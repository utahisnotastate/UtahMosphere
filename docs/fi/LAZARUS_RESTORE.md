# Lazarus-ytimen automaattinen palautus (v32.0)

Kun **PCR-poikkeaman tunnistus** laukaisee karanteenin (v31.0), **Lazarus-deemoni** automatisoi **puhdashuonepalautuksen**: hae vahvistettu Golden Master DHT-konsensuksesta, käytä ytimen tila uudelleen ja jatka laskentaa.

## Kulku

```
PCR drift detected
  --> emergency_quarantine() (stop containers)
  --> perform_rollback() (kexec attempt)
  --> LazarusRestore.auto_restore()
        1. Fetch golden_master from checkpoint / DHT
        2. kexec -l /boot/vmlinuz-verified
        3. apply_state() — re-inject registry + quorum
        3. Resume compute
```

## Moduuli (`lazarus_restore.py`)

| Metodi | Tarkoitus |
|--------|-----------|
| `auto_restore(kernel_ref)` | Täysi puhdashuonepalautus |
| `get_golden_master(kernel_ref)` | Lataa tarkistuspisteestä tai DHT:stä |
| `apply_state(kernel_ref, golden)` | Atomihinen tilan uudelleensovellus |
| `save_checkpoint(kernel_ref)` | Tallenna kultainen tila levylle |
| `schedule_auto_restore(kernel_ref)` | Asynkroninen palautus karanteenin jälkeen |

Tarkistuspiste: `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json`

## HTTP API

### GET /lazarus/status

### POST /lazarus/restore

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```

## Ympäristö

| Muuttuja | Oletus | Tarkoitus |
|----------|--------|-----------|
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Golden Master + kexec-atomipalautus (`0` = kehitys) |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec palautuksen aikana (`0` = kehitys) |
| `UTAH_LAZARUS_KEXEC_KERNEL` | `/boot/vmlinuz-verified` | Vahvistettu palautusydin |
| `UTAH_LAZARUS_KEXEC_INITRD` | `/boot/initramfs-verified` | Vahvistettu initramfs |
| `UTAH_LAZARUS_CHECKPOINT_PATH` | `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Golden Master -tarkistuspiste |

## Liittyvät

- [PCR-poikkeaman tunnistus](PCR_DRIFT.md)
- [DHT-federointi](DHT_FEDERATION.md)
