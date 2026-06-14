# Backend Recipes

Server-side patterns for UtahMosphere workloads.

---

## Deploy via /command

**Status:** Implemented

```python
import json
import urllib.request

def deploy_app(app_name: str, acoustic_hash: str = "0" * 64, host: str = "127.0.0.1") -> dict:
    payload = json.dumps({
        "transcript": f"deploy application {app_name}",
        "acoustic_hash": acoustic_hash,
    }).encode()
    req = urllib.request.Request(
        f"http://{host}:8999/command",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

if __name__ == "__main__":
    print(deploy_app("my-service"))
```

See: [examples/voice-deploy-simulator](../../examples/voice-deploy-simulator/)

---

## HMAC Tenant Signature

**Status:** Implemented (for future storage APIs)

```python
import hmac
import hashlib
import os

SECRET = os.environ.get(
    "UTAH_SECRET_VECTOR",
    "utah_akashic_sovereign_perimeter_authorization_vector",
).encode()

def sign_request(tenant_id: str, path: str) -> str:
    return hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()

# Example
sig = sign_request("my-tenant", "/s3/bucket/key")
```

---

## Synchronized Session Store (RDS Ledger)

**Status:** Roadmap

```python
import requests

BASE = "http://localhost:8999"

def save_session(session_id, user_data):
    requests.post(f"{BASE}/rds/write", json={
        "key": f"session:{session_id}",
        "value": user_data,
    })

def get_session(session_id):
    return requests.get(f"{BASE}/rds/read/session:{session_id}").json()["value"]
```

**Interim:** Use local SQLite or Redis; migrate when RDS API ships.

---

## Container Handler Pattern

**Status:** Implemented

```python
def handler(event, context):
    """UtahContainerEngine entry point."""
    action = event.get("action", "ping")
    if action == "ping":
        return {"status": "ok"}
    return {"status": "unknown_action", "action": action}
```

Template: [container-handler](../../templates/container-handler/)

---

## Simple HTTP Microservice

**Status:** Implemented (standalone; not kernel-integrated)

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "running",
            "environment": "UtahMosphere",
        }).encode())

if __name__ == "__main__":
    HTTPServer(("", 8080), SimpleHandler).serve_forever()
```

Template: [python-http-service](../../templates/python-http-service/)

---

## Patch App via API

**Status:** Partial (appends Lazarus comments)

```python
def patch_app(app_name: str, intent: str, acoustic_hash: str = "0" * 64):
    import json, urllib.request
    payload = json.dumps({
        "transcript": f"patch app {app_name} to {intent}",
        "acoustic_hash": acoustic_hash,
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
