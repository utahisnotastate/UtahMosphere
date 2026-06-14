# Motor de delta de estado entrelazado (v32.0)

La **sincronización de estado entrelazado** transmite solo el *delta matemático* del estado del registro — permitiendo que nodos globales alcancen estado idéntico con **<1 KB de sobrecarga** en lugar de payloads completos.

## Módulo (`state_diff_engine.py`)

```python
delta = get_state_delta(local_state, remote_state)
merged = apply_state_delta(remote_state, delta)
```

| Función | Propósito |
|---------|-----------|
| `get_state_delta(local, remote)` | Diferencia mínima a nivel de clave |
| `apply_state_delta(base, delta)` | Reconstruir estado sincronizado |
| `encode_delta(local, remote)` | Empaquetar delta + hashes para mesh |
| `state_hash(state)` | Huella SHA-256 canónica |
| `should_use_delta(local, remote)` | Usar delta cuando sea menor que JSON completo |

## Integración mesh

El gossip UtahNetes envía `registry_delta` en lugar del `registry` completo cuando es más eficiente en ancho de banda. Los nodos testigo validan `state_hash` antes de fusionar.

## Entorno

| Variable | Predeterminado | Propósito |
|----------|----------------|-----------|
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Preferir sync delta cuando sea menor |
| `UTAH_STATE_DIFF_MAX_BYTES` | `1024` | Tamaño máximo del payload delta |

## Relacionado

- [Testigos de quórum](QUORUM_WITNESSES.md)
- [Restauración Lazarus](LAZARUS_RESTORE.md)
