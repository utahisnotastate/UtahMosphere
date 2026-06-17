# API-viite

Perus-URL (oletus): `http://127.0.0.1:8999`

Kaikki vastaukset ovat JSON-muodossa, ellei toisin mainita.

---

## GET /health

Elvytystarkistus kuormantasaajille ja seurannalle.

**Vastaus `200`:**

```json
{
  "status": "healthy",
  "node": "my-hostname",
  "version": "35.0",
  "build": "omega-build-v35-omni-desk",
  "attestation": {
    "tpm_present": false,
    "provisioned": false,
    "sealed": false,
    "enforce": true,
    "tpm_lock": {"sealed": false, "binding_ok": true, "enforce": true},
    "ra_tls": {"enforce": true, "kernel_root_ca": "utahmosphere_omega_build_v35_root_ca", "dht_federation": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true}},
    "quote_registry": {"active": 1, "purged": 0, "total": 1},
    "dht_federation": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true},
    "quorum": {"quorum_reached": 1, "threshold": 0.51, "enforce": true},
    "witness": {"witnesses": 4, "threshold": 0.51, "enforce": true, "regions": ["us-east", "eu-west", "oceania-apac", "asia-east"]},
    "omni_mind": {"provider": "sovereign", "engine": "utahvidia"},
    "omni_glass": {"events": 0},
    "utah_claw": {"enforce": true, "pending": 0},
    "omni_desk": {"enforce": true, "genesis_apps": 5},
    "lazarus": {"auto_restore": true, "kexec_enforce": true, "checkpoint_exists": true},
    "pcr_drift": {"enforce": true, "rollback_enforce": true, "golden_set": true, "drift_detected": false}
  }
}
```

**Esimerkki:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /attestation/quote

Myöntää RA-TLS TPM quoten UtahNetes mesh-solmujen vahvistukseen.

**Vastaus `200`:**

```json
{
  "hardware_id": "sha256-hardware-fingerprint",
  "ra_tls_quote": {
    "body": "{\"build\":\"omega-build-v35-omni-desk\",\"node_id\":\"my-host\",\"hardware_id\":\"...\",\"pcr0_digest\":\"...\",\"vibe_hash\":\"...\"}",
    "signature": "hmac-sha256-hex",
    "ca_signature": "optional-rsa-hex"
  }
}
```

Katso [RA-TLS mesh-todentaminen](RA_TLS.md) ja [Laitteisto quote -rekisteri](QUOTE_REGISTRY.md).

---

## GET /registry/quotes

Vie globaali laitteisto quote -rekisteri (aktiiviset ja poistetut merkinnät).

**Vastaus `200`:**

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

Poista vaarantunut laitetunniste globaalista rekisteristä. Vain juuri-vibe-omistaja.

**Pyynnön runko:**

```json
{
  "hardware_id": "sha256-hardware-fingerprint",
  "acoustic_hash": "root-vibe-hash-64chars",
  "reason": "firmware tamper"
}
```

**Vastaus `200`:**

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

Myöntää tuoreen äänikomennon noncen. Vaaditaan solmun claimin jälkeen, kun `UTAH_NONCE_ENFORCE=1` (oletus).

**Vastaus `200`:**

```json
{
  "nonce": 1718323200,
  "window_sec": 30,
  "signature_hint": "HMAC-SHA256(acoustic_hash, f'{nonce}:{transcript}')"
}
```

**Esimerkki:**

```bash
curl http://127.0.0.1:8999/nonce
```

---

## GET /status

Operatiivinen tilannekuva: UI-tila, käyttöön otetut vuokralaiset ja onko solmu claimattu.

**Vastaus `200`:**

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

Suorita ääni-intentti ohjelmallisesti. Sama payload, jonka Voice Bridge lähettää.

**Pyynnön runko:**

| Kenttä | Tyyppi | Pakollinen | Kuvaus |
|--------|--------|------------|--------|
| `transcript` | string | Kyllä | Puhuttu komento (kirjainkoolla ei väliä) |
| `acoustic_hash` | string | Kyllä | 64 merkin SHA-256 vibe-print -hash |
| `nonce` | integer | Claimin jälkeen | Palvelimen myöntämä aikaleima `GET /nonce`:sta |
| `command_signature` | string | Claimin jälkeen | `HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")` — alias: `signature` |
| `request_signature` | string | Ei | Valinnainen AuthGuard HMAC delegoiduille solmuille |

**Vastaus `200`:**

```json
{
  "status": "manifested",
  "response": "Application successfully anchored into UtahContainerEngine loop on workspace port 8200."
}
```

### Tuetut transkriptit

| Intent | Transkriptiesimerkki |
|--------|---------------------|
| Claim node | `"Claim node"` |
| Authorize node | `"authorize node <64-char-vibe-hash>"` |
| Deploy app | `"deploy application hello"` tai `"manifest app hello"` |
| Patch app | `"patch app hello to add feature x"` |
| Status | `"status grid"` |

**Claim node (ensimmäinen ajo):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Claim node", "acoustic_hash": "abc123..."}'
```

**Deploy app (avoin tila — ennen claimia, mikä tahansa hash hyväksytään):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "deploy application hello", "acoustic_hash": "0000000000000000000000000000000000000000000000000000000000000000"}'
```

**Voice Bridge v27.0** kutsuu automaattisesti `GET /nonce` ja allekirjoittaa. Manuaalinen allekirjoitus:

```python
from voice_bridge_signed import get_signed_payload
payload = get_signed_payload("deploy application hello", acoustic_hash)
```

**Claimin jälkeen:** `acoustic_hash` täytyy vastata juurta tai `authorized_nodes[]`-listaa, ja `nonce` + `command_signature` täytyy olla kelvollisia, muuten ydin palauttaa:

```json
{
  "status": "manifested",
  "response": "Access Denied. Biological signature does not match the Akashic Record."
}
```

---

## GET /app/{app_name}

Pääsy käyttöön otettuun vuokralaiss sovellukseen. Utah-Tycoon-maksuvaltuutuksen takana.

**Otsikot:**

| Otsikko | Kuvaus |
|---------|--------|
| `X-Client-ID` | Valinnainen asiakastunniste (oletus: asiakkaan IP) |
| `X-Utah-Hardware-ID` | RA-TLS-laitteiston sormenjälki (sisääntulon todentaminen) |
| `X-Utah-RATLS-Quote` | JSON RA-TLS quote -payload |

Kun `UTAH_RA_TLS_GUARD_ENFORCE=1`, puuttuvat tai virheelliset todentamisotsikot palauttavat **403** ennen välitystä.

### Maksamaton asiakas — Vastaus `402 Payment Required`

```json
{
  "error": "Payment Required for UtahContainer Execution",
  "payment_address": "bc1q_utah_ephemeral_a1b2c3d4e5f6",
  "amount_sats": 5000,
  "message": "Transmit value to unlock silicon processing path."
}
```

Laskut selvitetään automaattisesti ~60 sekunnin kuluttua nykyisessä simulaatiossa.

### Maksanut asiakas — Vastaus `200`

UtahX välittää pyynnön UtahContainerEngine-taustaan vuokralaisen portissa. Vastauksen runko on käsittelijän JSON-tuloste.

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## PUT/POST /s3/{bucket}/{key}

Kirjoita objekti Utah S3 Meshiin (paikallinen NVMe-tallennus).

**Otsikot (valinnaiset):**

| Otsikko | Kuvaus |
|---------|--------|
| `X-Utah-Tenant-ID` | Vuokralaisen tunniste |
| `X-Utah-Signature` | HMAC-SHA256 `{tenant_id}:{path}` |

**Esimerkki:**

```bash
curl -X PUT http://127.0.0.1:8999/s3/my-data/file.txt \
  -H "Content-Type: text/plain" \
  --data-binary "Hello Utah"
```

---

## GET /s3/{bucket}/{key}

Lue objekti. Palauttaa raakatavut. Käytä `GET /s3/{bucket}/prefix*` listaukseen.

```bash
curl http://127.0.0.1:8999/s3/my-data/file.txt
```

---

## POST /rds/write

Kirjoita avain-arvo-tietue Utah RDS Ledgeriin.

**Pyynnön runko:**

```json
{"key": "user:123", "value": {"name": "Alice", "score": 9000}}
```

**Vastaus `200`:**

```json
{"key": "user:123", "status": "written", "epoch": 1718280000.0}
```

---

## GET /rds/read/{key}

Lue tietue avaimella.

```bash
curl http://127.0.0.1:8999/rds/read/user:123
```

---

## POST /lambda/{function_name}/invoke

Kutsu Utah Lambda -käsittelijää (ilman konttikuvan latausta).

**Pyynnön runko:** JSON-tapahtuma, joka välitetään `handler(event, context)`-funktiolle

```bash
curl -X POST http://127.0.0.1:8999/lambda/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "General 23"}'
```

**Vastaus `200`:**

```json
{"result": {"message": "Hello General 23 from Utah Lambda!"}}
```

---

## POST /app/unlock

Lähetä maksun avauspyyntö. Tycoon kysyy mempool.space (tai electrum-server) maksun lopullisuutta varten. Kehitysosoitteet (`bc1q_utah_*`) käyttävät ajoitettua selvitystä `auto`-tilassa.

**Pyynnön runko:**

```json
{
  "app_name": "hello",
  "client_id": "demo-client",
  "payment_tx": "optional-tx-hint",
  "amount_sats": 5000
}
```

**Vastaus `202`:**

```json
{
  "status": "pending",
  "message": "Payment required. Awaiting ledger consensus.",
  "tx_id": "tx_abc123",
  "payment_address": "bc1q_utah_ephemeral_...",
  "amount_sats": 5000
}
```

Selvityksen jälkeen `GET /app/{app_name}` samalla `X-Client-ID`:llä välittää konttiin.

---

## POST /admin/revoke-node

Peruuta delegoitu solmu `authorized_nodes[]`-listasta. Vain juuri-vibe-omistaja. Utah-Flux-peruutuspaneeli kutsuu tätä päätepistettä.

**Pyynnön runko:**

```json
{
  "node_hash": "abc123...64chars",
  "acoustic_hash": "root-vibe-hash-64chars"
}
```

**Vastaus `200`:**

```json
{"status": "revoked", "node_hash": "abc123..."}
```

---

## Virhevastaukset

| Koodi | Milloin |
|-------|---------|
| `404` | Tuntematon polku tai solmua ei voi peruuttaa |
| `402` | Sovellus on olemassa, mutta asiakas ei ole maksanut Tycoon-laskua |
| `403` | Virheelliset peruutustunnukset tai HMAC |

---

## Portit ja multicast

| Palvelu | Portti / Osoite |
|---------|-----------------|
| HTTP-sisääntulo | `8999` |
| UtahNetes-gossip | UDP `9001`, multicast `239.255.43.21` |
| Global Swarm | UDP `9055` |

---

## Datatiedostot

| Tiedosto | Tarkoitus |
|----------|-----------|
| `{UTAH_DATA_DIR}/secure_registry.json` | Vuokralaiset, UtahX-reitit, tallennusindeksi |
| `{UTAH_DATA_DIR}/flux_ui_manifest.json` | Utah-Flux UI -tila |
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Kontin käsittelijä |
| `{UTAH_DATA_DIR}/lambda/{fn}/handler.py` | Lambda-käsittelijä |
| `{UTAH_DATA_DIR}/s3/{bucket}/{key}` | S3 Mesh -objektit |
| `{UTAH_DATA_DIR}/rds/ledger.json` | RDS avain-arvo -tallennus |
| `security/biometric_ledger.json` | Juuri-vibe-hash (paikallinen varmuuskopio jos `/etc` ei kirjoitettavissa) |
| `{UTAH_DATA_DIR}/quote_registry.json` | Global hardware quote registry |
| `{UTAH_DATA_DIR}/dht_golden_registry.json` | DHT golden ledger |
| `{UTAH_DATA_DIR}/golden_pcr0.txt` | Golden PCR0 |
| `{UTAH_DATA_DIR}/dht_quorum_registry.json` | Quorum vote ledger |
| `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Lazarus Golden Master checkpoint |
| `{UTAH_DATA_DIR}/quorum_witness.json` | Multi-region witness registry |

Oletus `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (varmuuskopio paikallisiin hakemistoihin oikeusvirheissä).
