# API-referens

Bas-URL (standard): `http://127.0.0.1:8999`

Alla svar är JSON om inget annat anges.

---

## GET /health

Liveness-probe för lastbalanserare och övervakning.

**Svar `200`:**

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

**Exempel:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /nonce

Utfärdar ett färskt nonce för röstkommando. Krävs efter nod-claim när `UTAH_NONCE_ENFORCE=1` (standard).

**Svar `200`:**

```json
{
  "nonce": 1718323200,
  "window_sec": 30,
  "signature_hint": "HMAC-SHA256(acoustic_hash, f'{nonce}:{transcript}')"
}
```

**Exempel:**

```bash
curl http://127.0.0.1:8999/nonce
```

---

## GET /status

Operativ ögonblicksbild: UI-tillstånd, driftsatta tenants och om noden har claimats.

**Svar `200`:**

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

Kör en röstintent programmatiskt. Samma payload som Voice Bridge skickar.

**Request body:**

| Fält | Typ | Obligatoriskt | Beskrivning |
|------|-----|---------------|-------------|
| `transcript` | string | Ja | Talat kommando (skiftlägesokänsligt) |
| `acoustic_hash` | string | Ja | 64-teckens SHA-256 vibe-print-hash |
| `nonce` | integer | Efter claim | Serverutfärdad tidsstämpel från `GET /nonce` |
| `command_signature` | string | Efter claim | `HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")` — alias: `signature` |
| `request_signature` | string | Nej | Valfri AuthGuard HMAC för delegerade noder |

**Svar `200`:**

```json
{
  "status": "manifested",
  "response": "Application successfully anchored into UtahContainerEngine loop on workspace port 8200."
}
```

### Stödda transkript

| Intent | Transkriptexempel |
|--------|-------------------|
| Claim node | `"Claim node"` |
| Authorize node | `"authorize node <64-char-vibe-hash>"` |
| Deploy app | `"deploy application hello"` eller `"manifest app hello"` |
| Patch app | `"patch app hello to add feature x"` |
| Status | `"status grid"` |

**Claim node (första körningen):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Claim node", "acoustic_hash": "abc123..."}'
```

**Deploy app (öppet läge — före claim, vilken hash som helst accepteras):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "deploy application hello", "acoustic_hash": "0000000000000000000000000000000000000000000000000000000000000000"}'
```

**Voice Bridge v27.0** anropar automatiskt `GET /nonce` och signerar. Manuell signering:

```python
from voice_bridge_signed import get_signed_payload
payload = get_signed_payload("deploy application hello", acoustic_hash)
```

**Efter claim:** `acoustic_hash` måste matcha root eller `authorized_nodes[]`, och `nonce` + `command_signature` måste vara giltiga, annars returnerar kärnan:

```json
{
  "status": "manifested",
  "response": "Access Denied. Biological signature does not match the Akashic Record."
}
```

---

## GET /app/{app_name}

Åtkomst till en driftsatt tenant-app. Gated av Utah-Tycoon-betalningsauktorisering.

**Headers:**

| Header | Beskrivning |
|--------|-------------|
| `X-Client-ID` | Valfri klientidentifierare (standard: klient-IP) |

### Obetald klient — Svar `402 Payment Required`

```json
{
  "error": "Payment Required for UtahContainer Execution",
  "payment_address": "bc1q_utah_ephemeral_a1b2c3d4e5f6",
  "amount_sats": 5000,
  "message": "Transmit value to unlock silicon processing path."
}
```

Fakturor avvecklas automatiskt efter ~60 sekunder i nuvarande simulering.

### Betald klient — Svar `200`

UtahX proxar begäran till UtahContainerEngine-backend på tenant-porten. Svarskroppen är handler-JSON-utdata.

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## PUT/POST /s3/{bucket}/{key}

Skriv objekt till Utah S3 Mesh (lokal NVMe-lagring).

**Headers (valfria):**

| Header | Beskrivning |
|--------|-------------|
| `X-Utah-Tenant-ID` | Tenant-identifierare |
| `X-Utah-Signature` | HMAC-SHA256 av `{tenant_id}:{path}` |

**Exempel:**

```bash
curl -X PUT http://127.0.0.1:8999/s3/my-data/file.txt \
  -H "Content-Type: text/plain" \
  --data-binary "Hello Utah"
```

---

## GET /s3/{bucket}/{key}

Läs objekt. Returnerar råa bytes. Använd `GET /s3/{bucket}/prefix*` för listning.

```bash
curl http://127.0.0.1:8999/s3/my-data/file.txt
```

---

## POST /rds/write

Skriv nyckel-värde-post till Utah RDS Ledger.

**Request body:**

```json
{"key": "user:123", "value": {"name": "Alice", "score": 9000}}
```

**Svar `200`:**

```json
{"key": "user:123", "status": "written", "epoch": 1718280000.0}
```

---

## GET /rds/read/{key}

Läs post efter nyckel.

```bash
curl http://127.0.0.1:8999/rds/read/user:123
```

---

## POST /lambda/{function_name}/invoke

Anropa Utah Lambda-handler (ingen container image pull).

**Request body:** JSON-event som skickas till `handler(event, context)`

```bash
curl -X POST http://127.0.0.1:8999/lambda/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "General 23"}'
```

**Svar `200`:**

```json
{"result": {"message": "Hello General 23 from Utah Lambda!"}}
```

---

## POST /app/unlock

Skicka en begäran om betalningsupplåsning. Tycoon frågar mempool.space (eller electrum-server) om betalningens slutgiltighet. Dev-adresser (`bc1q_utah_*`) använder tidsstyrd avveckling i läget `auto`.

**Request body:**

```json
{
  "app_name": "hello",
  "client_id": "demo-client",
  "payment_tx": "optional-tx-hint",
  "amount_sats": 5000
}
```

**Svar `202`:**

```json
{
  "status": "pending",
  "message": "Payment required. Awaiting ledger consensus.",
  "tx_id": "tx_abc123",
  "payment_address": "bc1q_utah_ephemeral_...",
  "amount_sats": 5000
}
```

Efter avveckling proxar `GET /app/{app_name}` med samma `X-Client-ID` till containern.

---

## POST /admin/revoke-node

Återkalla en delegerad nod från `authorized_nodes[]`. Endast root vibe-innehavare. Utah-Flux återkallandepanel anropar denna endpoint.

**Request body:**

```json
{
  "node_hash": "abc123...64chars",
  "acoustic_hash": "root-vibe-hash-64chars"
}
```

**Svar `200`:**

```json
{"status": "revoked", "node_hash": "abc123..."}
```

---

## Felsvar

| Kod | När |
|-----|-----|
| `404` | Okänd sökväg eller nod kan inte återkallas |
| `402` | App finns men klienten har inte betalat Tycoon-faktura |
| `403` | Ogiltiga återkallandeuppgifter eller HMAC |

---

## Portar och multicast

| Tjänst | Port / Adress |
|--------|---------------|
| HTTP-ingress | `8999` |
| UtahNetes-gossip | UDP `9001`, multicast `239.255.43.21` |
| Global Swarm | UDP `9055` |

---

## Datafiler

| Fil | Syfte |
|-----|-------|
| `{UTAH_DATA_DIR}/secure_registry.json` | Tenants, UtahX-routes, lagringsindex |
| `{UTAH_DATA_DIR}/flux_ui_manifest.json` | Utah-Flux UI-tillstånd |
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Container-handler |
| `{UTAH_DATA_DIR}/lambda/{fn}/handler.py` | Lambda-handler |
| `{UTAH_DATA_DIR}/s3/{bucket}/{key}` | S3 Mesh-objekt |
| `{UTAH_DATA_DIR}/rds/ledger.json` | RDS nyckel-värde-lagring |
| `security/biometric_ledger.json` | Rot-vibe-hash (lokal fallback om `/etc` inte skrivbar) |
| `tycoon/settlement_ledger.json` | Faktura- och betalningstillstånd |

Standard `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (fallback till lokala kataloger vid behörighetsfel).
