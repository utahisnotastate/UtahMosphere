# UtahClaw Ambient Runner (v34.0)

**UtahClaw** est le subconscient compilé d'UtahMosphere — un démon ambient non bloquant qui comble les **vides épistémiques** lorsque l'Omni-Compiler rencontre des capacités inconnues (Stripe GraphQL, Twilio, nouvelles API).

## Topologie

```
Intention non résolue → EpistemicVoid
        |
        v
[UtahClaw Ambient Runner]
   /        |        \
Web/DHT   Mémoire       Bac à sable
scraper   holographique   compilateur
        |
[Outil MCP forgé → injection à chaud Lazarus]
```

## Modules (`utahclaw/`)

| Module | Rôle |
|--------|------|
| `ambient_runner.py` | Recherche asynchrone + forge d'outils MCP |
| `holographic_memory.py` | Motifs d'interférence conceptuelle |
| `epistemic_void.py` | Exception `EpistemicVoid` + détection |
| `kinematic_siphon.py` | Encodage binaire Ghost Tune B-Web |
| `service.py` | HTTP fast-socket sur le port **9090** |

## API HTTP

### POST /claw/void (noyau, port 8999)

```bash
curl -X POST http://127.0.0.1:8999/claw/void \
  -H "Content-Type: application/json" \
  -d '{"concept": "Integrate with Stripe GraphQL API"}'
```

### GET /claw/status

Recherches en attente, outils forgés, statistiques de mémoire holographique.

## Intégration Omni-Compiler

Lorsque l'intention correspond aux mots-clés de vide (`stripe`, `graphql`, `twilio`), `omni_compiler.py` délègue à UtahClaw.

## Environnement

| Variable | Défaut | Rôle |
|----------|--------|------|
| `UTAH_CLAW_ENFORCE` | `1` | Activer le runner (`0` = dev) |
| `UTAH_CLAW_PORT` | `9090` | Fast-socket UtahClaw |
| `UTAH_CLAW_TOOLS_DIR` | `{UTAH_DATA_DIR}/mcp_tools` | Outils MCP forgés |

## Voir aussi

- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [Chrono-State](CHRONO_STATE.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
