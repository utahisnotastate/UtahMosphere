### 🍳 Kehittäjän keittokirja: UtahMosphere-reseptit

Keittokirja on kehittäjän aloituspiste. Täydellinen reseptikirjasto: **[Reseptihakemisto](recipes/README.md)**.

---

#### **Pikalinkit**

| Tehtävä | Resepti |
|---------|---------|
| Käyttöönotto API:n kautta | [Backend — Käyttöönotto /command-kautta](recipes/README.md) |
| Terveysseuranta | [Ops — Terveystarkistus](recipes/README.md) |
| Maksuvirta (402) | [Frontend — Tycoon-virta](recipes/README.md) |
| HMAC-allekirjoitukset | [Backend — HMAC](recipes/README.md) |
| Ääni-intentit | [Äänireseptit](recipes/README.md) |

**Opas:** [Ensimmäinen sovellus](tutorials/05-developer-first-app.md)  
**Mallit:** [templates/](../../templates/) · **Aloitusprojektit:** [starter-projects/](../../starter-projects/)

---

#### **Frontend-resepti: Suora reunalle kuvan lataus**

> **Tila:** Tiekartta (S3 Mesh API ei vielä reititetty). Malli valmis migraatiota varten.

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

**Toteutettu tänään:** käytä `fetch('http://127.0.0.1:8999/status')` — katso [frontend-upload-malli](../../templates/frontend-upload/).

---

#### **Backend-resepti: Käyttöönotto /command-kautta**

> **Tila:** Toteutettu

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

Tai suorita: `python examples/voice-deploy-simulator/deploy.py my-app`

---

#### **Backend-resepti: Synkronoitu istuntotallennus**

> **Tila:** Tiekartta (RDS-kirjanpidon HTTP-reitit)

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

#### **Voice Bridge -resepti: Mukautettu Vibe-koodaus**

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

Täydellinen malli: [Äänireseptit](recipes/README.md)

---

#### **Pohja: UtahMosphere Python-palvelu**

Malli: [templates/python-http-service/](../../templates/python-http-service/)

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

#### **Turvallisuushuomio: Allekirjoitusten luominen**

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

Katso [Pääsynhallinta](CAPABILITY_MATRIX.md) tuotantokovettamiseen.
