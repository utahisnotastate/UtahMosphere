# API Reference

Base URL (default): `http://127.0.0.1:8999`

All responses are JSON unless noted.

---

## GET /health

Liveness probe for load balancers and monitoring.

**Response `200`:**

```json
{
  "status": "healthy",
  "node": "my-hostname",
  "version": "29.0",
  "build": "omega-build-v29-remote-attested",
  "attestation": {
    "tpm_present": false,
    "provisioned": false,
    "sealed": false,
    "enforce": true,
    "tpm_lock": {"sealed": false, "binding_ok": true, "enforce": true},
    "ra_tls": {"enforce": true, "kernel_root_ca": "utahmosphere_omega_build_v29_root_ca", "registry": {"active": 1, "purged": 0, "total": 1}},
    "quote_registry": {"active": 1, "purged": 0, "total": 1}
  }
}
```

**Example:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /attestation/quote

Issue an RA-TLS TPM quote for UtahNetes mesh peer verification.

**Response `200`:**

```json
{
  "hardware_id": "sha256-hardware-fingerprint",
  "ra_tls_quote": {
    "body": "{\"build\":\"omega-build-v29-remote-attested\",\"node_id\":\"my-host\",\"hardware_id\":\"...\",\"pcr0_digest\":\"...\",\"vibe_hash\":\"...\"}",
    "signature": "hmac-sha256-hex",
    "ca_signature": "optional-rsa-hex"
  }
}
```

See [RA-TLS Mesh Attestation](RA_TLS.md) and [Hardware Quote Registry](QUOTE_REGISTRY.md).

---

## GET /registry/quotes

Export the global hardware quote registry (active and purged entries).

**Response `200`:**

```json
{
  "nodes": {
    "abc123...": {
      "public_quote": "{\"body\":\"...\",\"signature\":\"...\"}",
      "vibe_hash": "64-char-sha256",
      "pcr_digest": "...",
      "node_id": "my-host",
      "status": "active",
      "registered_at": 1718323200.0
    }
  },
  "stats": {"active": 1, "purged": 0, "total": 1}
}
```

```bash
curl http://127.0.0.1:8999/registry/quotes
```

---

## POST /registry/purge

Purge a compromised hardware ID from the global registry. Root vibe holder only.

**Request body:**

```json
{
  "hardware_id": "sha256-hardware-fingerprint",
  "acoustic_hash": "root-vibe-hash-64chars",
  "reason": "firmware tamper"
}
```

**Response `200`:**

```json
{"status": "purged", "hardware_id": "abc123..."}
```

---

## GET /nonce

Issue a fresh voice-command nonce. Required after node claim when `UTAH_NONCE_ENFORCE=1` (default).

**Response `200`:**

```json
{
  "nonce": 1718323200,
  "window_sec": 30,
  "signature_hint": "HMAC-SHA256(acoustic_hash, f'{nonce}:{transcript}')"
}
```

**Example:**

```bash
curl http://127.0.0.1:8999/nonce
```

---

## GET /status

Operational snapshot: UI state, deployed tenants, and whether the node has been claimed.

**Response `200`:**

```json
{
  "ui_state": {
    "node_status": "Active [Sovereign Core v25.0]",
    "active_workloads": 1,
    "last_voice_command": "deploy application my-app",
    "cluster_health": "Resilient",
    "mutation_count": 0
  },
  "tenants": ["my-app"],
  "claimed": true,
  "authorized_nodes": ["abc123..."],
  "swarm_peers": 2,
  "tycoon": {
    "pending": 0,
    "settled_invoices": 1,
    "swept_funds": 5000,
    "settlement_mode": "auto",
    "mempool_failover_nodes": [
      {"region": "us-global", "url": "https://mempool.space/api"},
      {"region": "eu-signet", "url": "https://mempool.space/signet/api"},
      {"region": "global-blockstream", "url": "https://blockstream.info/api"},
      {"region": "oceania-apac", "url": "https://mempool.space/testnet/api"}
    ]
  },
  "attestation": {
    "tpm_present": false,
    "provisioned": false,
    "sealed": false,
    "enforce": true
  }
}
```

---

## POST /command

Execute a voice intent programmatically. Same payload the Voice Bridge sends.

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `transcript` | string | Yes | Spoken command (case-insensitive) |
| `acoustic_hash` | string | Yes | 64-char SHA-256 vibe-print hash |
| `nonce` | integer | After claim | Server-issued timestamp from `GET /nonce` |
| `command_signature` | string | After claim | `HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")` — alias: `signature` |
| `request_signature` | string | No | Optional AuthGuard HMAC for delegated nodes |

**Response `200`:**

```json
{
  "status": "manifested",
  "response": "Application successfully anchored into UtahContainerEngine loop on workspace port 8200."
}
```

### Supported transcripts

| Intent | Transcript example |
|--------|-------------------|
| Claim node | `"Claim node"` |
| Authorize node | `"authorize node <64-char-vibe-hash>"` |
| Deploy app | `"deploy application hello"` or `"manifest app hello"` |
| Patch app | `"patch app hello to add feature x"` |
| Status | `"status grid"` |

**Claim node (first run):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Claim node", "acoustic_hash": "abc123..."}'
```

**Deploy app (open mode — before claim, any hash accepted):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "deploy application hello", "acoustic_hash": "0000000000000000000000000000000000000000000000000000000000000000"}'
```

**Voice Bridge v27.0** calls `GET /nonce` and signs automatically. Manual signing:

```python
from voice_bridge_signed import get_signed_payload
payload = get_signed_payload("deploy application hello", acoustic_hash)
```

**After claim:** `acoustic_hash` must match root or `authorized_nodes[]`, and `nonce` + `command_signature` must be valid, or the kernel returns:

```json
{
  "status": "manifested",
  "response": "Access Denied. Biological signature does not match the Akashic Record."
}
```

---

## GET /app/{app_name}

Access a deployed tenant application. Gated by Utah-Tycoon payment authorization.

**Headers:**

| Header | Description |
|--------|-------------|
| `X-Client-ID` | Optional client identifier (defaults to client IP) |
| `X-Utah-Hardware-ID` | RA-TLS hardware fingerprint (ingress attestation) |
| `X-Utah-RATLS-Quote` | JSON RA-TLS quote payload |

When `UTAH_RA_TLS_GUARD_ENFORCE=1`, missing or invalid attestation headers return **403** before proxy.

### Unpaid client — Response `402 Payment Required`

```json
{
  "error": "Payment Required for UtahContainer Execution",
  "payment_address": "bc1q_utah_ephemeral_a1b2c3d4e5f6",
  "amount_sats": 5000,
  "message": "Transmit value to unlock silicon processing path."
}
```

Invoices auto-settle after ~60 seconds in the current simulation.

### Paid client — Response `200`

UtahX proxies the request to the UtahContainerEngine backend on the tenant port. Response body is the handler JSON output.

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## PUT/POST /s3/{bucket}/{key}

Write object to Utah S3 Mesh (local NVMe storage).

**Headers (optional):**

| Header | Description |
|--------|-------------|
| `X-Utah-Tenant-ID` | Tenant identifier |
| `X-Utah-Signature` | HMAC-SHA256 of `{tenant_id}:{path}` |

**Example:**

```bash
curl -X PUT http://127.0.0.1:8999/s3/my-data/file.txt \
  -H "Content-Type: text/plain" \
  --data-binary "Hello Utah"
```

---

## GET /s3/{bucket}/{key}

Read object. Returns raw bytes. Use `GET /s3/{bucket}/prefix*` to list.

```bash
curl http://127.0.0.1:8999/s3/my-data/file.txt
```

---

## POST /rds/write

Write key-value record to Utah RDS Ledger.

**Request body:**

```json
{"key": "user:123", "value": {"name": "Alice", "score": 9000}}
```

**Response `200`:**

```json
{"key": "user:123", "status": "written", "epoch": 1718280000.0}
```

---

## GET /rds/read/{key}

Read record by key.

```bash
curl http://127.0.0.1:8999/rds/read/user:123
```

---

## POST /lambda/{function_name}/invoke

Invoke Utah Lambda handler (no container image pull).

**Request body:** JSON event passed to `handler(event, context)`

```bash
curl -X POST http://127.0.0.1:8999/lambda/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "General 23"}'
```

**Response `200`:**

```json
{"result": {"message": "Hello General 23 from Utah Lambda!"}}
```

---

## POST /app/unlock

Submit a payment unlock request. Tycoon polls mempool.space (or electrum-server) for payment finality. Dev addresses (`bc1q_utah_*`) use timed settlement in `auto` mode.

**Request body:**

```json
{
  "app_name": "hello",
  "client_id": "demo-client",
  "payment_tx": "optional-tx-hint",
  "amount_sats": 5000
}
```

**Response `202`:**

```json
{
  "status": "pending",
  "message": "Payment required. Awaiting ledger consensus.",
  "tx_id": "tx_abc123",
  "payment_address": "bc1q_utah_ephemeral_...",
  "amount_sats": 5000
}
```

After settlement, `GET /app/{app_name}` with the same `X-Client-ID` proxies to the container.

---

## POST /admin/revoke-node

Revoke a delegated node from `authorized_nodes[]`. Root vibe holder only. Utah-Flux revocation panel calls this endpoint.

**Request body:**

```json
{
  "node_hash": "abc123...64chars",
  "acoustic_hash": "root-vibe-hash-64chars"
}
```

**Response `200`:**

```json
{"status": "revoked", "node_hash": "abc123..."}
```

---

## Error Responses

| Code | When |
|------|------|
| `404` | Unknown path or node not revocable |
| `402` | App exists but client has not paid Tycoon invoice |
| `403` | Invalid revocation credentials or HMAC |

---

## Ports & Multicast

| Service | Port / Address |
|---------|----------------|
| HTTP ingress | `8999` |
| UtahNetes gossip | UDP `9001`, multicast `239.255.43.21` |
| Global Swarm | UDP `9055` |

---

## Data Files

| File | Purpose |
|------|---------|
| `{UTAH_DATA_DIR}/secure_registry.json` | Tenants, UtahX routes, storage index |
| `{UTAH_DATA_DIR}/flux_ui_manifest.json` | Utah-Flux UI state |
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Container handler |
| `{UTAH_DATA_DIR}/lambda/{fn}/handler.py` | Lambda handler |
| `{UTAH_DATA_DIR}/s3/{bucket}/{key}` | S3 Mesh objects |
| `{UTAH_DATA_DIR}/rds/ledger.json` | RDS key-value store |
| `security/biometric_ledger.json` | Root vibe hash (local fallback if `/etc` not writable) |
| `{UTAH_DATA_DIR}/quote_registry.json` | Global hardware quote registry |

Default `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (falls back to local dirs on permission errors).
