# Õpetus: Sinu esimene rakendus

**Sihtgrupp:** Frontend ja backend arendajad  
**Aeg:** 30 minutit  
**Eesmärk:** Juuruta, pääse ligi ja laienda rakendust UtahMosphere'il otsast lõpuni

---

## Eeltingimused

- Python 3.11+
- `pip install -r requirements.txt`
- [Kohaliku arenduse juhend](../LOCAL_DEVELOPMENT.md) läbitud (valikuline)

---

## Samm 1: Käivita tuum

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

Kinnita:

```bash
curl http://127.0.0.1:8999/health
```

---

## Samm 2: Juuruta `hello-world`

```bash
python examples/voice-deploy-simulator/deploy.py hello-world
```

Oodatav vastus sisaldab porti `8200` (esimene rentnik).

Kontrolli olekut:

```bash
curl http://127.0.0.1:8999/status
```

---

## Samm 3: Pääse ligi rakendusele (maksevärav)

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Esimene vastus: **402 Payment Required** Bitcoin aadressiga.

Oota ~60 sekundit (simuleeritud arveldus), proovi uuesti:

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Vastus: **200 Unlocked**.

Või kasuta abiskripti:

```bash
python examples/paid-app-access/access_app.py hello-world
```

---

## Samm 4: Kohanda handlerit

Muuda:

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

Paika hääle/API kaudu:

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"patch app hello-world to add greeting","acoustic_hash":"0"}'
```

---

## Samm 5: Ehita päris teenus (mall)

Kopeeri algprojekt:

```bash
cp -r starter-projects/minimal-api my-api
cd my-api
python handler_service.py
```

Juuruta UtahMosphere'ile:

```bash
python ../examples/voice-deploy-simulator/deploy.py my-api
```

---

## Samm 6: Frontend integratsioon

Kasuta [frontend-upload malli](../../../templates/frontend-upload/) või hangi olek rakendusest:

```javascript
const res = await fetch("http://127.0.0.1:8999/status");
const data = await res.json();
console.log("Active tenants:", data.tenants);
```

---

## Samm 7: Genereeri HMAC allkirjad (tulevased salvestus-API-d)

```python
import hmac
import hashlib

SECRET = b"utah_akashic_sovereign_perimeter_authorization_vector"
tenant_id = "hello-world"
path = "/s3/assets/photo.jpg"
sig = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## Mida sa ehitasid

- Juurutasid rakenduse `/command` API kaudu
- Navigeerisid Tycoon HTTP 402 maksevoos
- Kohandasid `handler.py`
- Ühendasid frontendi `/status`-iga

---

## Järgmised sammud

- [Arendaja retseptiraamat](../DEVELOPER_COOKBOOK.md)
- [Frontend retseptid](../recipes/README.md)
- [Backend retseptid](../recipes/README.md)
- [API viide](../API_REFERENCE.md)
