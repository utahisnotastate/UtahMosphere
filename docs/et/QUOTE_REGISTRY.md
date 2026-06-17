# Riistvara tsitaadi register (v32.0)

**Riistvara tsitaadi register** on UtahMosphere parve jaotatud tõe allikas kehtivate TPM riistvara sõrmejälgede jaoks. Sõlmed ei usalda IP-aadresse — nad usaldavad **riistvara tsitaate**, mida allkirjastab Utah-Kernel juur-CA ja mis on selles registris.

## Topoloogia

```
Node A (claim)                    Swarm peers
    |                                  |
    |-- seal vibe to PCR0 ------------>|
    |-- sign hardware quote ---------->|-- merge_remote()
    |-- register_node() -------------->|-- quote_registry in mesh payload
    |                                  |
Peer B connects via RA-TLS ----------> verify against registry
    |                                  |
UtahX ingress ----------------------> ra_tls_guard.verify_http_headers()
```

## Registriteenus (`quote_registry.py`)

| Meetod | Eesmärk |
|--------|---------|
| `register_node(hardware_id, public_quote, ...)` | Lisa sõlm pärast biomeetrilist claimi |
| `is_valid_hardware(hardware_id)` | Kontrolli aktiivset kirjet |
| `purge_node(hardware_id, reason)` | Karantiini kompromiteeritud riistvara |
| `merge_remote(remote_nodes)` | Replikeeri register mesh gossipist |
| `export_nodes()` | Täielik registri hetktõmmis |

Salvestus: `{UTAH_DATA_DIR}/quote_registry.json`

## RA-TLS kaitse (`ra_tls_guard.py`)

Rakendab **CA kinnitamist**. Ainult registreeritud Utah-Kernel CA allkirjastatud tsitaadiga sõlmed saavad liituda võrguga või läbida UtahX sissepääsu.

- X.509 OID `1.3.6.1.4.1.99999` kannab TPM tsitaati
- HTTP sissepääs: `X-Utah-Hardware-ID` + `X-Utah-RATLS-Quote` enne proksit

## Biomeetriline TPM seos (claim)

`"Claim node"` ajal: vibe-print → PCR0 → `hardware_id` → allkirjastatud tsitaat → `register_node()` → mesh levitab `quote_registry`.

## HTTP API

Vaata [API viide](API_REFERENCE.md): `GET /registry/quotes`, `POST /registry/purge`.

## Keskkond

| Muutuja | Vaikimisi | Eesmärk |
|---------|-----------|---------|
| `UTAH_QUOTE_REGISTRY_PATH` | `{UTAH_DATA_DIR}/quote_registry.json` | Registri salvestus |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX sissepääs + CA (`0` = dev) |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v34_root_ca` | Tsitaadi allkirjastamise juur |

Dev:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
```

## Seotud

- [Võimekuste maatriks](CAPABILITY_MATRIX.md)
- [API viide](API_REFERENCE.md)
