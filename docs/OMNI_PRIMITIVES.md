# Omni Primitives (v33.0)

Kernel **primitive tools** exposed to the Omni-Compiler and MCP agents—replacing infinite hardcoded GCP APIs with a small composable surface.

## Module (`omni_primitives.py`)

| Function | Purpose |
|----------|---------|
| `allocate_memory_silo(app_name)` | Reserve container namespace |
| `write_file_to_disk(path, content)` | Write under `UTAH_DATA_DIR` |
| `read_file_from_disk(path)` | Read sovereign files |
| `list_directory(path)` | List directory entries |
| `update_utahx_routing(domain, port)` | UtahX ingress manifest |
| `execute_subprocess(command)` | Sandboxed shell (`UTAH_OMNI_SUBPROCESS_ENFORCE`) |

`PRIMITIVE_TOOLS` exports OpenAI-compatible tool schemas for agentic loops.

## Related

- [Omni-Compiler](OMNI_COMPILER.md)
