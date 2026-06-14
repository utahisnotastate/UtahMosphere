# API viide

Baas-URL (vaikimisi): `http://127.0.0.1:8999`

Kõik vastused on JSON, kui pole märgitud teisiti.

---

## GET /health

Elusoleku päring koormuse tasakaalustajatele ja jälgimisele.

**Vastus `200`:**

```json
{
  "status": "healthy",
  "node": "my-hostname",
  "version": "26.0",
  "build": "omega-build-v26-final"
}
```

**Näide:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /nonce

Väljastab värske häälkäsu nonce. Nõutav pärast sõlme claim-i, kui `UTAH_NONCE_ENFORCE=1` (vaikimisi).

**Vastus `200`:**

```json
{
  "nonce": 1718323200,
  "window_sec": 30,
  "signature_hint": "HMAC-SHA256(acoustic_hash, f'{nonce}:{transcript}')"
}
```

**Näide:**

```bash
curl http://127.0.0.1:8999/nonce
```

---

## GET /status

Operatiivne hetktõmmis: UI olek, juurutatud rentnikud ja kas sõlm on claim-itud.

**Vastus `200`:**

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

Käivita hääle intent programmiliselt. Sama keha, mida Voice Bridge saadab.

**Päringu keha:**

| Väli | Tüüp | Kohustuslik | Kirjeldus |
|------|------|-------------|-----------|
| `transcript` | string | Jah | Kõnele käsk (tõstutundetu) |
| `acoustic_hash` | string | Jah | 64-tähemärgiline SHA-256 vibe-print räsi |
| `nonce` | integer | Pärast claim-i | Serveri väljastatud ajatempel `GET /nonce`-st |
| `command_signature` | string | Pärast claim-i | `HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")` |
| `request_signature` | string | Ei | Valikuline AuthGuard HMAC delegeeritud sõlmedele |

**Vastus `200`:**

```json
{
  "status": "manifested",
  "response": "Application successfully anchored into UtahContainerEngine loop on workspace port 8200."
}
```

### Toetatud transkriptsioonid

| Intent | Transkriptsiooni näide |
|--------|------------------------|
| Claim node | `"Claim node"` |
| Authorize node | `"authorize node <64-char-vibe-hash>"` |
| Deploy app | `"deploy application hello"` või `"manifest app hello"` |
| Patch app | `"patch app hello to add feature x"` |
| Status | `"status grid"` |

**Claim node (esimene käivitus):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Claim node", "acoustic_hash": "abc123..."}'
```

**Deploy app (avatud režiim — enne claim-i, iga räsi aktsepteeritud):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "deploy application hello", "acoustic_hash": "0000000000000000000000000000000000000000000000000000000000000000"}'
```

**Pärast claim-i:** `acoustic_hash` peab ühtima juure või `authorized_nodes[]`-ga ning `nonce` + `command_signature` peavad olema kehtivad, muidu tagastab tuum:

```json
{
  "status": "manifested",
  "response": "Access Denied. Biological signature does not match the Akashic Record."
}
```

---

## GET /app/{app_name}

Juurdepääs juurutatud rentniku rakendusele. Utah-Tycoon makse autoriseerimisega.

**Päised:**

| Päis | Kirjeldus |
|------|-----------|
| `X-Client-ID` | Valikuline kliendi identifikaator (vaikimisi kliendi IP) |

### Tasumata klient — Vastus `402 Payment Required`

```json
{
  "error": "Payment Required for UtahContainer Execution",
  "payment_address": "bc1q_utah_ephemeral_a1b2c3d4e5f6",
  "amount_sats": 5000,
  "message": "Transmit value to unlock silicon processing path."
}
```

Arved lahenduvad praeguses simulatsioonis automaatselt ~60 sekundi pärast.

### Tasutud klient — Vastus `200`

UtahX suunab päringu UtahContainerEngine taustale rentniku pordil. Vastuse keha on handleri JSON väljund.

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## PUT/POST /s3/{bucket}/{key}

Kirjuta objekt Utah S3 Mesh-i (kohalik NVMe salvestus).

**Päised (valikulised):**

| Päis | Kirjeldus |
|------|-----------|
| `X-Utah-Tenant-ID` | Rentniku identifikaator |
| `X-Utah-Signature` | HMAC-SHA256 `{tenant_id}:{path}` |

**Näide:**

```bash
curl -X PUT http://127.0.0.1:8999/s3/my-data/file.txt \
  -H "Content-Type: text/plain" \
  --data-binary "Hello Utah"
```

---

## GET /s3/{bucket}/{key}

Loe objekti. Tagastab toorbaite. Kasuta `GET /s3/{bucket}/prefix*` loendamiseks.

```bash
curl http://127.0.0.1:8999/s3/my-data/file.txt
```

---

## POST /rds/write

Kirjuta võti-väärtus kirje Utah RDS Ledgerisse.

**Päringu keha:**

```json
{"key": "user:123", "value": {"name": "Alice", "score": 9000}}
```

**Vastus `200`:**

```json
{"key": "user:123", "status": "written", "epoch": 1718280000.0}
```

---

## GET /rds/read/{key}

Loe kirjet võtme järgi.

```bash
curl http://127.0.0.1:8999/rds/read/user:123
```

---

## POST /lambda/{function_name}/invoke

Kutsu Utah Lambda handlerit (ilma konteineri pildi tõmbamiseta).

**Päringu keha:** JSON sündmus, mis edastatakse `handler(event, context)`-ile

```bash
curl -X POST http://127.0.0.1:8999/lambda/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "General 23"}'
```

**Vastus `200`:**

```json
{"result": {"message": "Hello General 23 from Utah Lambda!"}}
```

---

## POST /app/unlock

Esita makse avamise taotlus. Tycoon küsitleb mempool.space (või electrum-server) makse lõplikkuse jaoks. Arendusaadressid (`bc1q_utah_*`) kasutavad ajastatud arveldust režiimis `auto`.

**Päringu keha:**

```json
{
  "app_name": "hello",
  "client_id": "demo-client",
  "payment_tx": "optional-tx-hint",
  "amount_sats": 5000
}
```

**Vastus `202`:**

```json
{
  "status": "pending",
  "message": "Payment required. Awaiting ledger consensus.",
  "tx_id": "tx_abc123",
  "payment_address": "bc1q_utah_ephemeral_...",
  "amount_sats": 5000
}
```

Pärast arveldust suunab `GET /app/{app_name}` sama `X-Client-ID`-ga konteinerisse.

---

## POST /admin/revoke-node

Tühista delegeeritud sõlm `authorized_nodes[]`-st. Ainult juur-vibe omanik. Utah-Flux tühistamise paneel kutsub seda lõpp-punkti.

**Päringu keha:**

```json
{
  "node_hash": "abc123...64chars",
  "acoustic_hash": "root-vibe-hash-64chars"
}
```

**Vastus `200`:**

```json
{"status": "revoked", "node_hash": "abc123..."}
```

---

## Veavastused

| Kood | Millal |
|------|--------|
| `404` | Tundmatu tee või sõlm pole tühistatav |
| `402` | Rakendus eksisteerib, kuid klient pole Tycoon arvet tasunud |
| `403` | Kehtetu tühistamise mandaat või HMAC |

---

## Pordid ja multicast

| Teenus | Port / Aadress |
|--------|----------------|
| HTTP sissepääs | `8999` |
| UtahNetes gossip | UDP `9001`, multicast `239.255.43.21` |
| Global Swarm | UDP `9055` |

---

## Andmefailid

| Fail | Eesmärk |
|------|---------|
| `{UTAH_DATA_DIR}/secure_registry.json` | Rentnikud, UtahX marsruudid, salvestusindeks |
| `{UTAH_DATA_DIR}/flux_ui_manifest.json` | Utah-Flux UI olek |
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Konteineri handler |
| `{UTAH_DATA_DIR}/lambda/{fn}/handler.py` | Lambda handler |
| `{UTAH_DATA_DIR}/s3/{bucket}/{key}` | S3 Mesh objektid |
| `{UTAH_DATA_DIR}/rds/ledger.json` | RDS võti-väärtus salvestus |
| `security/biometric_ledger.json` | Juur-vibe räsi (kohalik varuvariant, kui `/etc` pole kirjutatav) |
| `tycoon/settlement_ledger.json` | Arve ja makse olek |

Vaikimisi `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (langeb kohalikele kataloogidele õiguse vigade korral).
