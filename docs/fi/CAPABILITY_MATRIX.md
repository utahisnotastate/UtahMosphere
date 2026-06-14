# Ominaisuusmatriisi

UtahMosphere OS **v26.0 Omega-Build FINAL** — täydellinen tiekartan toteutus.

---

## HTTP API -päätepisteet

| Päätepiste | Metodi | Tila | Huomiot |
|------------|--------|------|---------|
| `/health` | GET | **Toteutettu** | Elvytystarkistus + `build: omega-build-v26-final` |
| `/nonce` | GET | **Toteutettu** | Myöntää tuoreen äänikomennon noncen (30 s ikkuna) |
| `/status` | GET | **Toteutettu** | UI-tila, vuokralaiset, claim-tila, S3-juuri |
| `/command` | POST | **Toteutettu** | Ääni-intentti + nonce uudelleentoiston esto claimin jälkeen |
| `/admin/revoke-node` | POST | **Toteutettu** | Vain juuri — delegoidun solmun peruutus |
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
| **Quantum Ledger** | **Toteutettu** | Biometrinen claim + vahvistus |
| **Utah-Tycoon** | **Toteutettu** | Mempool/electrum-selvitys (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Toteutettu** | `authorized_nodes[]`-pakottaminen äänelle ja verkolle |
| **Nonce-Guard (`nonce_guard.py`)** | **Toteutettu** | 30 s uudelleentoiston esto äänikomennoille |
| **UtahNetes Gossip** | **Toteutettu** | AuthGuard-allekirjoitettu 5 s multicast `utah_mesh_engine.py`:n kautta |
| **Global Swarm** | **Toteutettu** | Deterministinen DHT + allekirjoitettu rekisterisynkronointi |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Toteutettu** | Alpine vmlinuz/initramfs -hybridi-ISO |
| **Utah-Flux peruutus-UI (`ui_revocation.py`)** | **Toteutettu** | Ylläpitopaneeli `flux_gui.py`:ssä |
| **Utah-Flux UI** | **Toteutettu** | Tkinter-tila + peruutuskojelauta |
| **Auto-Genesis (`genesis_deploy.py`)** | **Toteutettu** | Moniprosessinen orkestroija |
| **Bootstrap (`bootstrap.sh`)** | **Toteutettu** | Paljaan metallin systemd-asennus |

---

## Äänikomennot

| Komentomalli | Tila | Esimerkki |
|--------------|------|-----------|
| Claim node | Toteutettu | `"Claim node"` |
| Authorize node | **Toteutettu** | `"authorize node <64-char-vibe-hash>"` |
| Deploy application | Toteutettu | `"deploy application my-app"` |
| Patch application | **Toteutettu** | `"patch app my-app to add logging"` |
| Status / grid | Toteutettu | `"status grid"` |

**Claimin jälkeen:** sisällytä `nonce` + `command_signature` `GET /nonce`:sta jokaiseen `/command`-pyyntöön.

---

## Käyttöönotto-vaihtoehdot

| Menetelmä | Tila | Alusta |
|-----------|------|--------|
| `python3 utahmosphere_master.py` | **Suositeltu** | Kaikki |
| `python3 utahmosphere_os.py` | Toteutettu | Kaikki |
| `python3 genesis_deploy.py` | Toteutettu | Linux / kehitys |
| `sudo bash bootstrap.sh` | **Suositeltu tuotannossa** | Linux systemd |
| `sudo bash setup.sh` | Toteutettu | Alias bootstrapille |
| `python3 genesis_iso_builder.py` | **Toteutettu** | Linux — rakentaa `utah_genesis_v26.iso` |
| `./mk_iso.sh` | **Toteutettu** | Genesis ISO -rakentajan kääre |
| `docker-compose up` | Valinnainen | Vain perinteinen kätevyys |

---

## Tiekartta

Kaikki v25.x-tiekartan kohdat on **toteutettu** v26.0:ssa. Tuleva työ:

- Laitteiston todentaminen Genesis ISO -automaattiasennusta varten
- Monialueinen mempool-varajärjestelmä
- Voice Bridge -automaattinen nonce-allekirjoitus

Katso [API-viite](API_REFERENCE.md) ja [Kehittäjän keittokirja](DEVELOPER_COOKBOOK.md) nykyisistä toteutusyksityiskohdista.
