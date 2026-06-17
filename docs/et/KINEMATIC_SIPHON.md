# Kinematic Siphon (v34.0)

**Kinematic Siphon** muudab Chrome/Electroni UtahMosphere klientides üleliigseks. Tuum voogedastab **Ghost Tune** — kompaktse B-Web binaarprotokolli Omni-Glass stseenigraafi kodeerimiseks otse GPU tekstuuri üleslaadimiseks.

## HTTP API

### GET /siphon/ghost-tune

```bash
curl http://127.0.0.1:8999/siphon/ghost-tune --output ghost.tune
```

Tagastab `application/octet-stream` magic päisega `UTAH\x01`.

## Seotud

- [Omni-Glass UI](OMNI_GLASS_UI.md)
