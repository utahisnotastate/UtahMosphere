### 🍳 Arendaja retseptiraamat: UtahMosphere retseptid

Retseptiraamat on arendaja sissepääs. Täieliku retseptikogu jaoks vaata **[Retseptide registrit](recipes/README.md)**.

---

#### **Kiirlingid**

| Ülesanne | Retsept |
|----------|---------|
| Juuruta API kaudu | [Backend — Juuruta /command kaudu](recipes/README.md) |
| Tervise jälgimine | [Ops — Tervise päring](recipes/README.md) |
| Maksevoog (402) | [Frontend — Tycoon voog](recipes/README.md) |
| HMAC allkirjad | [Backend — HMAC](recipes/README.md) |
| Hääle intentid | [Hääle retseptid](recipes/README.md) |

**Õpetus:** [Sinu esimene rakendus](tutorials/05-developer-first-app.md)  
**Mallid:** [templates/](../../templates/) · **Algprojektid:** [starter-projects/](../../starter-projects/)

---

#### **Frontend retsept: Otsene serva pildi üleslaadimine**

> **Olek:** Teekaart (S3 Mesh API pole veel marsruutitud). Muster valmis migratsiooniks.

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

**Täna rakendatud:** kasuta `fetch('http://127.0.0.1:8999/status')` — vaata [frontend-upload malli](../../templates/frontend-upload/).

---

#### **Backend retsept: Juuruta /command kaudu**

> **Olek:** Rakendatud

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

Või käivita: `python examples/voice-deploy-simulator/deploy.py my-app`

---

#### **Backend retsept: Sünkroniseeritud sessiooni hoidla**

> **Olek:** Teekaart (RDS ledger HTTP marsruudid)

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

#### **Hääle sild retsept: Kohandatud Vibe-Coding**

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

Täielik muster: [Hääle retseptid](recipes/README.md)

---

#### **Boilerplate: UtahMosphere Python teenus**

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

#### **Turvalisuse märkus: Allkirjade genereerimine**

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

Vaata tootmise tugevdamist: [Juurdepääsukontroll](CAPABILITY_MATRIX.md).
