# Kinematic Siphon (v34.0)

**Kinematic Siphon** tekee Chrome/Electronista tarpeettoman UtahMosphere-asiakkaille. Ydin striimaa **Ghost Tune** -binääriprotokollan B-Web-skenografiasta suoraan GPU-tekstuurilataukseen.

## HTTP API

### GET /siphon/ghost-tune

```bash
curl http://127.0.0.1:8999/siphon/ghost-tune --output ghost.tune
```

Palauttaa `application/octet-stream` magic-otsikolla `UTAH\x01`.

## Katso myös

- [Omni-Glass UI](OMNI_GLASS_UI.md)
