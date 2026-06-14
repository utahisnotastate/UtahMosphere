# Testigos de quórum multi-región (v32.0)

Los **nodos testigo** son observadores regionales ligeros que guardan los hashes criptográficos del consenso del enjambre. Si una región (p. ej., US-East) pierde conectividad troncal, los testigos en **Oceanía** y **Europa** actúan como desempates — manteniendo la integridad del enjambre sin control centralizado.

## Arquitectura

```
US-East Node (partitioned)     Witness Layer
        |                           |
        |-- state_hash ------------>|-- us-east witness
        |                           |-- eu-west witness
        |                           |-- oceania-apac witness
        |<-- quorum confirmed ------|   (>51% must agree)
```

## Módulo (`quorum_witness.py`)

| Método | Propósito |
|--------|-----------|
| `get_consensus(proposed_state_hash)` | >50 % de testigos deben confirmar el hash |
| `ping_and_verify(hash)` | Ping HTTP por región |
| `record_local_witness(hash)` | Desempate local si remoto no alcanzable |
| `export_witnesses()` | Estado regional de testigos |

Regiones predeterminadas: `us-east`, `eu-west`, `oceania-apac`

## API HTTP

### GET /witness/status

```bash
curl http://127.0.0.1:8999/witness/status
```

## Entorno

| Variable | Predeterminado | Propósito |
|----------|----------------|-----------|
| `UTAH_WITNESS_ENFORCE` | `1` | Exigir quórum testigo (`0` = desarrollo) |
| `UTAH_WITNESS_THRESHOLD` | `0.51` | Proporción mínima de votos |
| `UTAH_WITNESS_NODES` | 3 por defecto | Endpoints testigo separados por coma |

## Relacionado

- [Consenso de quórum federado](QUORUM_CONSENSUS.md)
- [Motor de delta de estado](STATE_DIFF_ENGINE.md)
