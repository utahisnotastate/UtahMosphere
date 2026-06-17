# Omni-Glass UI (v34.0)

**Omni-Glass** remplace les logs terminal et Datadog par un manifold visuel en temps réel — vecteurs de pensée Omni-Mind, chemins de recherche UtahClaw et mutations AST Lazarus.

## Manifold d'état

| Point de terminaison | Port | Rôle |
|---------------------|------|------|
| `GET /omni/glass` | 8999 | Événements + manifold JSON |
| `GET /manifold` | 9091 | Manifold complet |
| `GET /stream` | 9091 | Flux SSE (~60 FPS) |

```bash
curl http://127.0.0.1:8999/omni/glass
curl -N http://127.0.0.1:9091/stream
```

## Environnement

| Variable | Défaut | Rôle |
|----------|--------|------|
| `UTAH_OMNI_GLASS_STREAM` | `1` | Relais SSE sur le port 9091 |
| `UTAH_OMNI_GLASS_PORT` | `9091` | Port FluxRelay |

## Voir aussi

- [Kinematic Siphon](KINEMATIC_SIPHON.md)
- [UtahClaw](UTAH_CLAW.md)
