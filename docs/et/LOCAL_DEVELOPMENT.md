# Kohaliku arenduse juhend

Käivita UtahMosphere Windowsis, macOS-is või Linuxis ilma root õiguste või `/var/lib` teedeta.

---

## Eeltingimused

- Python 3.11+
- `pip install -r requirements.txt`

**Ainult Voice Bridge (valikuline):**

- Mikrofon + `pyaudio` (Windowsis võib olla keeruline — kasuta eelkompleeritud wheel-e)
- Internet Google Speech Recognition jaoks

---

## Kiire kohalik start

### 1. Määra kohalik andmekataloog

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

### 2. Käivita tuum

```bash
python utahmosphere_os.py
```

Kontrolli:

```bash
curl http://127.0.0.1:8999/health
```

### 3. Juuruta ilma mikrofonita

```bash
python examples/voice-deploy-simulator/deploy.py hello
```

Või kasuta curl otse (avatud režiim enne claim-i):

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application hello","acoustic_hash":"0"}'
```

### 4. Valikuline: Voice Bridge

Teises terminalis (tuum peab töötama):

```bash
python voice_bridge.py
```

Ütle: **"Claim node"** siis **"deploy application my-app"**.

### 5. Valikuline: Utah-Flux UI

```bash
python flux_gui.py
```

Nõuab ekraani (Tkinter). Jätab peaga keskkondades vaikselt vahele.

---

## Kataloogi paigutus (kohalik)

Kui `UTAH_DATA_DIR` on seatud `./.utah-data`:

```
.utah-data/
├── secure_registry.json
├── flux_ui_manifest.json
├── containers/
│   └── hello/
│       └── handler.py
└── utahx_mesh/
    └── hello.utahx.json

security/biometric_ledger.json   # kohalik varuvariant
tycoon/settlement_ledger.json    # kohalik varuvariant
```

Lisa `.utah-data/`, `security/`, `tycoon/` ja `swarm/` `.gitignore`-i (juba kaetud).

---

## Windowsi märkused

- Käivita PowerShell administraatorina ainult kui seod privileegitud porte (8999 jaoks pole vaja).
- `genesis_deploy.py` töötab Windowsis ilma rootita (`os.name == 'nt'`).
- `setup.sh` on ainult Linuxile; Windowsis kasuta kohaliku arenduse samme ülal.
- `pyaudio` probleemide korral: `pip install pipwin && pipwin install pyaudio` või kasuta WSL-i.

---

## macOS märkused

```bash
brew install portaudio
pip install pyaudio
```

---

## Docker (kõik platvormid)

```bash
docker-compose up
```

Kasutab host võrgustamist — Docker Desktop Windowsis/Macis kaardistab port 8999 localhost-ile.

---

## Näidete käivitamine

```bash
python examples/check-node-health/health_check.py
python examples/paid-app-access/access_app.py hello
```

---

## IDE seadistus

Soovitatud keskkonnamuutujad IDE käivituskonfiguratsioonis:

| Muutuja | Väärtus |
|---------|---------|
| `UTAH_DATA_DIR` | `${workspaceFolder}/.utah-data` |
| `UTAH_SECRET_VECTOR` | `local-dev-secret` |

Silumise sissepääs: `utahmosphere_os.py`

---

## Järgmised sammud

- [Õpetus: Sinu esimene rakendus](tutorials/05-developer-first-app.md)
- [API viide](API_REFERENCE.md)
- [Mallid](../../templates/) ja [Algprojektid](../../starter-projects/)
