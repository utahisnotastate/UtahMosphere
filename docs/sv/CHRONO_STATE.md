# Chrono-State (v34.0)

**Chrono-State** gör CI/CD-staging överflödigt. Innan Lazarus injicerar AI-genererad kod tar motorn en minnesögonblicksbild. Vid fel spolas tiden tillbaka — ofta före HTTP-timeout.

## Modul (`chrono_state.py`)

| Metod | Syfte |
|-------|-------|
| `execute_with_rewind()` | Spekulativ körning + återspolning |
| `snapshot_namespace()` | Djupkopia av modulens dict |
| `rewind_namespace()` | Återställ före mutation |

## HTTP API

### GET /chrono/status

```bash
curl http://127.0.0.1:8999/chrono/status
```

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_CHRONO_ENFORCE` | `1` | Chrono-återspolning (`0` = direkt körning) |

## Se även

- [UtahClaw](UTAH_CLAW.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
