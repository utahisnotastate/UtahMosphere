# Chrono-State (v34.0)

**Chrono-State** tekee CI/CD-stagingin tarpeettomaksi. Ennen Lazaruksen AI-koodin injektiota moottori ottaa moduulin muistista tilannekuvan. Epäonnistuessa aika kelataan taaksepäin — usein ennen HTTP-aikakatkaisua.

## Moduuli (`chrono_state.py`)

| Metodi | Tarkoitus |
|--------|-----------|
| `execute_with_rewind()` | Spekulatiivinen suoritus + kelaus |
| `snapshot_namespace()` | Moduulin dictin syväkopio |
| `rewind_namespace()` | Palautus ennen mutaatiota |

## HTTP API

### GET /chrono/status

```bash
curl http://127.0.0.1:8999/chrono/status
```

## Ympäristö

| Muuttuja | Oletus | Tarkoitus |
|----------|--------|-----------|
| `UTAH_CHRONO_ENFORCE` | `1` | Chrono-kelaus (`0` = suora suoritus) |

## Katso myös

- [UtahClaw](UTAH_CLAW.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
