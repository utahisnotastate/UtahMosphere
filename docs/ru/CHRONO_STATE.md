# Chrono-State (v34.0)

**Chrono-State** делает CI/CD staging излишним. Перед инъекцией AI-кода Lazarus движок снимает снимок памяти модуля. При сбое мутации время откатывается — часто до таймаута HTTP.

## Модуль (`chrono_state.py`)

| Метод | Назначение |
|-------|------------|
| `execute_with_rewind()` | Спекулятивное выполнение + откат |
| `snapshot_namespace()` | Глубокая копия dict модуля |
| `rewind_namespace()` | Восстановление до мутации |

## HTTP API

### GET /chrono/status

```bash
curl http://127.0.0.1:8999/chrono/status
```

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `UTAH_CHRONO_ENFORCE` | `1` | Откат chrono (`0` = прямое выполнение) |

## См. также

- [UtahClaw](UTAH_CLAW.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
