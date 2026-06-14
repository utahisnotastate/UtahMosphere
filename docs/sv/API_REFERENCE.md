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
  "version": "25.1",
  "build": "golden-master-v25.1"
}
```

**Exempel:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /status

Operativ ögonblicksbild: UI-tillstånd, driftsatta tenants, claim-status, `authorized_nodes`, `swarm_peers` och utökade Tycoon-fält.

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
    "mempool_api": "https://mempool.space/api"
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

**Efter claim:** `acoustic_hash` måste matcha den förankrade rot-vibe-hashen **eller** vara en post i `authorized_nodes[]`, annars returnerar kärnan:

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

```json
{
  "status": "Unlocked",
  "message": "Container hello executing."
}
```

**Exempel:**

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
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

## Felsvar

| Kod | När |
|-----|-----|
| `404` | Okänd sökväg |
| `402` | App finns men klienten har inte betalat Tycoon-faktura |

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
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Driftsatt handler-stub |
| `security/biometric_ledger.json` | Rot-vibe-hash (lokal fallback om `/etc` inte skrivbar) |
| `tycoon/settlement_ledger.json` | Faktura- och betalningstillstånd |

Standard `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (fallback till lokala kataloger vid behörighetsfel).
