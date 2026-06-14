# Võimekuste maatriks

UtahMosphere OS **v26.0 Omega-Build FINAL** — täielik teekaardi rakendamine.

---

## HTTP API lõpp-punktid

| Lõpp-punkt | Meetod | Olek | Märkused |
|------------|--------|------|----------|
| `/health` | GET | **Rakendatud** | Elusoleku päring + `build: omega-build-v26-final` |
| `/nonce` | GET | **Rakendatud** | Väljastab värske häälkäsu nonce (30s aken) |
| `/status` | GET | **Rakendatud** | UI olek, rentnikud, claim olek, S3 juur |
| `/command` | POST | **Rakendatud** | Hääle intenti käivitus + nonce korduskasutuse vastu pärast claim-i |
| `/admin/revoke-node` | POST | **Rakendatud** | Ainult juur — volitatud sõlme tühistamine |
| `/app/unlock` | POST | **Rakendatud** | Esita makse; tagastab 202 kuni arveldus |
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
| **UtahX Proxy (`utahx_proxy.py`)** | **Rakendatud** | Reaalajas HTTP proksi konteineri portidele |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Rakendatud** | Rentniku HTTP serverid portidel 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Rakendatud** | AST-kinnitatud handleri mutatsioon + OTA kanal |
| **S3 Mesh (`utah_s3_mesh.py`)** | **Rakendatud** | Kohalik objektisalvestus + HMAC |
| **Lambda Engine (`utah_lambda_engine.py`)** | **Rakendatud** | Handleri kutsumine ilma piltideta |
| **RDS Ledger (`utah_rds_ledger.py`)** | **Rakendatud** | JSON võti-väärtus register |
| **Quantum Ledger** | **Rakendatud** | Biomeetriline claim + kinnitamine |
| **Utah-Tycoon** | **Rakendatud** | Mempool/electrum arveldus (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Rakendatud** | `authorized_nodes[]` jõustamine hääle ja võrgu jaoks |
| **Nonce-Guard (`nonce_guard.py`)** | **Rakendatud** | 30s korduskasutuse vastu häälkäskudele |
| **UtahNetes Gossip** | **Rakendatud** | AuthGuard-allkirjastatud 5s multicast `utah_mesh_engine.py` kaudu |
| **Global Swarm** | **Rakendatud** | Deterministiline DHT + allkirjastatud registeri sünk |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Rakendatud** | Alpine vmlinuz/initramfs hübriid ISO |
| **Utah-Flux tühistamise UI (`ui_revocation.py`)** | **Rakendatud** | Admin-paneel `flux_gui.py` sees |
| **Utah-Flux UI** | **Rakendatud** | Tkinter olek + tühistamise armatuurlaud |
| **Auto-Genesis (`genesis_deploy.py`)** | **Rakendatud** | Mitmeprotsessiline orkestreerija |
| **Bootstrap (`bootstrap.sh`)** | **Rakendatud** | Palja riistvara systemd paigaldus |

---

## Häälkäsud

| Käsu muster | Olek | Näide |
|-------------|------|-------|
| Claim node | Rakendatud | `"Claim node"` |
| Authorize node | **Rakendatud** | `"authorize node <64-char-vibe-hash>"` |
| Deploy application | Rakendatud | `"deploy application my-app"` |
| Patch application | **Rakendatud** | `"patch app my-app to add logging"` |
| Status / grid | Rakendatud | `"status grid"` |

**Pärast claim-i:** lisa iga `/command` päringule `nonce` + `command_signature` pärit `GET /nonce`-st.

---

## Juurutamise valikud

| Meetod | Olek | Platvorm |
|--------|------|----------|
| `python3 utahmosphere_master.py` | **Soovitatav** | Kõik |
| `python3 utahmosphere_os.py` | Rakendatud | Kõik |
| `python3 genesis_deploy.py` | Rakendatud | Linux / arendus |
| `sudo bash bootstrap.sh` | **Soovitatav tootmises** | Linux systemd |
| `sudo bash setup.sh` | Rakendatud | Aliase bootstrapile |
| `python3 genesis_iso_builder.py` | **Rakendatud** | Linux — ehitab `utah_genesis_v26.iso` |
| `./mk_iso.sh` | **Rakendatud** | Genesis ISO ehitaja ümbris |
| `docker-compose up` | Valikuline | Ainult pärand mugavus |

---

## Teekaart

Kõik v25.x teekaardi punktid on v26.0-s **rakendatud**. Tuleviku töö:

- Riistvara tõendamine Genesis ISO automaatseks paigaldamiseks
- Mitme piirkonna mempool varuühendus
- Voice Bridge automaatne nonce allkirjastamine

Vaata [API viidet](API_REFERENCE.md) ja [Arendaja retseptiraamatut](DEVELOPER_COOKBOOK.md) praeguste rakenduse detailide jaoks.
