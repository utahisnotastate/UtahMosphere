# Entanglat tillståndsdiff-motor (v32.0)

**Entanglad tillståndssynkronisering** överför endast den *matematiska deltan* av registertillståndet — globala noder når identiskt tillstånd med **<1 KB overhead** istället för fulla registerpayloads.

## Modul (`state_diff_engine.py`)

```python
delta = get_state_delta(local_state, remote_state)
merged = apply_state_delta(remote_state, delta)
```

| Funktion | Syfte |
|----------|-------|
| `get_state_delta(local, remote)` | Minimal nyckelnivå-delta |
| `apply_state_delta(base, delta)` | Rekonstruera synkat tillstånd |
| `encode_delta(local, remote)` | Paketera delta + hashar för mesh |
| `state_hash(state)` | SHA-256 kanoniskt tillståndsavtryck |
| `should_use_delta(local, remote)` | Använd delta när mindre än full JSON |

## Mesh-integration

UtahNetes-gossip skickar `registry_delta` istället för fullt `registry` när det är bandbreddseffektivt. Vittnesnoder validerar `state_hash` före sammanslagning.

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Föredra deltasynk när mindre |
| `UTAH_STATE_DIFF_MAX_BYTES` | `1024` | Max delta-payloadstorlek |

## Relaterat

- [Kvorumvittnen](QUORUM_WITNESSES.md)
- [Lazarus autoåterställning](LAZARUS_RESTORE.md)
