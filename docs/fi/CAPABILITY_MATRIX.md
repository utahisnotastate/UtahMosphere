# Ominaisuusmatriisi

UtahMosphere OS **v25.1 Migration Ready** — toteutuksen tila Omega-Buildin mukaan.

---

## HTTP API -päätepisteet

| Päätepiste | Metodi | Tila | Huomiot |
|------------|--------|------|---------|
| `/health` | GET | **Toteutettu** | Elvytystarkistus + `build: golden-master-v25.1` |
| `/status` | GET | **Toteutettu** | UI-tila, vuokralaiset, claim-tila, S3-juuri |
| `/command` | POST | **Toteutettu** | Ääni-intentin suoritus |
| `/app/unlock` | POST | **Toteutettu** | Lähetä maksu; palauttaa 202 odotettavaan selvitykseen |
| `/app/{name}` | GET | **Toteutettu** | Tycoon 402 -portti + UtahX-välitys konttiin |
| `/app/{name}/{path}` | GET | **Toteutettu** | Alipolun välitys kontin taustaan |
| `/s3/{bucket}/{key}` | GET | **Toteutettu** | Objektin luku (paikallinen NVMe) |
| `/s3/{bucket}/{key}` | PUT/POST | **Toteutettu** | Objektin kirjoitus; valinnaiset HMAC-otsikot |
| `/s3/{bucket}/{prefix}*` | GET | **Toteutettu** | Objektien listaus |
| `/lambda/{fn}/invoke` | POST | **Toteutettu** | Serverittömän käsittelijän kutsu |
| `/lambda/{fn}` | GET | **Toteutettu** | GET-kutsu tyhjällä tapahtumalla |
| `/rds/write` | POST | **Toteutettu** | Avain-arvo -kirjoitus |
| `/rds/read/{key}` | GET | **Toteutettu** | Avain-arvo -luku |

---

## Ydinalijärjestelmät

| Komponentti | Tila | Mitä toimii tänään |
|-------------|------|-------------------|
| **Golden Master (`utahmosphere_master.py`)** | **Toteutettu** | Yhtenäinen sisääntulopiste |
| **Ydin (`utahmosphere_os.py`)** | **Toteutettu** | Täysi HTTP-multiplekseri, rekisteri, verkko |
| **UtahX Proxy (`utahx_proxy.py`)** | **Toteutettu** | Reaaliaikainen HTTP-välitys konttiporteille |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Toteutettu** | Vuokralaisen HTTP-palvelimet porteissa 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Toteutettu** | AST-validoitu käsittelijämutaatio + OTA-kanava |
| **S3 Mesh (`utah_s3_mesh.py`)** | **Toteutettu** | Paikallinen objektitallennus + HMAC |
| **Lambda Engine (`utah_lambda_engine.py`)** | **Toteutettu** | Käsittelijän kutsu ilman kuvia |
| **RDS Ledger (`utah_rds_ledger.py`)** | **Toteutettu** | JSON avain-arvo -rekisteri |
| **Quantum Ledger** | Toteutettu | Biometrinen claim + vahvistus |
| **Utah-Tycoon** | **Toteutettu** | Mempool/electrum-selvitys (`tycoon_settlement.py`), `POST /app/unlock`, HTTP 402 -portti |
| **UtahNetes Gossip** | **Toteutettu** | AuthGuard-allekirjoitettu 5 s multicast `utah_mesh_engine.py`:n kautta |
| **Global Swarm** | **Toteutettu** | Deterministinen DHT + allekirjoitettu rekisterisynkronointi |
| **AuthGuard (`ledger_auth.py`)** | **Toteutettu** | `authorized_nodes[]`-pakottaminen äänelle ja verkolle |
| **Genesis ISO (`mk_iso.sh`)** | **Toteutettu** | UEFI/hybridi flash-asennuksen rakentaja |
| **Utah-Flux UI** | Toteutettu | Tkinter-tilapaneeli |
| **Auto-Genesis (`genesis_deploy.py`)** | **Toteutettu** | Moniprosessinen orkestroija |
| **Bootstrap (`bootstrap.sh`)** | **Toteutettu** | Paljaan metallin systemd-asennus |

---

## Äänikomennot

| Komentomalli | Tila | Esimerkki |
|--------------|------|-----------|
| Claim node | Toteutettu | `"Claim node"` |
| Deploy application | Toteutettu | `"deploy application my-app"` |
| Patch application | **Toteutettu** | `"patch app my-app to add logging"` |
| Authorize node | **Toteutettu** | `"authorize node <64-char-vibe-hash>"` |
| Status / grid | Toteutettu | `"status grid"` |

---

## Käyttöönotto-vaihtoehdot

| Menetelmä | Tila | Alusta |
|-----------|------|--------|
| `python3 utahmosphere_master.py` | **Suositeltu** | Kaikki |
| `python3 utahmosphere_os.py` | Toteutettu | Kaikki |
| `python3 genesis_deploy.py` | Toteutettu | Linux / kehitys |
| `sudo bash bootstrap.sh` | **Suositeltu tuotannossa** | Linux systemd |
| `sudo bash setup.sh` | Toteutettu | Alias bootstrapille |
| `./mk_iso.sh` | **Toteutettu** | Linux — rakentaa `utah_genesis_v25.iso` |
| `docker-compose up` | Valinnainen | Vain perinteinen kätevyys |

---

## Tiekartta (jäljellä olevat puutteet)

- Alpine/vmlinuz-paketointi Genesis ISO:ssa (käynnistysvalikko dokumentoi toistaiseksi manuaalisen asennuspolun)
- Nonce/aikaleima äänikomentojen uudelleentoistoa vastaan
- `authorized_nodes`-peruutuksen käyttöliittymä
