# Monialueinen kvoorumitodistajat (v32.0)

**Todistajasolmut** ovat kevyitä alueellisia tarkkailijoita, jotka pitävät parven konsensuksen kryptografisia tiivisteitä. Kun alue (esim. US-East) menettää yhteysreitin, **Oseanian**, **Euroopan** ja **Aasian** todistajat toimivat välimiehinä — säilyttäen parven eheyden ilman keskitettyä ohjausta.

## Arkkitehtuuri

```
US-East Node (partitioned)     Witness Layer
        |                           |
        |-- state_hash ------------>|-- us-east witness
        |                           |-- eu-west witness
        |                           |-- oceania-apac witness
        |                           |-- asia-east witness
        |<-- quorum confirmed ------|   (>51% must agree)
```

## Moduuli (`quorum_witness.py`)

| Metodi | Tarkoitus |
|--------|-----------|
| `get_consensus(proposed_state_hash)` | >50 % todistajista vahvistaa tiivisteen |
| `ping_and_verify(hash)` | Alueellinen HTTP-ping todistajalle |
| `record_local_witness(hash)` | Paikallinen välimies kun etä ei tavoitettavissa |
| `export_witnesses()` | Alueellinen todistajatila |

Oletusalueet: `us-east`, `eu-west`, `oceania-apac`, `asia-east`

## HTTP API

### GET /witness/status

```bash
curl http://127.0.0.1:8999/witness/status
```

## Ympäristö

| Muuttuja | Oletus | Tarkoitus |
|----------|--------|-----------|
| `UTAH_WITNESS_ENFORCE` | `1` | Vaadi todistajakvoorumia (`0` = kehitys) |
| `UTAH_WITNESS_THRESHOLD` | `0.51` | Minimäääräinen ääniosuus |
| `UTAH_WITNESS_NODES` | 4 oletusta | Pilkulla erotetut todistajapäätepisteet |

## Liittyvät

- [Federatiivinen kvoorumikonsensus](QUORUM_CONSENSUS.md)
- [Tilan erotusmoottori](STATE_DIFF_ENGINE.md)
