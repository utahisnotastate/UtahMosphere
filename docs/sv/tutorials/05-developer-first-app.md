# Guide: Din första app

**Målgrupp:** Frontend- och backend-utvecklare  
**Tid:** 30 minuter  
**Mål:** Driftsätt, använd och utöka en app på UtahMosphere från början till slut

---

## Förutsättningar

- Python 3.11+
- `pip install -r requirements.txt`
- [Guide för lokal utveckling](../LOCAL_DEVELOPMENT.md) genomförd (valfritt)

---

## Steg 1: Starta kärnan

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

Bekräfta:

```bash
curl http://127.0.0.1:8999/health
```

---

## Steg 2: Driftsätt `hello-world`

```bash
python examples/voice-deploy-simulator/deploy.py hello-world
```

Förväntat svar inkluderar port `8200` (första tenant).

Kontrollera status:

```bash
curl http://127.0.0.1:8999/status
```

---

## Steg 3: Använd din app (betalningsport)

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Första svar: **402 Payment Required** med Bitcoin-adress.

Vänta ~60 sekunder (simulerad avveckling), försök igen:

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Svar: **200 Unlocked**.

Eller använd hjälpskriptet:

```bash
python examples/paid-app-access/access_app.py hello-world
```

---

## Steg 4: Anpassa handlern

Redigera:

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

Patcha via röst/API:

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"patch app hello-world to add greeting","acoustic_hash":"0"}'
```

---

## Steg 5: Bygg en riktig tjänst (mall)

Kopiera startprojektet:

```bash
cp -r starter-projects/minimal-api my-api
cd my-api
python handler_service.py
```

Driftsätt till UtahMosphere:

```bash
python ../examples/voice-deploy-simulator/deploy.py my-api
```

---

## Steg 6: Frontend-integration

Använd [frontend-upload-mallen](../../templates/frontend-upload/) eller hämta status från din app:

```javascript
const res = await fetch("http://127.0.0.1:8999/status");
const data = await res.json();
console.log("Active tenants:", data.tenants);
```

---

## Steg 7: Generera HMAC-signaturer (framtida lagrings-API:er)

```python
import hmac
import hashlib

SECRET = b"utah_akashic_sovereign_perimeter_authorization_vector"
tenant_id = "hello-world"
path = "/s3/assets/photo.jpg"
sig = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## Vad du byggde

- Driftsatte app via `/command` API
- Navigerade Tycoon HTTP 402-betalningsflöde
- Anpassade `handler.py`
- Anslöt frontend till `/status`

---

## Nästa steg

- [Utvecklarkokbok](../DEVELOPER_COOKBOOK.md)
- [Frontend-recept](../recipes/README.md)
- [Backend-recept](../recipes/README.md)
- [API-referens](../API_REFERENCE.md)
