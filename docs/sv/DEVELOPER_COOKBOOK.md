### 🍳 Utvecklarkokbok: UtahMosphere-recept

Kokboken är utvecklarens startpunkt. För det fullständiga receptbiblioteket, se **[Receptindex](recipes/README.md)**.

---

#### **Snabblänkar**

| Uppgift | Recept |
|---------|--------|
| Driftsätt via API | [Backend — Driftsätt via /command](recipes/README.md) |
| Hälsoövervakning | [Ops — Hälsokontroll](recipes/README.md) |
| Betalningsflöde (402) | [Frontend — Tycoon-flöde](recipes/README.md) |
| HMAC-signaturer | [Backend — HMAC](recipes/README.md) |
| Röstintents | [Röstrecept](recipes/README.md) |

**Guide:** [Din första app](tutorials/05-developer-first-app.md)  
**Mallar:** [templates/](../../templates/) · **Startprojekt:** [starter-projects/](../../starter-projects/)

---

#### **Frontend-recept: Direkt-till-edge-bilduppladdning**

> **Status:** Roadmap (S3 Mesh API ännu inte routat). Mönster redo för migrering.

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

**Implementerat idag:** använd `fetch('http://127.0.0.1:8999/status')` — se [frontend-upload-mall](../../templates/frontend-upload/).

---

#### **Backend-recept: Driftsätt via /command**

> **Status:** Implementerat

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

Eller kör: `python examples/voice-deploy-simulator/deploy.py my-app`

---

#### **Backend-recept: Synkroniserad sessionslagring**

> **Status:** Roadmap (RDS-ledger HTTP-routes)

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

#### **Voice Bridge-recept: Anpassad Vibe-kodning**

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

Fullständigt mönster: [Röstrecept](recipes/README.md)

---

#### **Boilerplate: UtahMosphere Python-tjänst**

Mall: [templates/python-http-service/](../../templates/python-http-service/)

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

#### **Säkerhetsnotering: Generera signaturer**

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

Se [Åtkomstkontroll](CAPABILITY_MATRIX.md) för produktionshärdning.
