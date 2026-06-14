# Referensia API

Base URL (default): `http://127.0.0.1:8999`

Todu i response siha JSON unless noted otherwise.

---

## GET /health

Chek si mumuña para load balancers yan monitoring.

**Response `200`:**

```json
{
  "status": "healthy",
  "node": "my-hostname",
  "version": "27.0",
  "build": "omega-build-v27-production",
  "attestation": {
    "tpm_present": true,
    "provisioned": true,
    "sealed": false,
    "enforce": true
  }
}
```

**Ehemplo:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /nonce

Ma issue fresh voice command nonce. Necessario después claim yanggen `UTAH_NONCE_ENFORCE=1` (default).

**Response `200`:**

```json
{
  "nonce": 1718323200,
  "window_sec": 30,
  "signature_hint": "HMAC-SHA256(acoustic_hash, f'{nonce}:{transcript}')"
}
```

**Ehemplo:**

```bash
curl http://127.0.0.1:8999/nonce
```

---

## GET /status

Retratu operasion: UI state, deployed tenants, yan claimed status.

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
      "https://mempool.space/api",
      "https://mempool.space/signet/api",
      "https://blockstream.info/api"
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

Ma execute voice intent programmaticamente. I mismo payload Voice Bridge ma send.

**Request body:**

| Field | Type | Necessario | Deskripsion |
|-------|------|------------|-------------|
| `transcript` | string | Si | Komando gi bos (ti importa uppercase/lowercase) |
| `acoustic_hash` | string | Si | 64-char SHA-256 vibe-print hash |
| `nonce` | integer | Después claim | Server-issued timestamp ginen `GET /nonce` |
| `command_signature` | string | Después claim | `HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")` — alias: `signature` |
| `request_signature` | string | Tåya' | Optional AuthGuard HMAC para delegated nodes |

**Response `200`:**

```json
{
  "status": "manifested",
  "response": "Application successfully anchored into UtahContainerEngine loop on workspace port 8200."
}
```

### Transcript siha ma support

| Intent | Ehemplo Transcript |
|--------|-------------------|
| Claim node | `"Claim node"` |
| Authorize node | `"authorize node <64-char-vibe-hash>"` |
| Deploy app | `"deploy application hello"` pat `"manifest app hello"` |
| Patch app | `"patch app hello to add feature x"` |
| Status | `"status grid"` |

**Claim node (primeru run):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Claim node", "acoustic_hash": "abc123..."}'
```

**Deploy app (open mode — antes claim, cualquier hash ma accept):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "deploy application hello", "acoustic_hash": "0000000000000000000000000000000000000000000000000000000000000000"}'
```

**Voice Bridge v27.0** ma call `GET /nonce` yan ma sign automaticamente. Manual signing:

```python
from voice_bridge_signed import get_signed_payload
payload = get_signed_payload("deploy application hello", acoustic_hash)
```

**Después claim:** `acoustic_hash` debi match root pat `authorized_nodes[]`, yan `nonce` + `command_signature` debi valid, pat core returns:

```json
{
  "status": "manifested",
  "response": "Access Denied. Biological signature does not match the Akashic Record."
}
```

---

## GET /app/{app_name}

Access gi deployed tenant app. Behind Utah-Tycoon payment authorization.

**Headers:**

| Header | Deskripsion |
|--------|-------------|
| `X-Client-ID` | Optional client identifier (default: client IP) |

### Client ti pago — Response `402 Payment Required`

```json
{
  "error": "Payment Required for UtahContainer Execution",
  "payment_address": "bc1q_utah_ephemeral_a1b2c3d4e5f6",
  "amount_sats": 5000,
  "message": "Transmit value to unlock silicon processing path."
}
```

Invoices ma settle automaticamente ~60 seconds gi current simulation.

### Client ma pago — Response `200`

UtahX ma proxy i request gi UtahContainerEngine backend gi tenant port. I response body i handler JSON output.

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## PUT/POST /s3/{bucket}/{key}

Write object gi Utah S3 Mesh (local NVMe storage).

**Headers (optional):**

| Header | Deskripsion |
|--------|-------------|
| `X-Utah-Tenant-ID` | Tenant identifier |
| `X-Utah-Signature` | HMAC-SHA256 gi `{tenant_id}:{path}` |

**Ehemplo:**

```bash
curl -X PUT http://127.0.0.1:8999/s3/my-data/file.txt \
  -H "Content-Type: text/plain" \
  --data-binary "Hello Utah"
```

---

## GET /s3/{bucket}/{key}

Read object. Ma return raw bytes. Usa `GET /s3/{bucket}/prefix*` para list.

```bash
curl http://127.0.0.1:8999/s3/my-data/file.txt
```

---

## POST /rds/write

Write key-value record gi Utah RDS Ledger.

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

Invoke Utah Lambda handler (sin container image pull).

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

Submit payment unlock request. Tycoon ma poll mempool.space (pat electrum-server) para payment finality. Dev addresses (`bc1q_utah_*`) ma usa timed settlement gi `auto` mode.

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

Después settlement, `GET /app/{app_name}` yan i mismo `X-Client-ID` ma proxy gi container.

---

## POST /admin/revoke-node

Revoke delegated node ginen `authorized_nodes[]`. Root vibe holder ha'. Utah-Flux revocation panel ma call este endpoint.

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

| Code | Yanggen |
|------|---------|
| `404` | Unknown path pat node ti revocable |
| `402` | App exists pero client ti pago Tycoon invoice |
| `403` | Invalid revocation credentials pat HMAC |

---

## Ports yan Multicast

| Service | Port / Address |
|---------|----------------|
| HTTP ingress | `8999` |
| UtahNetes gossip | UDP `9001`, multicast `239.255.43.21` |
| Global Swarm | UDP `9055` |

---

## Data Files

| File | Para håfa |
|------|-----------|
| `{UTAH_DATA_DIR}/secure_registry.json` | Tenants, UtahX routes, storage index |
| `{UTAH_DATA_DIR}/flux_ui_manifest.json` | Utah-Flux UI state |
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Container handler |
| `{UTAH_DATA_DIR}/lambda/{fn}/handler.py` | Lambda handler |
| `{UTAH_DATA_DIR}/s3/{bucket}/{key}` | S3 Mesh objects |
| `{UTAH_DATA_DIR}/rds/ledger.json` | RDS key-value store |
| `security/biometric_ledger.json` | Root vibe hash (lokal backup yanggen `/etc` not writable) |
| `tycoon/settlement_ledger.json` | Invoice yan payment state |

Default `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (falls back to local dirs on permission errors).
