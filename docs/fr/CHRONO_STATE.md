# Chrono-State (v34.0)

**Chrono-State** rend le staging CI/CD obsolète. Avant l'injection de code IA par Lazarus, le moteur capture un instantané mémoire du module. En cas d'échec, le temps est rembobiné — souvent avant le timeout HTTP.

## Module (`chrono_state.py`)

| Méthode | Rôle |
|---------|------|
| `execute_with_rewind()` | Exécution spéculative + rembobinage |
| `snapshot_namespace()` | Copie profonde du dict du module |
| `rewind_namespace()` | Restauration pré-mutation |

## API HTTP

### GET /chrono/status

```bash
curl http://127.0.0.1:8999/chrono/status
```

## Environnement

| Variable | Défaut | Rôle |
|----------|--------|------|
| `UTAH_CHRONO_ENFORCE` | `1` | Rembobinage chrono (`0` = exécution directe) |

## Voir aussi

- [UtahClaw](UTAH_CLAW.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
