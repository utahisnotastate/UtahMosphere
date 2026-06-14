# Võimekuste maatriks

UtahMosphere OS **v27.0 Production Immutable** — suveräänsed usaldusankrud on täielikult paigas.

---

## HTTP API lõpp-punktid

| Lõpp-punkt | Meetod | Olek | Märkused |
|------------|--------|------|----------|
| `/health` | GET | **Rakendatud** | Elusoleku päring + `build: omega-build-v27-production` + `attestation` |
| `/nonce` | GET | **Rakendatud** | Väljastab värske häälkäsu nonce (30s aken) |
| `/status` | GET | **Rakendatud** | UI olek, rentnikud, tõendamine, mempool varuühenduse statistika |
| `/command` | POST | **Rakendatud** | Hääle intent + automaatne nonce allkirjastamine (`voice_bridge_signed.py`) |
| `/admin/revoke-node` | POST | **Rakendatud** | Ainult juur — volitatud sõlme tühistamine |
| `/app/unlock` | POST | **Rakendatud** | Esita makse; mempool varuühenduse arveldus |
| `/app/{name}` | GET | **Rakendatud** | Tycoon 402 värav + UtahX proksi konteinerisse |
| `/app/{name}/{path}` | GET | **Rakendatud** | Alamtee proksi konteineri taustale |
| `/s3/{bucket}/{key}` | GET | **Rakendatud** | Objekti lugemine (kohalik NVMe) |
| `/s3/{bucket}/{key}` | PUT/POST | **Rakendatud** | Objekti kirjutamine; valikulised HMAC päised |
| `/s3/{bucket}/{prefix}*` | GET | **Rakendatud** | Objektide loend |
| `/lambda/{fn}/invoke` | POST | **Rakendatud** | Serveritu handleri kutsumine |
| `/lambda/{fn}` | GET | **Rakendatud** | GET kutsumine tühja sündmusega |
| `/rds/write` | POST | **Rakendatud** | Võti-väärtus kirjutamine |
| `/rds/read/{key}` | GET | **Rakendatud** | Võti-väärtus lugemine |

---

## Tuuma alamsüsteemid

| Komponent | Olek | Mis täna töötab |
|-----------|------|-----------------|
| **Golden Master (`utahmosphere_master.py`)** | **Rakendatud** | Ühtne sisenemispunkt |
| **Tuum (`utahmosphere_os.py`)** | **Rakendatud** | Täielik HTTP multiplekser, register, võrk |
| **Riistvara tõendamine (`attestation_guard.py`)** | **Rakendatud** | TPM 2.0 PCR0 värav bootstrapis + tervises |
| **Mempool varuühendus (`tycoon_failover.py`)** | **Rakendatud** | USA/EU/Aasia mempool vaikne varuühendus |
| **Voice Bridge Signed (`voice_bridge_signed.py`)** | **Rakendatud** | Automaatne `GET /nonce` + HMAC allkirjastamine |
| **UtahX Proxy (`utahx_proxy.py`)** | **Rakendatud** | Reaalajas HTTP proksi konteineri portidele |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Rakendatud** | Rentniku HTTP serverid portidel 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Rakendatud** | AST-kinnitatud handleri mutatsioon + OTA |
| **S3 / Lambda / RDS** | **Rakendatud** | Täielik pilve pariteet |
| **Quantum Ledger** | **Rakendatud** | Biomeetriline claim + kinnitamine |
| **Utah-Tycoon** | **Rakendatud** | Varuühenduse mempool + electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Rakendatud** | `authorized_nodes[]` jõustamine |
| **Nonce-Guard (`nonce_guard.py`)** | **Rakendatud** | 30s korduskasutuse vastu häälkäskudele |
| **UtahNetes + Swarm DHT** | **Rakendatud** | Allkirjastatud gossip + deterministiline marsruutimine |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Rakendatud** | Alpine vmlinuz + TPM-teadlik bootstrap |
| **Utah-Flux tühistamise UI** | **Rakendatud** | Admin-paneel `flux_gui.py` sees |
| **Auto-Genesis / Bootstrap** | **Rakendatud** | systemd + tõendamise värav |

---

## Häälkäsud

| Käsu muster | Olek | Näide |
|-------------|------|-------|
| Claim node | Rakendatud | `"Claim node"` |
| Authorize node | Rakendatud | `"authorize node <64-char-vibe-hash>"` |
| Deploy application | Rakendatud | `"deploy application my-app"` |
| Patch application | Rakendatud | `"patch app my-app to add logging"` |
| Status / grid | Rakendatud | `"status grid"` |

**Voice Bridge v27.0** hangib automaatselt `GET /nonce` ja allkirjastab iga käsu. Käsitsi kliendid kasutavad `voice_bridge_signed.get_signed_payload()`.

---

## Juurutamise valikud

| Meetod | Olek | Platvorm |
|--------|------|----------|
| `python3 utahmosphere_master.py` | **Soovitatav** | Kõik |
| `sudo bash bootstrap.sh` | **Soovitatav tootmises** | Linux + TPM (valikuline vahelejätmine) |
| `python3 genesis_iso_builder.py` | **Rakendatud** | Ehitab `utah_genesis_v27.iso` |
| `./mk_iso.sh` | **Rakendatud** | Genesis ISO ehitaja ümbris |
| `python3 voice_bridge.py` | **Rakendatud** | Automaatse nonce allkirjastamisega häälklient |

---

## Teekaart

Kõik v26.0 ja varasemad teekaardi punktid on v27.0-s **rakendatud**.

Tuleviku täiustused:

- TPM quote tõendamise kaugkinnitamine (RA-TLS)
- Neljas mempool piirkond (Okeaania)
- Riistvaraga seotud vibe-print sidumine TPM PCR-iga

Vaata [API viidet](API_REFERENCE.md) ja [Arendaja retseptiraamatut](DEVELOPER_COOKBOOK.md).
