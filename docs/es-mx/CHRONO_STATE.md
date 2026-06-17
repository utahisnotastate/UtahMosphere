# Chrono-State (v34.0)

**Chrono-State** hace obsoleto el staging CI/CD. Antes de que Lazarus inyecte código IA, el motor captura un snapshot de memoria del módulo. Si la mutación falla, el tiempo se rebobina — a menudo antes del timeout HTTP.

## Módulo (`chrono_state.py`)

| Método | Propósito |
|--------|-----------|
| `execute_with_rewind()` | Ejecución especulativa + rebobinado |
| `snapshot_namespace()` | Copia profunda del dict del módulo |
| `rewind_namespace()` | Restaurar estado pre-mutación |

## API HTTP

### GET /chrono/status

```bash
curl http://127.0.0.1:8999/chrono/status
```

## Entorno

| Variable | Predeterminado | Propósito |
|----------|----------------|-----------|
| `UTAH_CHRONO_ENFORCE` | `1` | Rebobinado chrono (`0` = ejecución directa) |

## Ver también

- [UtahClaw](UTAH_CLAW.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
