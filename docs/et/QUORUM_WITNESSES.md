# Mitmeregiooni kvoorumi tunnistajad (v32.0)

**Tunnistajasõlmed** on kerged piirkondlikud vaatlejad, mis hoiavad parve konsensuse krüptograafilisi räsisid. Kui piirkond (nt US-East) kaotab selgrooühenduse, toimivad **Okeaania** ja **Euroopa** tunnistajad vahekohtunikena — säilitades parve terviklikkuse ilma tsentraliseeritud juhtimiseta.

## Arhitektuur

```
US-East Node (partitioned)     Witness Layer
        |                           |
        |-- state_hash ------------>|-- us-east witness
        |                           |-- eu-west witness
        |                           |-- oceania-apac witness
        |                           |-- asia-east witness
        |<-- quorum confirmed ------|   (>51% must agree)
```

## Moodul (`quorum_witness.py`)

| Meetod | Eesmärk |
|--------|---------|
| `get_consensus(proposed_state_hash)` | >50% tunnistajatest peab räsi kinnitama |
| `ping_and_verify(hash)` | Piirkondlik HTTP ping tunnistajale |
| `record_local_witness(hash)` | Kohalik vahekoht kui kaugühendus puudub |
| `export_witnesses()` | Piirkondlik tunnistaja olek |

Vaikimisi piirkonnad: `us-east`, `eu-west`, `oceania-apac`, `asia-east`

## HTTP API

### GET /witness/status

```bash
curl http://127.0.0.1:8999/witness/status
```

## Keskkond

| Muutuja | Vaikimisi | Eesmärk |
|---------|-----------|---------|
| `UTAH_WITNESS_ENFORCE` | `1` | Nõua tunnistaja kvoorumit (`0` = arendus) |
| `UTAH_WITNESS_THRESHOLD` | `0.51` | Minimaalne häälte suhe |
| `UTAH_WITNESS_NODES` | 3 vaikimisi | Komaeraldusega tunnistaja lõpp-punktid |

## Seotud

- [Föderatiivne kvoorumi konsensus](QUORUM_CONSENSUS.md)
- [Oleku-erinevuse mootor](STATE_DIFF_ENGINE.md)
