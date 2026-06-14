# Tutorial: Tu primera aplicación

**Audiencia:** Desarrolladores frontend y backend  
**Tiempo:** 30 minutos  
**Objetivo:** Desplegar, acceder y extender una aplicación en UtahMosphere de punta a punta

---

## Requisitos previos

- Python 3.11+
- `pip install -r requirements.txt`
- [Guía de desarrollo local](../LOCAL_DEVELOPMENT.md) completada (opcional)

---

## Paso 1: Inicia el kernel

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

Confirma:

```bash
curl http://127.0.0.1:8999/health
```

---

## Paso 2: Despliega `hello-world`

```bash
python examples/voice-deploy-simulator/deploy.py hello-world
```

La respuesta esperada incluye el puerto `8200` (primer inquilino).

Verifica el estado:

```bash
curl http://127.0.0.1:8999/status
```

---

## Paso 3: Accede a tu aplicación (puerta de pago)

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Primera respuesta: **402 Payment Required** con dirección Bitcoin.

Espera ~60 segundos (liquidación simulada), reintenta:

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Respuesta: **200 Unlocked**.

O usa el script auxiliar:

```bash
python examples/paid-app-access/access_app.py hello-world
```

---

## Paso 4: Personaliza el handler

Edita:

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

Parchea vía voz/API:

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"patch app hello-world to add greeting","acoustic_hash":"0"}'
```

---

## Paso 5: Construye un servicio real (plantilla)

Copia el proyecto de arranque:

```bash
cp -r starter-projects/minimal-api my-api
cd my-api
python handler_service.py
```

Despliega en UtahMosphere:

```bash
python ../examples/voice-deploy-simulator/deploy.py my-api
```

---

## Paso 6: Integración frontend

Usa la plantilla [frontend-upload](../../templates/frontend-upload/) o consulta el estado desde tu app:

```javascript
const res = await fetch("http://127.0.0.1:8999/status");
const data = await res.json();
console.log("Active tenants:", data.tenants);
```

---

## Paso 7: Genera firmas HMAC (APIs de almacenamiento futuras)

```python
import hmac
import hashlib

SECRET = b"utah_akashic_sovereign_perimeter_authorization_vector"
tenant_id = "hello-world"
path = "/s3/assets/photo.jpg"
sig = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## Lo que construiste

- Aplicación desplegada vía API `/command`
- Flujo de pago HTTP 402 Tycoon navegado
- `handler.py` personalizado
- Frontend conectado a `/status`

---

## Próximos pasos

- [Recetario del desarrollador](../DEVELOPER_COOKBOOK.md)
- [Índice de recetas](../recipes/README.md)
- [Referencia de API](../API_REFERENCE.md)
