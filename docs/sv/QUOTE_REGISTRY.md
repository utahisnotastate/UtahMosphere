# Hårdvarucitatregister (v32.0)

**Hårdvarucitatregistret** är den distribuerade sanningen för giltiga TPM-hårdvaruavtryck i UtahMosphere-svärmen. Noder litar inte på IP-adresser — de litar på **hårdvarucitat** signerade av Utah-Kernel Root CA och registrerade i detta register.

## Topologi

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

## Registertjänst (`quote_registry.py`)

| Metod | Syfte |
|--------|-------|
| `register_node(hardware_id, public_quote, ...)` | Lägg till nod efter biometrisk claim |
| `is_valid_hardware(hardware_id)` | Kontrollera aktiv post |
| `purge_node(hardware_id, reason)` | Karantän för komprometterad hårdvara |
| `merge_remote(remote_nodes)` | Replikera från mesh gossip |
| `export_nodes()` | Full registerögonblicksbild |

Persistens: `{UTAH_DATA_DIR}/quote_registry.json`

## RA-TLS-vakt (`ra_tls_guard.py`)

**CA-fästning.** Endast noder med Utah-Kernel CA-citat i registret kan gå med i mesh eller passera UtahX ingress.

- X.509 OID `1.3.6.1.4.1.99999` bär TPM-citat
- HTTP: `X-Utah-Hardware-ID` + `X-Utah-RATLS-Quote` före proxy

## Biometrisk TPM-bindning (claim)

Vid `"Claim node"`: vibe-print → PCR0 → `hardware_id` → signerat citat → `register_node()` → mesh sprider `quote_registry`.

## HTTP API

Se [API-referens](API_REFERENCE.md): `GET /registry/quotes`, `POST /registry/purge`.

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_QUOTE_REGISTRY_PATH` | `{UTAH_DATA_DIR}/quote_registry.json` | Registerpersistens |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress + CA (`0` = dev) |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v32_root_ca` | Citatsigneringsrot |

Dev:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
```

## Relaterat

- [Kapacitetsmatris](CAPABILITY_MATRIX.md)
- [API-referens](API_REFERENCE.md)
