# Témoins de quorum multi-régions (v32.0)

Les **nœuds témoins** sont des observateurs régionaux légers qui conservent les hachages cryptographiques du consensus de l'essaim. Lorsqu'une région (ex. US-East) perd la connectivité dorsale, les témoins en **Océanie**, **Europe** et **Asie** servent d'arbitres — préservant l'intégrité de l'essaim sans contrôle centralisé.

## Architecture

```
US-East Node (partitioned)     Witness Layer
        |                           |
        |-- state_hash ------------>|-- us-east witness
        |                           |-- eu-west witness
        |                           |-- oceania-apac witness
        |                           |-- asia-east witness
        |<-- quorum confirmed ------|   (>51% must agree)
```

## Module (`quorum_witness.py`)

| Méthode | Rôle |
|---------|------|
| `get_consensus(proposed_state_hash)` | >50 % des témoins doivent confirmer le hachage |
| `ping_and_verify(hash)` | Ping HTTP par région |
| `record_local_witness(hash)` | Arbitrage local si distant injoignable |
| `export_witnesses()` | État des témoins régionaux |

Régions par défaut : `us-east`, `eu-west`, `oceania-apac`, `asia-east`

## API HTTP

### GET /witness/status

```bash
curl http://127.0.0.1:8999/witness/status
```

## Environnement

| Variable | Défaut | Rôle |
|----------|--------|------|
| `UTAH_WITNESS_ENFORCE` | `1` | Exiger le quorum témoin (`0` = dev) |
| `UTAH_WITNESS_THRESHOLD` | `0.51` | Ratio minimal de votes |
| `UTAH_WITNESS_NODES` | 4 par défaut | Points de terminaison témoins |

## Voir aussi

- [Consensus quorum fédéré](QUORUM_CONSENSUS.md)
- [Moteur de delta d'état](STATE_DIFF_ENGINE.md)
