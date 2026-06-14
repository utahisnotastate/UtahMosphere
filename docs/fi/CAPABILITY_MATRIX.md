# Ominaisuusmatriisi

UtahMosphere OS **v27.0 Production Immutable** — suvereenit luottamusankkurit ovat valmiit.

---

## HTTP API -päätepisteet

| Päätepiste | Metodi | Tila | Huomiot |
|------------|--------|------|---------|
| `/health` | GET | **Toteutettu** | Elvytystarkistus + `build: omega-build-v27-production` + `attestation` |
| `/nonce` | GET | **Toteutettu** | Myöntää tuoreen äänikomennon noncen (30 s ikkuna) |
| `/status` | GET | **Toteutettu** | UI-tila, vuokralaiset, todentaminen, mempool-varajärjestelmän tilastot |
| `/command` | POST | **Toteutettu** | Ääni-intentti + automaattinen nonce-allekirjoitus (`voice_bridge_signed.py`) |
| `/admin/revoke-node` | POST | **Toteutettu** | Vain juuri — delegoidun solmun peruutus |
| `/app/unlock` | POST | **Toteutettu** | Lähetä maksu; mempool-varajärjestelmän selvitys |
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
| **Laitteiston todentaminen (`attestation_guard.py`)** | **Toteutettu** | TPM 2.0 PCR0-portti bootstrapissa + health |
| **Mempool-varajärjestelmä (`tycoon_failover.py`)** | **Toteutettu** | US/EU/Aasia mempool hiljainen varajärjestelmä |
| **Voice Bridge Signed (`voice_bridge_signed.py`)** | **Toteutettu** | Automaattinen `GET /nonce` + HMAC-allekirjoitus |
| **UtahX Proxy (`utahx_proxy.py`)** | **Toteutettu** | Reaaliaikainen HTTP-välitys konttiporteille |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Toteutettu** | Vuokralaisen HTTP-palvelimet porteissa 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Toteutettu** | AST-validoitu käsittelijämutaatio + OTA |
| **S3 / Lambda / RDS** | **Toteutettu** | Täysi pilvipariteetti |
| **Quantum Ledger** | **Toteutettu** | Biometrinen claim + vahvistus |
| **Utah-Tycoon** | **Toteutettu** | Varajärjestelmän mempool + electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Toteutettu** | `authorized_nodes[]`-pakottaminen |
| **Nonce-Guard (`nonce_guard.py`)** | **Toteutettu** | 30 s uudelleentoiston esto äänikomennoille |
| **UtahNetes + Swarm DHT** | **Toteutettu** | Allekirjoitettu gossip + deterministinen reititys |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Toteutettu** | Alpine vmlinuz + TPM-tietoinen bootstrap |
| **Utah-Flux peruutus-UI** | **Toteutettu** | Ylläpitopaneeli `flux_gui.py`:ssä |
| **Auto-Genesis / Bootstrap** | **Toteutettu** | systemd + todentamisportti |

---

## Äänikomennot

| Komentomalli | Tila | Esimerkki |
|--------------|------|-----------|
| Claim node | Toteutettu | `"Claim node"` |
| Authorize node | Toteutettu | `"authorize node <64-char-vibe-hash>"` |
| Deploy application | Toteutettu | `"deploy application my-app"` |
| Patch application | Toteutettu | `"patch app my-app to add logging"` |
| Status / grid | Toteutettu | `"status grid"` |

**Voice Bridge v27.0** hakee automaattisesti `GET /nonce` ja allekirjoittaa jokaisen komennon. Manuaaliset asiakkaat käyttävät `voice_bridge_signed.get_signed_payload()`.

---

## Käyttöönotto-vaihtoehdot

| Menetelmä | Tila | Alusta |
|-----------|------|--------|
| `python3 utahmosphere_master.py` | **Suositeltu** | Kaikki |
| `sudo bash bootstrap.sh` | **Suositeltu tuotannossa** | Linux + TPM (valinnainen ohitus) |
| `python3 genesis_iso_builder.py` | **Toteutettu** | Rakentaa `utah_genesis_v27.iso` |
| `./mk_iso.sh` | **Toteutettu** | Genesis ISO -rakentajan kääre |
| `python3 voice_bridge.py` | **Toteutettu** | Automaattisen nonce-allekirjoituksen ääniasiakas |

---

## Tiekartta

Kaikki v26.0:n ja aiempien versioiden tiekartan kohdat on **toteutettu** v27.0:ssa.

Tulevat parannukset:

- TPM quote -todentamisen etävahvistus (RA-TLS)
- Neljäs mempool-alue (Oseania)
- Laitteistoon sidottu vibe-print -sidonta TPM PCR:ään

Katso [API-viite](API_REFERENCE.md) ja [Kehittäjän keittokirja](DEVELOPER_COOKBOOK.md).
