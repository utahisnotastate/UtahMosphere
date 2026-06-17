# Kinematic Siphon (v34.0)

**Kinematic Siphon** делает Chrome/Electron излишними для клиентов UtahMosphere. Ядро стримит **Ghost Tune** — компактный бинарный протокол B-Web для прямой загрузки текстур GPU.

## HTTP API

### GET /siphon/ghost-tune

```bash
curl http://127.0.0.1:8999/siphon/ghost-tune --output ghost.tune
```

Возвращает `application/octet-stream` с заголовком `UTAH\x01`.

## См. также

- [Omni-Glass UI](OMNI_GLASS_UI.md)
