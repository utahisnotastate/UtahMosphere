### 🍳 Guide du développeur : Recettes UtahMosphere

Le guide du développeur est le point d'entrée pour les développeurs. Pour la bibliothèque complète de recettes, consultez l'**[Index des recettes](recipes/README.md)**.

---

#### **Liens rapides**

| Tâche | Recette |
|-------|---------|
| Déployer via API | [Index des recettes](recipes/README.md) |
| Surveillance de santé | [Index des recettes](recipes/README.md) |
| Flux de paiement (402) | [Index des recettes](recipes/README.md) |
| Signatures HMAC | [Index des recettes](recipes/README.md) |
| Intentions vocales | [Index des recettes](recipes/README.md) |

**Tutoriel :** [Votre première application](tutorials/05-developer-first-app.md)  
**Modèles :** `templates/` · **Projets de démarrage :** `starter-projects/`

---

#### **Recette frontend : Téléversement d'image direct vers l'edge**

> **Statut :** Feuille de route (API S3 Mesh pas encore routée). Modèle prêt pour la migration.

```javascript
async function uploadToUtah(file, tenantId, signature) {
  const response = await fetch(`http://utahmosphere.local:8999/s3/assets/${file.name}`, {
    method: 'POST',
    headers: {
      'X-Utah-Tenant-ID': tenantId,
      'X-Utah-Signature': signature,
      'Content-Type': file.type
    },
    body: file
  });
  return await response.json();
}
```

**Implémenté aujourd'hui :** utilisez `fetch('http://127.0.0.1:8999/status')` — voir le modèle `templates/frontend-upload/`.

---

#### **Recette backend : Déployer via /command**

> **Statut :** Implémenté

```python
import json, urllib.request

def deploy(app_name):
    payload = json.dumps({
        "transcript": f"deploy application {app_name}",
        "acoustic_hash": "0" * 64,
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:8999/command",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
```

Ou exécutez : `python examples/voice-deploy-simulator/deploy.py my-app`

---

#### **Recette backend : Magasin de sessions synchronisé**

> **Statut :** Feuille de route (routes HTTP du registre RDS)

```python
import requests

def save_session(session_id, user_data):
    url = "http://localhost:8999/rds/write"
    payload = {"key": f"session:{session_id}", "value": user_data}
    requests.post(url, json=payload)

def get_session(session_id):
    url = f"http://localhost:8999/rds/read/session:{session_id}"
    return requests.get(url).json()['value']
```

---

#### **Recette Voice Bridge : Vibe-coding personnalisé**

```python
CUSTOM_INTENTS = {
    "go dark mode": lambda: print("[Vibe] Initiating aesthetic shift..."),
}

def handle_custom(transcript):
    for phrase, action in CUSTOM_INTENTS.items():
        if phrase in transcript.lower():
            action()
            return True
    return False
```

Modèle complet : [Index des recettes](recipes/README.md)

---

#### **Modèle de base : Service Python UtahMosphere**

Modèle : `templates/python-http-service/`

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "running", "environment": "UtahMosphere"}).encode())

if __name__ == "__main__":
    HTTPServer(('', 8080), SimpleHandler).serve_forever()
```

---

#### **Note de sécurité : Génération de signatures**

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

Consultez la [Référence API](API_REFERENCE.md) pour le durcissement en production.
