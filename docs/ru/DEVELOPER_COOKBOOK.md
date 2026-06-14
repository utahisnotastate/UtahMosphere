### 🍳 Справочник разработчика: рецепты UtahMosphere

Справочник — точка входа для разработчиков. Полная библиотека рецептов: **[Индекс рецептов](recipes/README.md)**.

---

#### **Быстрые ссылки**

| Задача | Рецепт |
|--------|--------|
| Развёртывание через API | [Индекс рецептов → Развёртывание через /command](recipes/README.md) |
| Мониторинг здоровья | [Индекс рецептов → Проверка здоровья](recipes/README.md) |
| Поток оплаты (402) | [Индекс рецептов → Поток Tycoon](recipes/README.md) |
| HMAC-подписи | [Индекс рецептов → HMAC](recipes/README.md) |
| Голосовые интенты | [Индекс рецептов](recipes/README.md) |

**Учебник:** [Ваше первое приложение](tutorials/05-developer-first-app.md)  
**Шаблоны:** [templates/](../../templates/) · **Стартеры:** [starter-projects/](../../starter-projects/)

---

#### **Рецепт фронтенда: прямая загрузка изображений на периферию**

> **Статус:** В планах (API S3 Mesh ещё не маршрутизирован). Паттерн готов к миграции.

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

**Реализовано сегодня:** используйте `fetch('http://127.0.0.1:8999/status')` — см. [шаблон frontend-upload](../../templates/frontend-upload/).

---

#### **Рецепт бэкенда: развёртывание через /command**

> **Статус:** Реализовано

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

Или запустите: `python examples/voice-deploy-simulator/deploy.py my-app`

---

#### **Рецепт бэкенда: синхронизированное хранилище сессий**

> **Статус:** В планах (HTTP-маршруты реестра RDS)

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

#### **Рецепт Voice Bridge: пользовательские Vibe-команды**

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

Полный паттерн: [Индекс рецептов](recipes/README.md)

---

#### **Каркас: Python-сервис UtahMosphere**

Шаблон: [templates/python-http-service/](../../templates/python-http-service/)

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

#### **Замечание по безопасности: генерация подписей**

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

См. [Матрицу возможностей](CAPABILITY_MATRIX.md) для усиления безопасности в продакшене.
