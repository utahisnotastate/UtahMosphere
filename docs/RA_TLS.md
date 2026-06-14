# RA-TLS Mesh Attestation (v30.0)

**Remote Attestation via TLS (RA-TLS)** plus **DHT-federated golden consensus** ensures UtahNetes mesh peers run authentic kernels on trusted TPM hardware before gossip sync is accepted.

## Global Attestation Topology

```
Tokyo Node                         Utah Root Node
     |                                    |
     |--- TLS + X.509 OID 1.3.6.1.4.1.99999 -->|
     |                                    |-- ra_tls_guard.verify_attestation()
     |                                    |-- quote_registry.is_valid_hardware()
     |<-------- mesh sync (if valid) -----|
```

Nodes do not trust IP addresses. They trust **Hardware Quotes** signed by the Utah-Kernel Root CA and listed in the registry.

## Components

| Module | Role |
|--------|------|
| `ra_tls_attest.py` | Generate quotes; attach to mesh gossip; verify peers |
| `ra_tls_guard.py` | CA pinning; X.509 OID extraction; UtahX ingress guard |
| `quote_registry.py` | Distributed ledger of `{hardware_id: public_quote}` |

## Generate Quote

```bash
curl http://127.0.0.1:8999/attestation/quote
```

**Response `200`:**

```json
{
  "hardware_id": "sha256-of-vibe-pcr-node",
  "ra_tls_quote": {
    "body": "{\"build\":\"omega-build-v30-federated-attested\",\"node_id\":\"host\",\"hardware_id\":\"...\",\"pcr0_digest\":\"...\",\"vibe_hash\":\"...\"}",
    "signature": "hmac-sha256-over-body",
    "ca_signature": "optional-rsa-over-body"
  }
}
```

Mesh broadcasts attach `ra_tls_quote` and replicate `quote_registry` via `RATLSAttestation.attach_to_message()`.

## UtahX Ingress (CA Pinning)

Before proxying `/app/{name}`, UtahX validates:

| Header | Purpose |
|--------|---------|
| `X-Utah-Hardware-ID` | Derived hardware fingerprint |
| `X-Utah-RATLS-Quote` | JSON quote payload |

Invalid or unregistered hardware receives **403** at the ingress layer when `UTAH_RA_TLS_GUARD_ENFORCE=1`.

## Verification

`RATLSAttestation.verify_mesh_message()` checks:

1. HMAC signature against `UTAH_KERNEL_ROOT_CA`
2. Hardware ID present in `quote_registry`
3. `ra_tls_guard.verify_quote_payload()` CA pinning
4. PCR0 digest matches local TPM measurement (when enforced)

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_RA_TLS_ENFORCE` | `1` | Reject mesh sync without valid quote (`0` = dev) |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress + CA pinning |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v30_root_ca` | Quote signing root |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus on peer quotes |

## Related

- [DHT-Federated Attestation](DHT_FEDERATION.md)
- [PCR Drift Detection](PCR_DRIFT.md)
- [Hardware Quote Registry](QUOTE_REGISTRY.md)
- [Capability Matrix](CAPABILITY_MATRIX.md)
