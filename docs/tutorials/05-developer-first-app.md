# Tutorial: Your First App

**Audience:** Frontend and backend developers  
**Time:** 30 minutes  
**Goal:** Deploy, access, and extend an app on UtahMosphere end-to-end

---

## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`
- [Local Development Guide](../LOCAL_DEVELOPMENT.md) completed (optional)

---

## Step 1: Start the Kernel

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

Confirm:

```bash
curl http://127.0.0.1:8999/health
```

---

## Step 2: Deploy `hello-world`

```bash
python examples/voice-deploy-simulator/deploy.py hello-world
```

Expected response includes port `8200` (first tenant).

Check status:

```bash
curl http://127.0.0.1:8999/status
```

---

## Step 3: Access Your App (Payment Gate)

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

First response: **402 Payment Required** with Bitcoin address.

Wait ~60 seconds (simulated settlement), retry:

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Response: **200 Unlocked**.

Or use the helper script:

```bash
python examples/paid-app-access/access_app.py hello-world
```

---

## Step 4: Customize the Handler

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

## Step 5: Build a Real Service (Template)

Copy the starter project:

```bash
cp -r starter-projects/minimal-api my-api
cd my-api
python handler_service.py
```

Deploy to UtahMosphere:

```bash
python ../examples/voice-deploy-simulator/deploy.py my-api
```

---

## Step 6: Frontend Integration

Use the [frontend-upload template](../../templates/frontend-upload/) or fetch status from your app:

```javascript
const res = await fetch("http://127.0.0.1:8999/status");
const data = await res.json();
console.log("Active tenants:", data.tenants);
```

---

## Step 7: Generate HMAC Signatures (Future Storage APIs)

```python
import hmac
import hashlib

SECRET = b"utah_akashic_sovereign_perimeter_authorization_vector"
tenant_id = "hello-world"
path = "/s3/assets/photo.jpg"
sig = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## What You Built

- Deployed app via `/command` API
- Navigated Tycoon HTTP 402 payment flow
- Customized `handler.py`
- Connected frontend to `/status`

---

## Next Steps

- [Developer Cookbook](../DEVELOPER_COOKBOOK.md)
- [Frontend Recipes](../recipes/frontend-recipes.md)
- [Backend Recipes](../recipes/backend-recipes.md)
- [API Reference](../API_REFERENCE.md)
