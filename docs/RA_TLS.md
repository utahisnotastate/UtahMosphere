# RA-TLS Mesh Attestation (v28.0)

Remote Attestation TLS (RA-TLS) ensures UtahNetes mesh peers run authentic UtahMosphere kernels on trusted TPM hardware before gossip sync is accepted.

## Flow

```
Peer A                          Peer B
  |                               |
  |-- MESH_SYNC + ra_tls_quote -->|
  |                               |-- verify_peer_quote()
  |                               |-- verify mesh_signature
  |<-------- registry merge -------|
```

## Generate Quote

```bash
curl http://127.0.0.1:8999/attestation/quote
```

**Response:**

```json
{
  "ra_tls_quote": {
    "body": "{\"build\":\"omega-build-v28-attested\",\"node_id\":\"host\",\"pcr0_digest\":\"...\"}",
    "signature": "hmac-sha256-over-body"
  }
}
```

Mesh broadcasts attach `ra_tls_quote` automatically via `ra_tls_attest.RATLSAttestation`.

## Verification

`RATLSAttestation.verify_mesh_message()` checks:

1. HMAC signature against `UTAH_KERNEL_ROOT_CA`
2. Kernel build ID in quote body
3. PCR0 digest matches local TPM measurement (when enforced)

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_RA_TLS_ENFORCE` | `1` | Reject mesh sync without valid quote (`0` = dev) |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v28_root_ca` | Quote signing root |

## Related

- [Hardware Attestation](ATTESTATION.md)
- [TPM Locker](../tpm_lock.py)
- [Capability Matrix](CAPABILITY_MATRIX.md)
