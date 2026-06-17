# Kinematic Siphon (v34.0)

The **Kinematic Siphon** obsoletes Chrome/Electron for UtahMosphere clients. Instead of HTML/JS, the kernel streams a **Ghost Tune**—a compact B-Web binary protocol encoding the Omni-Glass scene graph for direct GPU texture upload.

## Module (`utahclaw/kinematic_siphon.py`)

```python
from utahclaw.kinematic_siphon import kinematic_siphon

binary = kinematic_siphon.encode_scene_graph(omni_glass.export_manifold())
```

Native clients (`utah-core.exe`, ~5MB) decode the payload and paint pixels via WebGPU/WGPU—no DOM, no JS engine.

## HTTP API

### GET /siphon/ghost-tune

```bash
curl http://127.0.0.1:8999/siphon/ghost-tune --output ghost.tune
```

Returns `application/octet-stream` with magic header `UTAH\x01`.

## Related

- [Omni-Glass UI](OMNI_GLASS_UI.md)
