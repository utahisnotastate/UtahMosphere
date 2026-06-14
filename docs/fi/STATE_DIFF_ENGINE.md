# Kietoutunut tilan erotusmoottori (v32.0)

**Kietoutunut tilan synkronointi** lähettää vain rekisteritilan *matemaattisen deltan* — globaalit solmut saavuttavat identtisen tilan **<1 kt ylikuormituksella** täyden rekisterin sijaan.

## Moduuli (`state_diff_engine.py`)

```python
delta = get_state_delta(local_state, remote_state)
merged = apply_state_delta(remote_state, delta)
```

| Funktio | Tarkoitus |
|---------|-----------|
| `get_state_delta(local, remote)` | Minimaalinen avaintason ero |
| `apply_state_delta(base, delta)` | Rakenna synkronoitu tila |
| `encode_delta(local, remote)` | Pakkaa delta + tiivisteet meshiin |
| `state_hash(state)` | SHA-256 kanoninen tilan sormenjälki |
| `should_use_delta(local, remote)` | Käytä deltaa jos pienempi kuin koko JSON |

## Mesh-integraatio

UtahNetes-gossip lähettää `registry_delta` täyden `registry`-payloadin sijaan kun se on kaistanleveyden kannalta tehokkaampaa. Todistajasolmut validoivat `state_hash` ennen yhdistämistä.

## Ympäristö

| Muuttuja | Oletus | Tarkoitus |
|----------|--------|-----------|
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Suosi deltasynkkiä kun pienempi |
| `UTAH_STATE_DIFF_MAX_BYTES` | `1024` | Deltapayloadin maksimikoko |

## Liittyvät

- [Kvoorumitodistajat](QUORUM_WITNESSES.md)
- [Lazarus-automaattinen palautus](LAZARUS_RESTORE.md)
