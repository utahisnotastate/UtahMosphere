# Kinematic Siphon (v34.0)

Le **Kinematic Siphon** rend Chrome/Electron superflus pour les clients UtahMosphere. Le noyau diffuse un **Ghost Tune** — protocole binaire B-Web compact pour chargement direct de textures GPU.

## API HTTP

### GET /siphon/ghost-tune

```bash
curl http://127.0.0.1:8999/siphon/ghost-tune --output ghost.tune
```

Retourne `application/octet-stream` avec l'en-tête magique `UTAH\x01`.

## Voir aussi

- [Omni-Glass UI](OMNI_GLASS_UI.md)
