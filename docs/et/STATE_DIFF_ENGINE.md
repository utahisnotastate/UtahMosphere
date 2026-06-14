# Põimunud oleku-erinevuse mootor (v32.0)

**Põimunud oleku sünkroniseerimine** edastab ainult registri oleku *matemaatilise delta* — võimaldades globaalsetel sõlmedel jõuda identsesse olekusse **<1KB ülekoormusega** täielike registripayloadide asemel.

## Moodul (`state_diff_engine.py`)

```python
delta = get_state_delta(local_state, remote_state)
merged = apply_state_delta(remote_state, delta)
```

| Funktsioon | Eesmärk |
|------------|---------|
| `get_state_delta(local, remote)` | Minimaalne võtmetaseme erinevus |
| `apply_state_delta(base, delta)` | Rekonstrueeri sünkroniseeritud olek |
| `encode_delta(local, remote)` | Pakenda delta + räsid meshi jaoks |
| `state_hash(state)` | SHA-256 kanooniline oleku sõrmejälg |
| `should_use_delta(local, remote)` | Kasuta deltat kui väiksem kui täielik JSON |

## Mesh integratsioon

UtahNetes gossip saadab `registry_delta` täieliku `registry` asemel kui see on ribalaiuse mõttes tõhusam. Tunnistajasõlmed valideerivad `state_hash` enne ühendamist.

## Keskkond

| Muutuja | Vaikimisi | Eesmärk |
|---------|-----------|---------|
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Eelista delta sünki kui väiksem |
| `UTAH_STATE_DIFF_MAX_BYTES` | `1024` | Maksimaalne delta payload |

## Seotud

- [Kvoorumi tunnistajad](QUORUM_WITNESSES.md)
- [Lazarus automaatne taastamine](LAZARUS_RESTORE.md)
