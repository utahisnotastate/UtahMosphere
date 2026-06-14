# Hardware Quote Registry (v30.0)

The **Hardware Quote Registry** is the distributed source of truth for valid TPM hardware fingerprints. **DHT-federated attestation** (v30.0) cross-verifies quotes against the golden measurement ledger in `dht_quote_registry.py`.

## Topology

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
| `register_node(hardware_id, public_quote, ...)` | Add node after biometric claim |
| `is_valid_hardware(hardware_id)` | Check active registry entry |
| `purge_node(hardware_id, reason)` | Quarantine compromised hardware |
| `merge_remote(remote_nodes)` | Replicate registry from mesh gossip |
| `export_nodes()` | Full registry snapshot for sync |

Persistence: `{UTAH_DATA_DIR}/quote_registry.json`

## RA-TLS Guard (`ra_tls_guard.py`)

Enforces **CA pinning**. Only nodes whose hardware quote is signed by the Utah-Kernel Root CA and present in the registry can join the mesh or pass UtahX ingress.

- X.509 custom OID `1.3.6.1.4.1.99999` carries the TPM quote (when `cryptography` is installed)
- HTTP ingress: `X-Utah-Hardware-ID` + `X-Utah-RATLS-Quote` headers validated before proxy

## Biometric-to-TPM Binding (Claim Flow)

During `"Claim node"`:

1. Capture acoustic MFCCs → vibe-print hash
2. Seal vibe-print to TPM PCR0 (`tpm_lock.py`)
3. Derive `hardware_id` from vibe + PCR0 + node identity
4. Sign hardware quote with kernel root CA
5. `register_node()` pushes entry to global registry
6. Mesh broadcasts include `quote_registry` for peer merge

## HTTP API

### GET /registry/quotes

List all registered hardware quotes.

```bash
curl http://127.0.0.1:8999/registry/quotes
```

**Response `200`:**

```json
{
  "nodes": {
    "abc123...": {
      "public_quote": "{\"body\":\"...\",\"signature\":\"...\"}",
      "vibe_hash": "64-char-sha256",
      "status": "active"
    }
  },
  "stats": {"active": 1, "purged": 0, "total": 1}
}
```

### POST /registry/purge

Purge compromised hardware. Root vibe holder only.

```bash
curl -X POST http://127.0.0.1:8999/registry/purge \
  -H "Content-Type: application/json" \
  -d '{"hardware_id": "abc...", "acoustic_hash": "root-vibe-64chars", "reason": "firmware tamper"}'
```

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `UTAH_QUOTE_REGISTRY_PATH` | `{UTAH_DATA_DIR}/quote_registry.json` | Registry persistence |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress + CA pinning (`0` = dev) |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v30_root_ca` | Quote signing root |
| `UTAH_KERNEL_ROOT_CA_PATH` | `/etc/utahmosphere/security/utah_root_ca.pem` | PEM public key for CA verify |

Dev skip all attestation layers:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
```

## Related

- [DHT-Federated Attestation](DHT_FEDERATION.md)
- [PCR Drift Detection](PCR_DRIFT.md)
- [RA-TLS Mesh Attestation](RA_TLS.md)
- [Capability Matrix](CAPABILITY_MATRIX.md)
