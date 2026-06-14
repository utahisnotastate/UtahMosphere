# Võimekuste maatriks

UtahMosphere OS **v25.1 Migration Ready** — rakendamise olek Omega-Buildi järgi.

---

## HTTP API lõpp-punktid

| Lõpp-punkt | Meetod | Olek | Märkused |
|------------|--------|------|----------|
| `/health` | GET | **Rakendatud** | Elusoleku päring + `build: golden-master-v25.1` |
| `/status` | GET | **Rakendatud** | UI olek, rentnikud, claim olek, S3 juur |
| `/command` | POST | **Rakendatud** | Hääle intenti käivitus |
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
| **Quantum Ledger** | Rakendatud | Biomeetriline claim + kinnitamine |
| **Utah-Tycoon** | **Rakendatud** | Mempool/electrum arveldus (`tycoon_settlement.py`), `POST /app/unlock`, HTTP 402 värav |
| **UtahNetes Gossip** | **Rakendatud** | AuthGuard-allkirjastatud 5s multicast `utah_mesh_engine.py` kaudu |
| **Global Swarm** | **Rakendatud** | Deterministiline DHT + allkirjastatud registeri sünk |
| **AuthGuard (`ledger_auth.py`)** | **Rakendatud** | `authorized_nodes[]` jõustamine hääle ja võrgu jaoks |
| **Genesis ISO (`mk_iso.sh`)** | **Rakendatud** | UEFI/hübriid flash-installeri ehitaja |
| **Utah-Flux UI** | Rakendatud | Tkinter oleku armatuurlaud |
| **Auto-Genesis (`genesis_deploy.py`)** | **Rakendatud** | Mitmeprotsessiline orkestreerija |
| **Bootstrap (`bootstrap.sh`)** | **Rakendatud** | Palja riistvara systemd paigaldus |

---

## Häälkäsud

| Käsu muster | Olek | Näide |
|-------------|------|-------|
| Claim node | Rakendatud | `"Claim node"` |
| Deploy application | Rakendatud | `"deploy application my-app"` |
| Patch application | **Rakendatud** | `"patch app my-app to add logging"` |
| Authorize node | **Rakendatud** | `"authorize node <64-char-vibe-hash>"` |
| Status / grid | Rakendatud | `"status grid"` |

---

## Juurutamise valikud

| Meetod | Olek | Platvorm |
|--------|------|----------|
| `python3 utahmosphere_master.py` | **Soovitatav** | Kõik |
| `python3 utahmosphere_os.py` | Rakendatud | Kõik |
| `python3 genesis_deploy.py` | Rakendatud | Linux / arendus |
| `sudo bash bootstrap.sh` | **Soovitatav tootmises** | Linux systemd |
| `sudo bash setup.sh` | Rakendatud | Aliase bootstrapile |
| `./mk_iso.sh` | **Rakendatud** | Linux — ehitab `utah_genesis_v25.iso` |
| `docker-compose up` | Valikuline | Ainult pärand mugavus |

---

## Teekaart (ülejäänud lüngad)

- Alpine/vmlinuz bundling Genesis ISO sees (käivitusmenüü dokumenteerib praegu käsitsi paigaldustee)
- Nonce/ajatempel häälkäskude korduskasutamise vastu
- `authorized_nodes` tühistamise kasutajaliides
