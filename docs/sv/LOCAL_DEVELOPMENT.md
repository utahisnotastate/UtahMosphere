# Guide för lokal utveckling

Kör UtahMosphere på Windows, macOS eller Linux utan root-privilegier eller `/var/lib`-sökvägar.

---

## Förutsättningar

- Python 3.11+
- `pip install -r requirements.txt`

**Endast Voice Bridge (valfritt):**

- Mikrofon + `pyaudio` (kan vara knepigt på Windows — använd förbyggda wheels)
- Internetåtkomst för Google Speech Recognition

---

## Snabb lokal start

### 1. Ange en lokal datakatalog

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

### 2. Starta kärnan

```bash
python utahmosphere_os.py
```

Verifiera:

```bash
curl http://127.0.0.1:8999/health
```

### 3. Driftsätt utan mikrofon

```bash
python examples/voice-deploy-simulator/deploy.py hello
```

Eller använd curl direkt (öppet läge före claim):

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application hello","acoustic_hash":"0"}'
```

### 4. Valfritt: Voice Bridge

I en andra terminal (kärnan måste köra):

```bash
python voice_bridge.py
```

Säg: **"Claim node"** sedan **"deploy application my-app"**.

### 5. Valfritt: Utah-Flux UI

```bash
python flux_gui.py
```

Kräver skärm (Tkinter). Hoppar över smidigt i headless-miljöer.

---

## Kataloglayout (lokal)

När `UTAH_DATA_DIR` är satt till `./.utah-data`:

```
.utah-data/
├── secure_registry.json
├── flux_ui_manifest.json
├── containers/
│   └── hello/
│       └── handler.py
└── utahx_mesh/
    └── hello.utahx.json

security/biometric_ledger.json   # lokal fallback
tycoon/settlement_ledger.json    # lokal fallback
```

Lägg till `.utah-data/`, `security/`, `tycoon/` och `swarm/` i `.gitignore` (redan täckt).

---

## Windows-noteringar

- Kör PowerShell som administratör endast om du binder privilegierade portar (behövs inte för 8999).
- `genesis_deploy.py` fungerar utan root på Windows (`os.name == 'nt'`).
- `setup.sh` är endast Linux; använd lokala utvecklingssteg ovan på Windows.
- För `pyaudio`-problem: `pip install pipwin && pipwin install pyaudio` eller använd WSL.

---

## macOS-noteringar

```bash
brew install portaudio
pip install pyaudio
```

---

## Docker (alla plattformar)

```bash
docker-compose up
```

Använder host-nätverk — på Docker Desktop för Windows/Mac mappas port 8999 till localhost.

---

## Köra exempel

```bash
python examples/check-node-health/health_check.py
python examples/paid-app-access/access_app.py hello
```

---

## IDE-konfiguration

Rekommenderade miljövariabler i din IDE-körkonfiguration:

| Variabel | Värde |
|----------|-------|
| `UTAH_DATA_DIR` | `${workspaceFolder}/.utah-data` |
| `UTAH_SECRET_VECTOR` | `local-dev-secret` |

Startpunkt för felsökning: `utahmosphere_os.py`

---

## Nästa steg

- [Guide: Din första app](tutorials/05-developer-first-app.md)
- [API-referens](API_REFERENCE.md)
- [Mallar](../../templates/) och [Startprojekt](../../starter-projects/)
