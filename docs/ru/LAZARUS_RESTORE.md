# Автовосстановление ядра Lazarus (v32.0)

Когда **обнаружение дрейфа PCR** запускает карантин (v31.0), **демон Lazarus** автоматизирует **восстановление в чистой комнате**: загрузка проверенного Golden Master из DHT-консенсуса, повторное применение состояния ядра и возобновление вычислений.

## Поток

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

## Модуль (`lazarus_restore.py`)

| Метод | Назначение |
|-------|------------|
| `auto_restore(kernel_ref)` | Полное восстановление в чистой комнате |
| `get_golden_master(kernel_ref)` | Загрузка из контрольной точки или DHT |
| `apply_state(kernel_ref, golden)` | Атомарное восстановление состояния |
| `save_checkpoint(kernel_ref)` | Сохранение золотого состояния на диск |
| `schedule_auto_restore(kernel_ref)` | Асинхронное восстановление после карантина |

Контрольная точка: `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json`

## HTTP API

### GET /lazarus/status

### POST /lazarus/restore

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Golden Master + атомный kexec (`0` = разработка) |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec при восстановлении (`0` = разработка) |
| `UTAH_LAZARUS_KEXEC_KERNEL` | `/boot/vmlinuz-verified` | Проверенное ядро восстановления |
| `UTAH_LAZARUS_KEXEC_INITRD` | `/boot/initramfs-verified` | Проверенный initramfs |
| `UTAH_LAZARUS_CHECKPOINT_PATH` | `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Контрольная точка Golden Master |

## См. также

- [Обнаружение дрейфа PCR](PCR_DRIFT.md)
- [DHT-федерация](DHT_FEDERATION.md)
