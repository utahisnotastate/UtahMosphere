# Opas: Ensimmäinen sovellus

**Kohderyhmä:** Frontend- ja backend-kehittäjät  
**Aika:** 30 minuuttia  
**Tavoite:** Ota sovellus käyttöön, käytä sitä ja laajenna sitä UtahMospheressa päästä päähän

---

## Esivaatimukset

- Python 3.11+
- `pip install -r requirements.txt`
- [Paikallisen kehityksen opas](../LOCAL_DEVELOPMENT.md) suoritettu (valinnainen)

---

## Vaihe 1: Käynnistä ydin

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

Varmista:

```bash
curl http://127.0.0.1:8999/health
```

---

## Vaihe 2: Ota `hello-world` käyttöön

```bash
python examples/voice-deploy-simulator/deploy.py hello-world
```

Odotettu vastaus sisältää portin `8200` (ensimmäinen vuokralainen).

Tarkista tila:

```bash
curl http://127.0.0.1:8999/status
```

---

## Vaihe 3: Käytä sovellustasi (maksuportti)

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Ensimmäinen vastaus: **402 Payment Required** Bitcoin-osoitteella.

Odota ~60 sekuntia (simuloitu selvitys), yritä uudelleen:

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Vastaus: **200 Unlocked**.

Tai käytä apuskriptiä:

```bash
python examples/paid-app-access/access_app.py hello-world
```

---

## Vaihe 4: Mukauta käsittelijää

Muokkaa:

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

Korjaa äänen/API:n kautta:

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"patch app hello-world to add greeting","acoustic_hash":"0"}'
```

---

## Vaihe 5: Rakenna oikea palvelu (malli)

Kopioi aloitusprojekti:

```bash
cp -r starter-projects/minimal-api my-api
cd my-api
python handler_service.py
```

Ota käyttöön UtahMospheressa:

```bash
python ../examples/voice-deploy-simulator/deploy.py my-api
```

---

## Vaihe 6: Frontend-integraatio

Käytä [frontend-upload-mallia](../../templates/frontend-upload/) tai hae tila sovelluksestasi:

```javascript
const res = await fetch("http://127.0.0.1:8999/status");
const data = await res.json();
console.log("Active tenants:", data.tenants);
```

---

## Vaihe 7: Luo HMAC-allekirjoituksia (tulevat tallennus-API:t)

```python
import hmac
import hashlib

SECRET = b"utah_akashic_sovereign_perimeter_authorization_vector"
tenant_id = "hello-world"
path = "/s3/assets/photo.jpg"
sig = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## Mitä rakensit

- Otit sovelluksen käyttöön `/command` API:n kautta
- Navigoit Tycoon HTTP 402 -maksuvirran läpi
- Mukautit `handler.py`:tä
- Yhdistit frontendin `/status`-päätepisteeseen

---

## Seuraavat vaiheet

- [Kehittäjän keittokirja](../DEVELOPER_COOKBOOK.md)
- [Frontend-reseptit](../recipes/README.md)
- [Backend-reseptit](../recipes/README.md)
- [API-viite](../API_REFERENCE.md)
