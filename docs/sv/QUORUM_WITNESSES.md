# Kvorumvittnen i flera regioner (v32.0)

**Vittnesnoder** är lätta regionala observatörer som håller kryptografiska hashar av svärmkonsensus. När en region (t.ex. US-East) förlorar ryggradsförbindelsen fungerar vittnen i **Oceanien** och **Europa** som domare — och bevarar svärmens integritet utan centraliserad styrning.

## Arkitektur

```
US-East Node (partitioned)     Witness Layer
        |                           |
        |-- state_hash ------------>|-- us-east witness
        |                           |-- eu-west witness
        |                           |-- oceania-apac witness
        |<-- quorum confirmed ------|   (>51% must agree)
```

## Modul (`quorum_witness.py`)

| Metod | Syfte |
|-------|-------|
| `get_consensus(proposed_state_hash)` | >50 % av vittnen måste bekräfta hashen |
| `ping_and_verify(hash)` | Regional HTTP-ping till vittne |
| `record_local_witness(hash)` | Lokal domare när fjärr är otillgänglig |
| `export_witnesses()` | Regional vittnesstatus |

Standardregioner: `us-east`, `eu-west`, `oceania-apac`

## HTTP API

### GET /witness/status

```bash
curl http://127.0.0.1:8999/witness/status
```

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_WITNESS_ENFORCE` | `1` | Kräv vittneskvorum (`0` = utveckling) |
| `UTAH_WITNESS_THRESHOLD` | `0.51` | Minsta röstandel |
| `UTAH_WITNESS_NODES` | 3 standard | Kommaseparerade vittnesändpunkter |

## Relaterat

- [Federerad kvorumkonsensus](QUORUM_CONSENSUS.md)
- [Tillståndsdiff-motor](STATE_DIFF_ENGINE.md)
