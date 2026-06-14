# Moteur de delta d'état entrelacé (v32.0)

La **synchronisation d'état entrelacée** ne transmet que le *delta mathématique* de l'état du registre — permettant aux nœuds mondiaux d'atteindre un état identique avec **<1 Ko de surcharge** au lieu de payloads complets.

## Module (`state_diff_engine.py`)

```python
delta = get_state_delta(local_state, remote_state)
merged = apply_state_delta(remote_state, delta)
```

| Fonction | Rôle |
|----------|------|
| `get_state_delta(local, remote)` | Delta minimal au niveau des clés |
| `apply_state_delta(base, delta)` | Reconstruire l'état synchronisé |
| `encode_delta(local, remote)` | Empaqueter delta + hachages pour le mesh |
| `state_hash(state)` | Empreinte SHA-256 canonique |
| `should_use_delta(local, remote)` | Utiliser le delta s'il est plus petit que le JSON complet |

## Intégration mesh

Le gossip UtahNetes envoie `registry_delta` au lieu du `registry` complet lorsque c'est plus efficace en bande passante. Les témoins valident `state_hash` avant fusion.

## Environnement

| Variable | Défaut | Rôle |
|----------|--------|------|
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Préférer la sync delta si plus petite |
| `UTAH_STATE_DIFF_MAX_BYTES` | `1024` | Taille max du payload delta |

## Voir aussi

- [Témoins de quorum](QUORUM_WITNESSES.md)
- [Restauration Lazarus](LAZARUS_RESTORE.md)
