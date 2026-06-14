# Paikallisen kehityksen opas

Aja UtahMosphere Windowsissa, macOS:ssä tai Linuxissa ilman root-oikeuksia tai `/var/lib`-polkuja.

---

## Esivaatimukset

- Python 3.11+
- `pip install -r requirements.txt`

**Vain Voice Bridge (valinnainen):**

- Mikrofoni + `pyaudio` (voi olla hankala Windowsissa — käytä valmiita wheelejä)
- Internet-yhteys Google Speech Recognitionille

---

## Nopea paikallinen aloitus

### 1. Aseta paikallinen datahakemisto

```powershell
# Windows PowerShell
$env:UTAH_DATA_DIR = "$PWD\.utah-data"
$env:UTAH_SECRET_VECTOR = "dev-only-change-me"
```

```bash
# macOS / Linux
export UTAH_DATA_DIR="$(pwd)/.utah-data"
export UTAH_SECRET_VECTOR="dev-only-change-me"
```

### 2. Käynnistä ydin

```bash
python utahmosphere_os.py
```

Varmista:

```bash
curl http://127.0.0.1:8999/health
```

### 3. Käyttöönotto ilman mikrofonia

```bash
python examples/voice-deploy-simulator/deploy.py hello
```

Tai käytä curlia suoraan (avoin tila ennen claimia):

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application hello","acoustic_hash":"0"}'
```

### 4. Valinnainen: Voice Bridge

Toisessa terminaalissa (ydin täytyy olla käynnissä):

```bash
python voice_bridge.py
```

Sano: **"Claim node"** sitten **"deploy application my-app"**.

### 5. Valinnainen: Utah-Flux UI

```bash
python flux_gui.py
```

Vaatii näytön (Tkinter). Ohittaa sulavasti headless-ympäristöissä.

---

## Hakemistorakenne (paikallinen)

Kun `UTAH_DATA_DIR` on asetettu `./.utah-data`:ksi:

```
.utah-data/
├── secure_registry.json
├── flux_ui_manifest.json
├── containers/
│   └── hello/
│       └── handler.py
└── utahx_mesh/
    └── hello.utahx.json

security/biometric_ledger.json   # paikallinen varmuuskopio
tycoon/settlement_ledger.json    # paikallinen varmuuskopio
```

Lisää `.utah-data/`, `security/`, `tycoon/` ja `swarm/` `.gitignore`-tiedostoon (jo katettu).

---

## Windows-huomiot

- Suorita PowerShell ylläpitäjänä vain jos sidot etuoikeutettuja portteja (ei tarvita portille 8999).
- `genesis_deploy.py` toimii ilman rootia Windowsissa (`os.name == 'nt'`).
- `setup.sh` on vain Linuxille; käytä yllä olevia paikallisen kehityksen vaiheita Windowsissa.
- `pyaudio`-ongelmiin: `pip install pipwin && pipwin install pyaudio` tai käytä WSL:ää.

---

## macOS-huomiot

```bash
brew install portaudio
pip install pyaudio
```

---

## Docker (kaikilla alustoilla)

```bash
docker-compose up
```

Käyttää host-verkkoa — Docker Desktopissa Windowsissa/Macissa portti 8999 kartoitetaan localhostiin.

---

## Esimerkkien ajaminen

```bash
python examples/check-node-health/health_check.py
python examples/paid-app-access/access_app.py hello
```

---

## IDE-asetukset

Suositellut ympäristömuuttujat IDE:n ajokonfiguraatiossa:

| Muuttuja | Arvo |
|----------|------|
| `UTAH_DATA_DIR` | `${workspaceFolder}/.utah-data` |
| `UTAH_SECRET_VECTOR` | `local-dev-secret` |

Virheenkorjauksen aloituspiste: `utahmosphere_os.py`

---

## Seuraavat vaiheet

- [Opas: Ensimmäinen sovellus](tutorials/05-developer-first-app.md)
- [API-viite](API_REFERENCE.md)
- [Mallit](../../templates/) ja [Aloitusprojektit](../../starter-projects/)
