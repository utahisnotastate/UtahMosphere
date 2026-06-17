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
  "version": "34.0",
  "build": "omega-build-v34-utah-claw",
  "attestation": {
    "tpm_present": false,
    "provisioned": false,
    "sealed": false,
    "enforce": true,
    "tpm_lock": {"sealed": false, "binding_ok": true, "enforce": true},
    "ra_tls": {"enforce": true, "kernel_root_ca": "utahmosphere_omega_build_v34_root_ca", "dht_federation": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true}},
    "quote_registry": {"active": 1, "purged": 0, "total": 1},
    "dht_federation": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true},
    "quorum": {"quorum_reached": 1, "threshold": 0.51, "enforce": true},
    "witness": {"witnesses": 4, "threshold": 0.51, "enforce": true, "regions": ["us-east", "eu-west", "oceania-apac", "asia-east"]},
    "omni_mind": {"provider": "sovereign", "engine": "utahvidia"},
    "omni_glass": {"events": 0},
    "utah_claw": {"enforce": true, "pending": 0},
    "lazarus": {"auto_restore": true, "kexec_enforce": true, "checkpoint_exists": true},
    "pcr_drift": {"enforce": true, "rollback_enforce": true, "golden_set": true, "drift_detected": false}
  }
}
```

**Näide:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /attestation/quote

Väljasta RA-TLS TPM quote UtahNetes mesh-sõlmede kontrolliks.

**Vastus `200`:**

```json
{
  "hardware_id": "sha256-hardware-fingerprint",
  "ra_tls_quote": {
    "body": "{\"build\":\"omega-build-v34-utah-claw\",\"node_id\":\"my-host\",\"hardware_id\":\"...\",\"pcr0_digest\":\"...\",\"vibe_hash\":\"...\"}",
    "signature": "hmac-sha256-hex",
    "ca_signature": "optional-rsa-hex"
  }
}
```

---

## GET /registry/quotes

Export global hardware quote registry.

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

Purge compromised hardware ID. Root vibe holder only.

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

---

---



---



---

## POST /claw/void

Dispatch UtahClaw epistemic void research.

---

## GET /claw/status

UtahClaw ambient runner status.

---

## GET /chrono/status

Chrono-State rewind engine status.

---

## GET /siphon/ghost-tune

Kinematic Siphon Ghost Tune binary.


## POST /omni/compile

Agentic intent compilation.

```bash
curl -X POST http://127.0.0.1:8999/omni/compile -H "Content-Type: application/json" -d '{"intent": "health check API"}'
```

---

## GET /omni/status

Omni-Mind status.

---

## GET /omni/glass

Omni-Glass agentic event log.


## GET /witness/status

Multi-region quorum witness status.

```bash
curl http://127.0.0.1:8999/witness/status
```

---

## GET /lazarus/status

Lazarus auto-restore checkpoint status.

---

## POST /lazarus/restore

Trigger Golden Master restoration.

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```


## GET /quorum/consensus

Export majority-quorum vote ledger.

**Response `200`:**

```json
{
  "consensus": {
    "my-host": {
      "golden_quote": "sha256-fingerprint",
      "votes": {"voter-node": "sha256-fingerprint"},
      "quorum_ratio": 1.0,
      "vote_count": 1,
      "status": "quorum_reached"
    }
  },
  "stats": {"quorum_reached": 1, "pending": 0, "quarantined": 0, "total": 1, "threshold": 0.51, "enforce": true}
}
```

```bash
curl http://127.0.0.1:8999/quorum/consensus
```


## GET /dht/consensus

Export DHT golden measurement ledger.

**Response `200`:**

```json
{
  "golden": {
    "my-host": {
      "golden_quote": "sha256-fingerprint",
      "pcr_digest": "...",
      "hardware_id": "...",
      "status": "consensus",
      "recorded_at": 1718323200.0
    }
  },
  "stats": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true}
}
```

```bash
curl http://127.0.0.1:8999/dht/consensus
```

---

## POST /dht/challenge

Issue attestation challenge to swarm peer.

**Request body:**

```json
{"peer_hash": "64-char-node-hash"}
```

**Response `202`:**

```json
{"status": "challenge_sent", "peer_hash": "abc123..."}
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

Käivita hääle intent programmiliselt. Sama keha, mida Voice Bridge saadab.

**Päringu keha:**

| Väli | Tüüp | Kohustuslik | Kirjeldus |
|------|------|-------------|-----------|
| `transcript` | string | Jah | Kõnele käsk (tõstutundetu) |
| `acoustic_hash` | string | Jah | 64-tähemärgiline SHA-256 vibe-print räsi |
| `nonce` | integer | Pärast claim-i | Serveri väljastatud ajatempel `GET /nonce`-st |
| `command_signature` | string | Pärast claim-i | `HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")` — alias: `signature` |
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

**Voice Bridge v27.0** kutsub automaatselt `GET /nonce` ja allkirjastab. Käsitsi allkirjastamine:

```python
from voice_bridge_signed import get_signed_payload
payload = get_signed_payload("deploy application hello", acoustic_hash)
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
| `X-Utah-Hardware-ID` | RA-TLS hardware fingerprint (ingress attestation) |
| `X-Utah-RATLS-Quote` | JSON RA-TLS quote payload |

When `UTAH_RA_TLS_GUARD_ENFORCE=1`, missing or invalid attestation headers return **403** before proxy.

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
| `tycoon/settlement_ledger.json` |
| `{UTAH_DATA_DIR}/quote_registry.json` | Global hardware quote registry |
| `{UTAH_DATA_DIR}/dht_golden_registry.json` | DHT golden ledger |
| `{UTAH_DATA_DIR}/golden_pcr0.txt` | Golden PCR0 |
| `{UTAH_DATA_DIR}/dht_quorum_registry.json` | Quorum vote ledger |
| `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Lazarus Golden Master checkpoint |
| `{UTAH_DATA_DIR}/quorum_witness.json` | Multi-region witness registry |

Vaikimisi `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (langeb kohalikele kataloogidele õiguse vigade korral).
