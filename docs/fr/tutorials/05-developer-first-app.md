# Tutoriel : Votre première application

**Public :** Développeurs frontend et backend  
**Durée :** 30 minutes  
**Objectif :** Déployer, accéder et étendre une application sur UtahMosphere de bout en bout

---

## Prérequis

- Python 3.11+
- `pip install -r requirements.txt`
- [Guide de développement local](../LOCAL_DEVELOPMENT.md) complété (optionnel)

---

## Étape 1 : Démarrer le noyau

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

Confirmation :

```bash
curl http://127.0.0.1:8999/health
```

---

## Étape 2 : Déployer `hello-world`

```bash
python examples/voice-deploy-simulator/deploy.py hello-world
```

La réponse attendue inclut le port `8200` (premier locataire).

Vérifier le statut :

```bash
curl http://127.0.0.1:8999/status
```

---

## Étape 3 : Accéder à votre application (porte de paiement)

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Première réponse : **402 Payment Required** avec adresse Bitcoin.

Attendez ~60 secondes (règlement simulé), réessayez :

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Réponse : **200 Unlocked**.

Ou utilisez le script d'aide :

```bash
python examples/paid-app-access/access_app.py hello-world
```

---

## Étape 4 : Personnaliser le handler

Modifiez :

```
.utah-data/containers/hello-world/handler.py
```

```python
def handler(event, context):
    return {
        "status": "active",
        "message": "Hello from my first UtahMosphere app!",
        "event": event,
    }
```

Corriger via voix/API :

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"patch app hello-world to add greeting","acoustic_hash":"0"}'
```

---

## Étape 5 : Construire un vrai service (modèle)

Copiez le projet de démarrage :

```bash
cp -r starter-projects/minimal-api my-api
cd my-api
python handler_service.py
```

Déployez sur UtahMosphere :

```bash
python ../examples/voice-deploy-simulator/deploy.py my-api
```

---

## Étape 6 : Intégration frontend

Utilisez le modèle `templates/frontend-upload/` ou récupérez le statut depuis votre application :

```javascript
const res = await fetch("http://127.0.0.1:8999/status");
const data = await res.json();
console.log("Active tenants:", data.tenants);
```

---

## Étape 7 : Générer des signatures HMAC (APIs de stockage futures)

```python
import hmac
import hashlib

SECRET = b"utah_akashic_sovereign_perimeter_authorization_vector"
tenant_id = "hello-world"
path = "/s3/assets/photo.jpg"
sig = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## Ce que vous avez construit

- Application déployée via l'API `/command`
- Navigation dans le flux de paiement HTTP 402 Tycoon
- `handler.py` personnalisé
- Frontend connecté à `/status`

---

## Étapes suivantes

- [Guide du développeur](../DEVELOPER_COOKBOOK.md)
- [Index des recettes](../recipes/README.md)
- [Référence API](../API_REFERENCE.md)
