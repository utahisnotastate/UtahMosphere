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
  "version": "25.0",
  "build": "golden-master-final"
}
```

**Näide:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /status

Operatiivne hetktõmmis: UI olek, juurutatud rentnikud, claim olek, `swarm_peers` ja Tycoon statistika.

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
  "swarm_peers": 2,
  "tycoon": {"pending": 0, "settled_invoices": 1, "swept_funds": 5000}
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

**Pärast claim-i:** `acoustic_hash` peab ühtima ankurdatud juur-vibe räsiga, muidu tagastab tuum:

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

```json
{
  "status": "Unlocked",
  "message": "Container hello executing."
}
```

**Näide:**

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## POST /app/unlock

Esita makse avamise taotlus. Tycoon registreerib ootel tehingu ja tagastab HTTP `202` kuni krüptograafilise arvelduseni (~60 s).

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

## Veavastused

| Kood | Millal |
|------|--------|
| `404` | Tundmatu tee |
| `402` | Rakendus eksisteerib, kuid klient pole Tycoon arvet tasunud |

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
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Juurutatud handler stub |
| `security/biometric_ledger.json` | Juur-vibe räsi (kohalik varuvariant, kui `/etc` pole kirjutatav) |
| `tycoon/settlement_ledger.json` | Arve ja makse olek |

Vaikimisi `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (langeb kohalikele kataloogidele õiguse vigade korral).
