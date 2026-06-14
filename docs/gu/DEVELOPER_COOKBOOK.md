### 🍳 Cookbook para Developer: UtahMosphere Recipes

I cookbook i starting point para developers. Full recipe library: **[Indeks Recipes](recipes/README.md)**.

---

#### **Quick Links**

| Task | Resipe / Template |
|------|-------------------|
| Deploy via API | [Backend recipe gi baba](#backend-recipe-deploy-via-command) |
| Health monitoring | [Ops — usa `/health`](API_REFERENCE.md#get-health) |
| Payment flow (402) | [Frontend — Tycoon flow](../../templates/tycoon-payment-client/) |
| HMAC signatures | [Security recipe gi baba](#security-recipe-signature-generation) |
| Voice intents | [voice-command-client template](../../templates/voice-command-client/) |

**Tutorial:** [Primeru App](tutorials/05-developer-first-app.md)  
**Templates:** [templates/](../../templates/) · **Starter Projects:** [starter-projects/](../../starter-projects/)

---

#### **Frontend Recipe: Direct Edge Image Upload**

> **Status:** Roadmap (S3 Mesh API ti ma route på'go). Template ready para migration.

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

**Implemented på'go:** usa `fetch('http://127.0.0.1:8999/status')` — li'e [frontend-upload template](../../templates/frontend-upload/).

---

#### **Backend Recipe: Deploy via /command**

> **Status:** Implemented

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

Pat run: `python examples/voice-deploy-simulator/deploy.py my-app`

---

#### **Backend Recipe: Synchronized Session Storage**

> **Status:** Roadmap (RDS ledger HTTP routes)

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

#### **Voice Bridge Recipe: Custom Vibe Coding**

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

Full template: [voice-command-client](../../templates/voice-command-client/)

---

#### **Boilerplate: UtahMosphere Python Service**

Template: [templates/python-http-service/](../../templates/python-http-service/)

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

#### **Security Recipe: Signature Generation**

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

Para production hardening, set `UTAH_SECRET_VECTOR` gi environment — li'e [Guia para Desarrollo Lokal](LOCAL_DEVELOPMENT.md).
