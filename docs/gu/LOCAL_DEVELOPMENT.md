# Guia Desarrollu Lokal

Puede un ma'å'ñao UtahMosphere gi Windows, macOS, pat Linux sin root privileges pat siña ti usa `/var/lib` paths.

---

## Riquirement siha

- Python 3.11+
- `pip install -r requirements.txt`

**Voice Bridge ha' (ti necesario):**

- Mikrofonu + `pyaudio` (puede difisil gi Windows — usa prebuilt wheels)
- Internet para Google Speech Recognition

---

## Tutuhon På'go gi Lokal

### 1. Set i lokal data directory

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

### 2. Tutuhon i core

```bash
python utahmosphere_os.py
```

Chek:

```bash
curl http://127.0.0.1:8999/health
```

### 3. Deploy sin mikrofonu

```bash
python examples/voice-deploy-simulator/deploy.py hello
```

Pat usa curl directamente (open mode antes claim):

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application hello","acoustic_hash":"0"}'
```

### 4. Ti necesario: Voice Bridge

Gi otro terminal (core debi ma'å'ñao):

```bash
python voice_bridge.py
```

Sångan: **"Claim node"** despues **"deploy application my-app"**.

### 5. Ti necesario: Utah-Flux UI

```bash
python flux_gui.py
```

Necessita display (Tkinter). Ma skip smooth gi headless environments.

---

## Estructura Directory (lokal)

Yanggen set `UTAH_DATA_DIR` to `./.utah-data`:

```
.utah-data/
├── secure_registry.json
├── flux_ui_manifest.json
├── containers/
│   └── hello/
│       └── handler.py
└── utahx_mesh/
    └── hello.utahx.json

security/biometric_ledger.json   # lokal backup
tycoon/settlement_ledger.json    # lokal backup
```

Na'i `.utah-data/`, `security/`, `tycoon/`, yan `swarm/` gi `.gitignore` (ma cover på'go).

---

## Notas Windows

- Ma'å'ñao PowerShell komo admin ha' yanggen bind privileged ports (ti necesario para port 8999).
- `genesis_deploy.py` siña ti root gi Windows (`os.name == 'nt'`).
- `setup.sh` Linux ha'; usa pasos gi apå'ya para desarrollu lokal gi Windows.
- Para `pyaudio` issues: `pip install pipwin && pipwin install pyaudio` pat usa WSL.

---

## Notas macOS

```bash
brew install portaudio
pip install pyaudio
```

---

## Docker (todu platform siha)

```bash
docker-compose up
```

Usa host network — gi Docker Desktop Windows/Mac, port 8999 ma map gi localhost.

---

## Ma'å'ñao Examples

```bash
python examples/check-node-health/health_check.py
python examples/paid-app-access/access_app.py hello
```

---

## Configuracion IDE

Environment variables ma recommend gi IDE run config:

| Variable | Value |
|----------|-------|
| `UTAH_DATA_DIR` | `${workspaceFolder}/.utah-data` |
| `UTAH_SECRET_VECTOR` | `local-dev-secret` |

Debug entry point: `utahmosphere_os.py`

---

## Sigiente Pasos

- [Leksion: Primeru App](tutorials/05-developer-first-app.md)
- [Referensia API](API_REFERENCE.md)
- [Templates](../../templates/) yan [Starter Projects](../../starter-projects/)
