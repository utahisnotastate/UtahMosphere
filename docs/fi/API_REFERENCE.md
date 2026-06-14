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
  "version": "25.0"
}
```

**Esimerkki:**

```bash
curl http://127.0.0.1:8999/health
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
  "claimed": true
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

**Claimin jälkeen:** `acoustic_hash` täytyy vastata ankkuroitua juuri-vibe-hashia tai ydin palauttaa:

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

```json
{
  "status": "Unlocked",
  "message": "Container hello executing."
}
```

**Esimerkki:**

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## Virhevastaukset

| Koodi | Milloin |
|-------|---------|
| `404` | Tuntematon polku |
| `402` | Sovellus on olemassa, mutta asiakas ei ole maksanut Tycoon-laskua |

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
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Käyttöön otettu käsittelijäpohja |
| `security/biometric_ledger.json` | Juuri-vibe-hash (paikallinen varmuuskopio jos `/etc` ei kirjoitettavissa) |
| `tycoon/settlement_ledger.json` | Lasku- ja maksutila |

Oletus `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (varmuuskopio paikallisiin hakemistoihin oikeusvirheissä).
