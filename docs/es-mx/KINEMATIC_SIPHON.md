# Kinematic Siphon (v34.0)

El **Kinematic Siphon** hace innecesarios Chrome/Electron para clientes UtahMosphere. El kernel transmite **Ghost Tune** — protocolo binario B-Web compacto para carga directa de texturas GPU.

## API HTTP

### GET /siphon/ghost-tune

```bash
curl http://127.0.0.1:8999/siphon/ghost-tune --output ghost.tune
```

Devuelve `application/octet-stream` con encabezado mágico `UTAH\x01`.

## Ver también

- [Omni-Glass UI](OMNI_GLASS_UI.md)
