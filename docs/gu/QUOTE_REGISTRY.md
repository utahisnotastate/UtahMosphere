# Registro di Hardware Quote (v29.0)

I **Hardware Quote Registry** i fuente di veridåt distribuido para valid TPM hardware fingerprints gi i UtahMosphere swarm. Ti nódus ti siña confia IP addresses — siña confia **hardware quotes** signed by Utah-Kernel Root CA yan registered gi este na ledger.

## Topologia

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

## Registry Service (`quote_registry.py`)

| Method | Purpose |
|--------|---------|
| `register_node(hardware_id, public_quote, ...)` | Add node despues biometric claim |
| `is_valid_hardware(hardware_id)` | Check active entry |
| `purge_node(hardware_id, reason)` | Quarantine compromised hardware |
| `merge_remote(remote_nodes)` | Replicate from mesh gossip |
| `export_nodes()` | Full registry snapshot |

Persistence: `{UTAH_DATA_DIR}/quote_registry.json`

## RA-TLS Guard (`ra_tls_guard.py`)

**CA pinning.** Solo nodes con Utah-Kernel CA quote gi registry puede join mesh pat pass UtahX ingress.

- X.509 OID `1.3.6.1.4.1.99999` carries TPM quote
- HTTP: `X-Utah-Hardware-ID` + `X-Utah-RATLS-Quote` antes proxy

## Biometric-to-TPM Binding (claim)

Durante `"Claim node"`: vibe-print → PCR0 → `hardware_id` → signed quote → `register_node()` → mesh spreads `quote_registry`.

## HTTP API

Li'e [API Reference](API_REFERENCE.md): `GET /registry/quotes`, `POST /registry/purge`.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_QUOTE_REGISTRY_PATH` | `{UTAH_DATA_DIR}/quote_registry.json` | Registry persistence |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress + CA (`0` = dev) |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v29_root_ca` | Quote signing root |

Dev:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
```

## Relacionao

- [Matrisis Kapasidad](CAPABILITY_MATRIX.md)
- [API Reference](API_REFERENCE.md)
