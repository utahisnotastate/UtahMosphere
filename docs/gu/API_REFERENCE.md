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
  "version": "25.0",
  "build": "golden-master-final"
}
```

**Ehemplo:**

```bash
curl http://127.0.0.1:8999/health
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
  "swarm_peers": 2,
  "tycoon": {"pending": 0, "settled_invoices": 1, "swept_funds": 5000}
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

**Después claim:** `acoustic_hash` debi match anchored root vibe hash pat core returns:

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

## POST /app/unlock

Submit payment unlock request. Tycoon ma register pending transaction ya ma return HTTP `202` hasta cryptographic settlement (~60s).

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

## Error Responses

| Code | Yanggen |
|------|---------|
| `404` | Unknown path |
| `402` | App exists pero client ti pago Tycoon invoice |

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
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Deployed handler boilerplate |
| `security/biometric_ledger.json` | Root vibe hash (lokal backup yanggen `/etc` not writable) |
| `tycoon/settlement_ledger.json` | Invoice yan payment state |

Default `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (falls back to local dirs on permission errors).
