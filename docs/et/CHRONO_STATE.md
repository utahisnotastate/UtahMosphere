# Chrono-State täitmised (v34.0)

**Chrono-State** muudab CI/CD stagingi üleliigseks. Enne Lazarus AI-koodi süstimist teeb mootor mooduli mälu hetktõmmise. Kui mutatsioon viskab erandi, keritakse aeg tagasi — sageli enne HTTP aegumist.

## Moodul (`chrono_state.py`)

| Meetod | Eesmärk |
|--------|---------|
| `execute_with_rewind()` | Spekulatiivne täitmine + tagasikerimine |
| `snapshot_namespace()` | Mooduli dict sügavkopeerimine |
| `rewind_namespace()` | Taasta eelmutatsiooni olek |

## HTTP API

### GET /chrono/status

```bash
curl http://127.0.0.1:8999/chrono/status
```

## Keskkond

| Muutuja | Vaikimisi | Eesmärk |
|---------|-----------|---------|
| `UTAH_CHRONO_ENFORCE` | `1` | Luba chrono tagasikerimine (`0` = otsetäitmine) |

## Seotud

- [UtahClaw](UTAH_CLAW.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
