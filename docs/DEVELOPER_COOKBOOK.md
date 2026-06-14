### 🍳 Developer Cookbook: UtahMosphere Recipes

The cookbook is the developer entry point. For the full recipe library, see **[Recipes Index](recipes/README.md)**.

---

#### **Quick Links**

| Task | Recipe |
|------|--------|
| Deploy via API | [Backend — Deploy via /command](recipes/backend-recipes.md#deploy-via-command) |
| Health monitoring | [Ops — Health probe](recipes/ops-recipes.md#health-monitoring) |
| Payment flow (402) | [Frontend — Tycoon flow](recipes/frontend-recipes.md#tycoon-payment-flow) |
| HMAC signatures | [Backend — HMAC](recipes/backend-recipes.md#hmac-tenant-signature) |
| Voice intents | [Voice Recipes](recipes/voice-recipes.md) |

**Tutorial:** [Your First App](tutorials/05-developer-first-app.md)  
**Templates:** [templates/](../templates/) · **Starters:** [starter-projects/](../starter-projects/)

---

#### **Frontend Recipe: Direct-to-Edge Image Upload**

> **Status:** Roadmap (S3 Mesh API not yet routed). Pattern ready for migration.

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

**Implemented today:** use `fetch('http://127.0.0.1:8999/status')` — see [frontend-upload template](../templates/frontend-upload/).

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

Or run: `python examples/voice-deploy-simulator/deploy.py my-app`

---

#### **Backend Recipe: Synchronized Session Store**

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

#### **Voice Bridge Recipe: Custom Vibe-Coding**

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

Full pattern: [Voice Recipes](recipes/voice-recipes.md)

---

#### **Boilerplate: UtahMosphere Python Service**

Template: [templates/python-http-service/](../templates/python-http-service/)

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

#### **Security Note: Generating Signatures**

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

See [Access Control](ACCESS_CONTROL.md) for production hardening.
