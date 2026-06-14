# Võimekuste maatriks

See maatriks dokumenteerib, mida UtahMosphere OS **v25.0** täna rakendab versus mis on turundusdokumentides kirjeldatud või planeeritud tulevasteks väljalaseteks. Kasuta seda realistlike ootuste seadmiseks migratsiooni ja arenduse ajal.

---

## HTTP API lõpp-punktid

| Lõpp-punkt | Meetod | Olek | Märkused |
|------------|--------|------|----------|
| `/health` | GET | **Rakendatud** | Sõlme elusoleku päring |
| `/status` | GET | **Rakendatud** | UI olek, rentnikute nimekiri, claim olek |
| `/command` | POST | **Rakendatud** | Hääle intenti käivitus (JSON keha) |
| `/app/unlock` | POST | **Rakendatud** | Esita makse; tagastab 202 kuni arveldus |
| `/app/{name}` | GET | **Rakendatud** | Tycoon-ga kaitstud rakenduse juurdepääs (402 kuni makstud) |
| `/s3/*` | * | Planeeritud | Dokumenteeritud migratsiooni juhendis; pole veel marsruutitud |
| `/lambda/*/invoke` | POST | Planeeritud | Handler stubid luuakse ainult juurutamisel |
| `/rds/read/*`, `/rds/write` | * | Planeeritud | Register eksisteerib; HTTP marsruudid pole ühendatud |

---

## Tuuma alamsüsteemid

| Komponent | Olek | Mis täna töötab |
|-----------|------|-----------------|
| **Tuum (`utahmosphere_os.py`)** | Rakendatud | Register, hääle intentid, UtahX marsruudi manifestid, võrgu gossip |
| **Quantum Ledger** | Rakendatud | Juur-vibe claim, biomeetriline räsi kontroll, avatud režiim enne claim-i |
| **Voice Bridge** | Rakendatud | Google STT + MFCC vibe-print eraldamine → `/command` |
| **Utah-Tycoon** | **Rakendatud** | Sündmuspõhine arveldusloop, `POST /app/unlock`, HTTP 402 värav |
| **UtahNetes Gossip** | **Rakendatud** | 5s multicast sünk `utah_mesh_engine.py` kaudu, `master_registry.json` |
| **Global Swarm** | **Rakendatud** | Deterministiline DHT marsruutimine, FIND_NODE, iteratiivne peer otsing |
| **Lazarus Daemon** | Osaliselt | Lisab patch kommentaarid `handler.py`-sse (mitte täielik AST ümberkirjutus) |
| **Utah-Flux UI** | Rakendatud | Tkinter armatuurlaud, loeb `flux_ui_manifest.json` |
| **UtahX Proxy** | Osaliselt | JSON marsruudi manifestid kirjutatakse; reaalajas TCP proksi protsessi pole |

---

## Häälkäsud (autoriseeritud)

| Käsu muster | Olek | Näide |
|-------------|------|-------|
| Claim node | Rakendatud | `"Claim node"` |
| Deploy application | Rakendatud | `"deploy application my-app"` |
| Patch application | Osaliselt | `"patch app my-app to add logging"` |
| Status / grid | Rakendatud | `"status grid"` |

---

## Juurutamise valikud

| Meetod | Olek | Platvorm |
|--------|------|----------|
| `python3 utahmosphere_os.py` | Rakendatud | Kõik (määra kohalikult `UTAH_DATA_DIR`) |
| `python3 genesis_deploy.py` | Rakendatud | Linux eelistatud; Windows dev OK |
| `sudo bash setup.sh` | Rakendatud | Linux (systemd teenus) |
| `docker-compose up` | Rakendatud | Valikuline; kasutab host võrgustamist |

---

## Turvamudel

| Funktsioon | Olek | Märkused |
|------------|------|----------|
| Üks juur-vibe omanik | Rakendatud | Esimene kõneleja claim-ib sõlme |
| `authorized_nodes[]` väli | Stub | Salvestatud ledger JSON-is; koodis pole jõustatud |
| HMAC rentniku allkirjad | Dokumenteeritud | Retsept olemas; tuuma jõustamine osaliselt |
| Ed25519 allkirjastamine | Planeeritud | Dokumentides viidatud; pole rakendatud |
| Vaikimisi `UTAH_SECRET_VECTOR` | Rakendatud | Muuda tootmises (vaata [Juurdepääsukontrolli](CAPABILITY_MATRIX.md)) |

---

## Docker / Nginx seos

UtahMosphere **peamine käitusaeg** on palja riistvara Python. Docker ja Nginx on **valikulised pärand-teed**:

- `docker-compose.yaml` — mugavuswrapper kohalikeks katseteks
- `nginx.conf` — viitekonfiguratsioon; UtahX JSON manifestid on suveräänne tee
- `setup.sh` — eemaldab Docker/Nginx puhtal Linux paigaldusel (tootmise suveräänsetel sõlmedel)

Hübriidkeskkondades hoia Docker/Nginx UtahMosphere kõrval migratsiooni ajal.

---

## Teekaart (veel rakendamata)

- S3-ühilduv objektisalvestuse HTTP API
- Lambda-stiilis invoke HTTP API
- RDS ledger read/write HTTP API
- Git-põhine deploy häälkäsk
- Täielik AST mutatsioon Lazarus kaudu
- Reaalne Bitcoin mempool integratsioon Tycoon-is

Vaata versiooniajalugu: [Muudatuste logi](CAPABILITY_MATRIX.md).
