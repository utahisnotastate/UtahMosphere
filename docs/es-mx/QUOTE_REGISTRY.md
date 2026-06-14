# Registro de citas de hardware (v32.0)

El **registro de citas de hardware** es la fuente de verdad distribuida de huellas TPM válidas en el enjambre UtahMosphere. Los nodos no confían en direcciones IP — confían en **citas de hardware** firmadas por la CA raíz Utah-Kernel y registradas en este ledger.

## Topología

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

## Servicio de registro (`quote_registry.py`)

| Método | Propósito |
|--------|-----------|
| `register_node(hardware_id, public_quote, ...)` | Agregar nodo tras claim biométrico |
| `is_valid_hardware(hardware_id)` | Verificar entrada activa |
| `purge_node(hardware_id, reason)` | Cuarentena de hardware comprometido |
| `merge_remote(remote_nodes)` | Replicar desde gossip de malla |
| `export_nodes()` | Instantánea completa del registro |

Persistencia: `{UTAH_DATA_DIR}/quote_registry.json`

## Guardia RA-TLS (`ra_tls_guard.py`)

**Fijación de CA.** Solo nodos con cita Utah-Kernel CA en el registro pueden unirse a la malla o pasar el ingress UtahX.

- OID X.509 `1.3.6.1.4.1.99999` transporta la cita TPM
- HTTP: encabezados `X-Utah-Hardware-ID` + `X-Utah-RATLS-Quote` antes del proxy

## Vinculación biométrica a TPM (claim)

En `"Claim node"`: vibe-print → PCR0 → `hardware_id` → cita firmada → `register_node()` → la malla difunde `quote_registry`.

## API HTTP

Ver [Referencia API](API_REFERENCE.md): `GET /registry/quotes`, `POST /registry/purge`.

## Variables de entorno

| Variable | Predeterminado | Propósito |
|----------|----------------|-----------|
| `UTAH_QUOTE_REGISTRY_PATH` | `{UTAH_DATA_DIR}/quote_registry.json` | Persistencia del registro |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | Ingress UtahX + CA (`0` = dev) |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v32_root_ca` | Raíz de firma de citas |

Dev:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
```

## Relacionado

- [Matriz de capacidades](CAPABILITY_MATRIX.md)
- [Referencia API](API_REFERENCE.md)
