### 🍳 Recetario del desarrollador: Recetas UtahMosphere

El recetario es el punto de entrada para desarrolladores. Para la biblioteca completa de recetas, consulta el **[Índice de recetas](recipes/README.md)**.

---

#### **Enlaces rápidos**

| Tarea | Receta |
|-------|--------|
| Desplegar vía API | [Índice de recetas](recipes/README.md) |
| Monitoreo de salud | [Índice de recetas](recipes/README.md) |
| Flujo de pago (402) | [Índice de recetas](recipes/README.md) |
| Firmas HMAC | [Índice de recetas](recipes/README.md) |
| Intenciones de voz | [Índice de recetas](recipes/README.md) |

**Tutorial:** [Tu primera aplicación](tutorials/05-developer-first-app.md)  
**Plantillas:** [templates/](../../templates/) · **Proyectos de arranque:** [starter-projects/](../../starter-projects/)

---

#### **Receta frontend: Carga de imagen directa al edge**

> **Estado:** Hoja de ruta (API S3 Mesh aún no enrutada). Patrón listo para migración.

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

**Implementado hoy:** usa `fetch('http://127.0.0.1:8999/status')` — consulta la plantilla [frontend-upload](../../templates/frontend-upload/).

---

#### **Receta backend: Desplegar vía /command**

> **Estado:** Implementado

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

O ejecuta: `python examples/voice-deploy-simulator/deploy.py my-app`

---

#### **Receta backend: Almacén de sesiones sincronizado**

> **Estado:** Hoja de ruta (rutas HTTP del ledger RDS)

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

#### **Receta Voice Bridge: Vibe-coding personalizado**

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

Patrón completo: [Índice de recetas](recipes/README.md)

---

#### **Plantilla base: Servicio Python UtahMosphere**

Plantilla: [templates/python-http-service/](../../templates/python-http-service/)

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

#### **Nota de seguridad: Generación de firmas**

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

Consulta la [Referencia de API](API_REFERENCE.md) para endurecimiento en producción.
