# Guide de développement local

Exécutez UtahMosphere sous Windows, macOS ou Linux sans privilèges root ni chemins `/var/lib`.

---

## Prérequis

- Python 3.11+
- `pip install -r requirements.txt`

**Voice Bridge uniquement (optionnel) :**

- Microphone + `pyaudio` (peut être délicat sous Windows — utilisez des wheels précompilés)
- Accès Internet pour Google Speech Recognition

---

## Démarrage local rapide

### 1. Définir un répertoire de données local

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

### 2. Démarrer le noyau

```bash
python utahmosphere_os.py
```

Vérification :

```bash
curl http://127.0.0.1:8999/health
```

### 3. Déployer sans microphone

```bash
python examples/voice-deploy-simulator/deploy.py hello
```

Ou utilisez curl directement (mode ouvert avant la revendication) :

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application hello","acoustic_hash":"0"}'
```

### 4. Optionnel : Voice Bridge

Dans un second terminal (le noyau doit être en cours d'exécution) :

```bash
python voice_bridge.py
```

Dites : **"Claim node"** puis **"deploy application my-app"**.

### 5. Optionnel : Interface Utah-Flux

```bash
python flux_gui.py
```

Nécessite un affichage (Tkinter). Se désactive gracieusement en environnement sans interface graphique.

---

## Structure des répertoires (local)

Lorsque `UTAH_DATA_DIR` est défini sur `./.utah-data` :

```
.utah-data/
├── secure_registry.json
├── flux_ui_manifest.json
├── containers/
│   └── hello/
│       └── handler.py
└── utahx_mesh/
    └── hello.utahx.json

security/biometric_ledger.json   # repli local
tycoon/settlement_ledger.json    # repli local
```

Ajoutez `.utah-data/`, `security/`, `tycoon/` et `swarm/` à `.gitignore` (déjà couvert).

---

## Notes Windows

- Exécutez PowerShell en tant qu'administrateur uniquement si vous liez des ports privilégiés (non nécessaire pour 8999).
- `genesis_deploy.py` fonctionne sans root sous Windows (`os.name == 'nt'`).
- `setup.sh` est réservé à Linux ; utilisez les étapes de dev local ci-dessus sous Windows.
- Pour les problèmes `pyaudio` : `pip install pipwin && pipwin install pyaudio` ou utilisez WSL.

---

## Notes macOS

```bash
brew install portaudio
pip install pyaudio
```

---

## Docker (toutes plateformes)

```bash
docker-compose up
```

Utilise le réseau hôte — sur Docker Desktop pour Windows/Mac, le port 8999 est mappé sur localhost.

---

## Exécution des exemples

```bash
python examples/check-node-health/health_check.py
python examples/paid-app-access/access_app.py hello
```

---

## Configuration IDE

Variables d'environnement recommandées dans la configuration d'exécution de votre IDE :

| Variable | Valeur |
|----------|--------|
| `UTAH_DATA_DIR` | `${workspaceFolder}/.utah-data` |
| `UTAH_SECRET_VECTOR` | `local-dev-secret` |

Point d'entrée pour le débogage : `utahmosphere_os.py`

---

## Étapes suivantes

- [Tutoriel : Votre première application](tutorials/05-developer-first-app.md)
- [Référence API](API_REFERENCE.md)
- Modèles `templates/` et projets de démarrage `starter-projects/`
