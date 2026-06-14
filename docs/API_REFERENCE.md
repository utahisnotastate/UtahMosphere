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
  "version": "25.0"
}
```

**Example:**

```bash
curl http://127.0.0.1:8999/health
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
  "claimed": true
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

**After claim:** `acoustic_hash` must match the anchored root vibe hash or the kernel returns:

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

```json
{
  "status": "Unlocked",
  "message": "Container hello executing."
}
```

**Example:**

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## Error Responses

| Code | When |
|------|------|
| `404` | Unknown path |
| `402` | App exists but client has not paid Tycoon invoice |

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
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Deployed handler stub |
| `security/biometric_ledger.json` | Root vibe hash (local fallback if `/etc` not writable) |
| `tycoon/settlement_ledger.json` | Invoice and payment state |

Default `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (falls back to local dirs on permission errors).
