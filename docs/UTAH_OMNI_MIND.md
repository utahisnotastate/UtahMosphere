# Utah-Omni-Mind (v33.0)

**Utah-Omni-Mind** replaces OpenAI/Anthropic APIs with sovereign local inference powered by **UtahVidia**—ZEO-Shield sparse activation, Osmotic tensor routing, and Photonic context ingestion.

## Stack

| Component | Module | Role |
|-----------|--------|------|
| Execution core | `utahvidia.core.Engine` | Stream tokens from local weights |
| ZEO-Shield | `utahvidia.zeo_shield` | ~2% sparse activation |
| Osmotic Router | `utahvidia.osmotic` | Shard KV-cache to swarm peers |
| Photonic Bridge | `utahvidia.photonic_sim` | Zero-copy prompt ingest |
| Heuristic fallback | `omni_intent_heuristics` | Offline blueprint when no weights/API |

## Module (`utah_omni_mind.py`)

```python
from utah_omni_mind import omni_mind

raw_json = omni_mind.generate_intent_blueprint(system_prompt, user_intent)
```

## Model weights

Default path: `{UTAH_DATA_DIR}/models/utah-frontier-v1.safetensors`

Genesis bootstrap downloads quantized weights when `UTAH_OMNI_DOWNLOAD_MODEL=1`:

```bash
UTAH_OMNI_DOWNLOAD_MODEL=1 sudo bash bootstrap.sh
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_OMNI_PROVIDER` | `sovereign` | `sovereign` (local) or `openai` |
| `UTAH_OMNI_MODEL_PATH` | `{UTAH_DATA_DIR}/models/utah-frontier-v1.safetensors` | Local weights |
| `UTAH_ZEO_THRESHOLD` | `0.05` | ZEO-Shield activation cutoff |
| `UTAH_OSMOTIC_PEERS` | — | Comma-separated peer endpoints |

## Related

- [Omni-Compiler](OMNI_COMPILER.md)
- [MCP Omni-Bridge](MCP_OMNI_BRIDGE.md)
