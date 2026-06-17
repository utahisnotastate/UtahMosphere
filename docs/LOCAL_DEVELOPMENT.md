# Local Development Guide

Run UtahMosphere on Windows, macOS, or Linux without root privileges or `/var/lib` paths.

---

## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`

**Voice Bridge only (optional):**

- Microphone + `pyaudio` (can be tricky on Windows — use pre-built wheels)
- Internet access for Google Speech Recognition

---

## Quick Local Start

### 1. Set a local data directory

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

### 2. Start the kernel

```bash
python utahmosphere_os.py
```

Verify:

```bash
curl http://127.0.0.1:8999/health
```

### 3. Deploy without a microphone

```bash
python examples/voice-deploy-simulator/deploy.py hello
```

Or use curl directly (open mode before claim):

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application hello","acoustic_hash":"0"}'
```

### 4. Optional: Voice Bridge

In a second terminal (kernel must be running):

```bash
python voice_bridge.py
```

Say: **"Claim node"** then **"deploy application my-app"**.

### 5. Optional: Utah-Flux UI

```bash
python flux_gui.py
```

Requires a display (Tkinter). Skips gracefully in headless environments.

---

## Skip Attestation (Dev)

On Linux/macOS without TPM:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
export UTAH_DHT_FEDERATION_ENFORCE=0
export UTAH_QUORUM_ENFORCE=0
export UTAH_OMNI_ENFORCE=1
export UTAH_OMNI_MCP_ENFORCE=0
export UTAH_OMNI_EXEC_ENFORCE=0
export UTAH_OMNI_PROVIDER=sovereign
export UTAH_WITNESS_ENFORCE=0
export UTAH_LAZARUS_AUTO_RESTORE=0
export UTAH_LAZARUS_KEXEC_ENFORCE=0
export UTAH_STATE_DIFF_ENFORCE=0
export UTAH_PCR_DRIFT_ENFORCE=0
export UTAH_PCR_ROLLBACK_ENFORCE=0
```

On Windows PowerShell:

```powershell
$env:UTAH_ATTESTATION_ENFORCE = "0"
$env:UTAH_TPM_LOCK_ENFORCE = "0"
$env:UTAH_RA_TLS_ENFORCE = "0"
$env:UTAH_RA_TLS_GUARD_ENFORCE = "0"
$env:UTAH_DHT_FEDERATION_ENFORCE = "0"
$env:UTAH_QUORUM_ENFORCE = "0"
$env:UTAH_OMNI_ENFORCE = "1"
$env:UTAH_OMNI_MCP_ENFORCE = "0"
$env:UTAH_OMNI_EXEC_ENFORCE = "0"
$env:UTAH_OMNI_PROVIDER = "sovereign"
$env:UTAH_WITNESS_ENFORCE = "0"
$env:UTAH_LAZARUS_AUTO_RESTORE = "0"
$env:UTAH_LAZARUS_KEXEC_ENFORCE = "0"
$env:UTAH_STATE_DIFF_ENFORCE = "0"
$env:UTAH_PCR_DRIFT_ENFORCE = "0"
$env:UTAH_PCR_ROLLBACK_ENFORCE = "0"
```

---

## Directory Layout (Local)

When `UTAH_DATA_DIR` is set to `./.utah-data`:

```
.utah-data/
├── secure_registry.json
├── flux_ui_manifest.json
├── containers/
│   └── hello/
│       └── handler.py
└── utahx_mesh/
    └── hello.utahx.json

security/biometric_ledger.json   # local fallback
tycoon/settlement_ledger.json    # local fallback
```

Add `.utah-data/`, `security/`, `tycoon/`, and `swarm/` to `.gitignore` (already covered).

---

## Windows Notes

- Run PowerShell as Administrator only if binding privileged ports (not needed for 8999).
- `genesis_deploy.py` works without root on Windows (`os.name == 'nt'`).
- `setup.sh` is Linux-only; use local dev steps above on Windows.
- For `pyaudio` issues: `pip install pipwin && pipwin install pyaudio` or use WSL.

---

## macOS Notes

```bash
brew install portaudio
pip install pyaudio
```

---

## Docker (All Platforms)

```bash
docker-compose up
```

Uses host networking — on Docker Desktop for Windows/Mac, port 8999 maps to localhost.

---

## Running Examples

```bash
python examples/check-node-health/health_check.py
python examples/paid-app-access/access_app.py hello
```

---

## IDE Setup

Recommended environment variables in your IDE run configuration:

| Variable | Value |
|----------|-------|
| `UTAH_DATA_DIR` | `${workspaceFolder}/.utah-data` |
| `UTAH_SECRET_VECTOR` | `local-dev-secret` |

Entry point for debugging: `utahmosphere_os.py`

---

## Next Steps

- [Tutorial: Your First App](tutorials/05-developer-first-app.md)
- [API Reference](API_REFERENCE.md)
- [Templates](../templates/) and [Starter Projects](../starter-projects/)
