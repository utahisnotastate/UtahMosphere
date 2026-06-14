# Leksion: Primeru App

**Para håyi:** Frontend yan backend developers  
**Tiempo:** 30 minutos  
**Meta:** Deploy app, usa, yan extend gi UtahMosphere end-to-end

---

## Riquirement siha

- Python 3.11+
- `pip install -r requirements.txt`
- [Guia Desarrollu Lokal](../LOCAL_DEVELOPMENT.md) ma complete (ti necesario)

---

## Paso 1: Tutuhon i core

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

Chek:

```bash
curl http://127.0.0.1:8999/health
```

---

## Paso 2: Deploy `hello-world`

```bash
python examples/voice-deploy-simulator/deploy.py hello-world
```

Expected response includes port `8200` (first tenant).

Chek status:

```bash
curl http://127.0.0.1:8999/status
```

---

## Paso 3: Usa i app-mu (tollbooth)

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

First response: **402 Payment Required** yan Bitcoin address.

Wait ~60 seconds (simulated settlement), try again:

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Response: **200 Unlocked**.

Pat usa helper script:

```bash
python examples/paid-app-access/access_app.py hello-world
```

---

## Paso 4: Customize handler

Edit:

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

Patch via voice/API:

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"patch app hello-world to add greeting","acoustic_hash":"0"}'
```

---

## Paso 5: Build real service (template)

Copy starter project:

```bash
cp -r starter-projects/minimal-api my-api
cd my-api
python handler_service.py
```

Deploy gi UtahMosphere:

```bash
python ../examples/voice-deploy-simulator/deploy.py my-api
```

---

## Paso 6: Frontend integration

Usa [frontend-upload template](../../templates/frontend-upload/) pat fetch status gi app-mu:

```javascript
const res = await fetch("http://127.0.0.1:8999/status");
const data = await res.json();
console.log("Active tenants:", data.tenants);
```

---

## Paso 7: Generate HMAC signatures (future storage APIs)

```python
import hmac
import hashlib

SECRET = b"utah_akashic_sovereign_perimeter_authorization_vector"
tenant_id = "hello-world"
path = "/s3/assets/photo.jpg"
sig = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## Håfa un build

- Deployed app via `/command` API
- Navigated Tycoon HTTP 402 payment flow
- Customized `handler.py`
- Connected frontend to `/status` endpoint

---

## Sigiente Pasos

- [Cookbook Desarrollador](../DEVELOPER_COOKBOOK.md)
- [Referensia API](../API_REFERENCE.md)
- [minimal-api starter project](../../starter-projects/minimal-api/)
- [monetized-endpoint starter project](../../starter-projects/monetized-endpoint/)
