# Kinematic Siphon (v34.0)

**Kinematic Siphon** gör Chrome/Electron överflödigt för UtahMosphere-klienter. Kärnan strömmar **Ghost Tune** — ett kompakt B-Web-binärprotokoll för direkt GPU-texturuppladdning.

## HTTP API

### GET /siphon/ghost-tune

```bash
curl http://127.0.0.1:8999/siphon/ghost-tune --output ghost.tune
```

Returnerar `application/octet-stream` med magic-header `UTAH\x01`.

## Se även

- [Omni-Glass UI](OMNI_GLASS_UI.md)
