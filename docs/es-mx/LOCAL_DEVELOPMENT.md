# Guía de desarrollo local

Ejecuta UtahMosphere en Windows, macOS o Linux sin privilegios de root ni rutas `/var/lib`.

---

## Requisitos previos

- Python 3.11+
- `pip install -r requirements.txt`

**Voice Bridge solamente (opcional):**

- Micrófono + `pyaudio` (puede ser complicado en Windows — usa wheels precompilados)
- Acceso a internet para Google Speech Recognition

---

## Inicio local rápido

### 1. Configura un directorio de datos local

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

### 2. Inicia el kernel

```bash
python utahmosphere_os.py
```

Verifica:

```bash
curl http://127.0.0.1:8999/health
```

### 3. Despliega sin micrófono

```bash
python examples/voice-deploy-simulator/deploy.py hello
```

O usa curl directamente (modo abierto antes del claim):

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application hello","acoustic_hash":"0"}'
```

### 4. Opcional: Voice Bridge

En una segunda terminal (el kernel debe estar en ejecución):

```bash
python voice_bridge.py
```

Di: **"Claim node"** y luego **"deploy application my-app"**.

### 5. Opcional: Interfaz Utah-Flux

```bash
python flux_gui.py
```

Requiere pantalla (Tkinter). Se omite sin problemas en entornos headless.

---

## Estructura de directorios (local)

Cuando `UTAH_DATA_DIR` está configurado en `./.utah-data`:

```
.utah-data/
├── secure_registry.json
├── flux_ui_manifest.json
├── containers/
│   └── hello/
│       └── handler.py
└── utahx_mesh/
    └── hello.utahx.json

security/biometric_ledger.json   # respaldo local
tycoon/settlement_ledger.json    # respaldo local
```

Agrega `.utah-data/`, `security/`, `tycoon/` y `swarm/` a `.gitignore` (ya cubierto).

---

## Notas para Windows

- Ejecuta PowerShell como Administrador solo si enlazas puertos privilegiados (no necesario para 8999).
- `genesis_deploy.py` funciona sin root en Windows (`os.name == 'nt'`).
- `setup.sh` es solo para Linux; usa los pasos de desarrollo local arriba en Windows.
- Para problemas con `pyaudio`: `pip install pipwin && pipwin install pyaudio` o usa WSL.

---

## Notas para macOS

```bash
brew install portaudio
pip install pyaudio
```

---

## Docker (todas las plataformas)

```bash
docker-compose up
```

Usa red del host — en Docker Desktop para Windows/Mac, el puerto 8999 se mapea a localhost.

---

## Ejecutar ejemplos

```bash
python examples/check-node-health/health_check.py
python examples/paid-app-access/access_app.py hello
```

---

## Configuración del IDE

Variables de entorno recomendadas en la configuración de ejecución de tu IDE:

| Variable | Valor |
|----------|-------|
| `UTAH_DATA_DIR` | `${workspaceFolder}/.utah-data` |
| `UTAH_SECRET_VECTOR` | `local-dev-secret` |

Punto de entrada para depuración: `utahmosphere_os.py`

---

## Próximos pasos

- [Tutorial: Tu primera aplicación](tutorials/05-developer-first-app.md)
- [Referencia de API](API_REFERENCE.md)
- [Plantillas](../../templates/) y [Proyectos de arranque](../../starter-projects/)
