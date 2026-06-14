# Ominaisuusmatriisi

Tämä matriisi dokumentoi, mitä UtahMosphere OS **v25.0** toteuttaa tänään verrattuna siihen, mitä markkinointidokumenteissa kuvataan tai mitä on suunniteltu tuleville julkaisuille. Käytä sitä asettaaksesi realistiset odotukset migraation ja kehityksen aikana.

---

## HTTP API -päätepisteet

| Päätepiste | Metodi | Tila | Huomiot |
|------------|--------|------|---------|
| `/health` | GET | **Toteutettu** | Solmun elvytystarkistus |
| `/status` | GET | **Toteutettu** | UI-tila, vuokralaisluettelo, claim-tila |
| `/command` | POST | **Toteutettu** | Ääni-intentin suoritus (JSON-runko) |
| `/app/unlock` | POST | **Toteutettu** | Lähetä maksu; palauttaa 202 odotettavaan selvitykseen |
| `/app/{name}` | GET | **Toteutettu** | Tycoon-portin takana oleva sovelluspääsy (402 kunnes maksettu) |
| `/s3/*` | * | Suunniteltu | Dokumentoitu migraatiooppaassa; ei vielä reititetty |
| `/lambda/*/invoke` | POST | Suunniteltu | Käsittelijäpohjat luodaan vain käyttöönotossa |
| `/rds/read/*`, `/rds/write` | * | Suunniteltu | Rekisteri on olemassa; HTTP-reittejä ei kytketty |

---

## Ydinalijärjestelmät

| Komponentti | Tila | Mitä toimii tänään |
|-------------|------|-------------------|
| **Ydin (`utahmosphere_os.py`)** | Toteutettu | Rekisteri, ääni-intentit, UtahX-reittimanifestit, mesh-gossip |
| **Quantum Ledger** | Toteutettu | Juuri-vibe-claim, biometrinen hash-vahvistus, avoin tila ennen claimia |
| **Voice Bridge** | Toteutettu | Google STT + MFCC vibe-print -poiminta → `/command` |
| **Utah-Tycoon** | **Toteutettu** | Tapahtumapohainen selvityssilmukka, `POST /app/unlock`, HTTP 402 -portti |
| **UtahNetes Gossip** | **Toteutettu** | 5 s multicast-synkronointi `utah_mesh_engine.py`:n kautta, `master_registry.json` |
| **Global Swarm** | **Toteutettu** | Deterministinen DHT-reititys, FIND_NODE, iteratiivinen vertaishaku |
| **Lazarus Daemon** | Osittainen | Liittää korjauskommentteja `handler.py`:hen (ei täyttä AST-uudelleenkirjoitusta) |
| **Utah-Flux UI** | Toteutettu | Tkinter-hallintapaneeli lukee `flux_ui_manifest.json` |
| **UtahX Proxy** | Osittainen | JSON-reittimanifestit kirjoitetaan; ei live TCP-välityspalvelinprosessia |

---

## Äänikomennot (valtuutettu)

| Komentomalli | Tila | Esimerkki |
|--------------|------|-----------|
| Claim node | Toteutettu | `"Claim node"` |
| Deploy application | Toteutettu | `"deploy application my-app"` |
| Patch application | Osittainen | `"patch app my-app to add logging"` |
| Status / grid | Toteutettu | `"status grid"` |

---

## Käyttöönotto-vaihtoehdot

| Menetelmä | Tila | Alusta |
|-----------|------|--------|
| `python3 utahmosphere_os.py` | Toteutettu | Kaikki (aseta `UTAH_DATA_DIR` paikallisesti) |
| `python3 genesis_deploy.py` | Toteutettu | Linux suositeltu; Windows dev OK |
| `sudo bash setup.sh` | Toteutettu | Linux (systemd-palvelu) |
| `docker-compose up` | Toteutettu | Valinnainen; käyttää host-verkkoa |

---

## Turvallisuusmalli

| Ominaisuus | Tila | Huomiot |
|------------|------|---------|
| Yksi juuri-vibe-omistaja | Toteutettu | Ensimmäinen claimaava puhuja omistaa solmun |
| `authorized_nodes[]`-kenttä | Stub | Tallennettu ledger JSON:iin; ei pakotettu koodissa |
| HMAC-vuokralaisallekirjoitukset | Dokumentoitu | Resepti tarjolla; ytimen pakottaminen osittainen |
| Ed25519-allekirjoitus | Suunniteltu | Dokumentaatio viittaa; ei toteutettu |
| Oletus `UTAH_SECRET_VECTOR` | Toteutettu | Vaihda tuotannossa (katso [Pääsynhallinta](CAPABILITY_MATRIX.md)) |

---

## Docker / Nginx -suhde

UtahMospheren **ensisijainen ajonaika** on paljaalla metallilla Python. Docker ja Nginx ovat **valinnaisia perinteisiä polkuja**:

- `docker-compose.yaml` — kätevä kääre paikallisiin kokeiluihin
- `nginx.conf` — viitekonfiguraatio; UtahX JSON-manifestit ovat suvereeni polku
- `setup.sh` — poistaa Docker/Nginx puhtailla Linux-asennuksilla (tuotannon suvereenit solmut)

Hybridiympäristöissä pidä Docker/Nginx rinnalla UtahMospheren kanssa migraation aikana.

---

## Tiekartta (ei vielä toteutettu)

- S3-yhteensopiva objektitallennuksen HTTP API
- Lambda-tyylinen invoke HTTP API
- RDS-kirjanpidon read/write HTTP API
- Git-pohjainen deploy-äänikomento
- Täysi AST-mutaatio Lazaruksen kautta
- Oikea Bitcoin-mempool-integraatio Tycoonissa

Katso [Muutosloki](CAPABILITY_MATRIX.md) versiohistoriasta.
