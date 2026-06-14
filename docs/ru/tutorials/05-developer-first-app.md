# Учебник: Ваше первое приложение

**Аудитория:** Фронтенд- и бэкенд-разработчики  
**Время:** 30 минут  
**Цель:** Развернуть, получить доступ и расширить приложение на UtahMosphere от начала до конца

---

## Предварительные требования

- Python 3.11+
- `pip install -r requirements.txt`
- [Руководство по локальной разработке](../LOCAL_DEVELOPMENT.md) пройдено (опционально)

---

## Шаг 1: Запуск ядра

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

Подтверждение:

```bash
curl http://127.0.0.1:8999/health
```

---

## Шаг 2: Развёртывание `hello-world`

```bash
python examples/voice-deploy-simulator/deploy.py hello-world
```

В ответе ожидается порт `8200` (первый арендатор).

Проверка статуса:

```bash
curl http://127.0.0.1:8999/status
```

---

## Шаг 3: Доступ к приложению (шлюз оплаты)

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Первый ответ: **402 Payment Required** с Bitcoin-адресом.

Подождите ~60 секунд (симулированное закрытие счёта), повторите:

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

Ответ: **200 Unlocked**.

Или используйте вспомогательный скрипт:

```bash
python examples/paid-app-access/access_app.py hello-world
```

---

## Шаг 4: Настройка обработчика

Отредактируйте:

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

Патч через голос/API:

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"patch app hello-world to add greeting","acoustic_hash":"0"}'
```

---

## Шаг 5: Реальный сервис (шаблон)

Скопируйте стартовый проект:

```bash
cp -r starter-projects/minimal-api my-api
cd my-api
python handler_service.py
```

Разверните на UtahMosphere:

```bash
python ../examples/voice-deploy-simulator/deploy.py my-api
```

---

## Шаг 6: Интеграция с фронтендом

Используйте [шаблон frontend-upload](../../templates/frontend-upload/) или запросите статус из приложения:

```javascript
const res = await fetch("http://127.0.0.1:8999/status");
const data = await res.json();
console.log("Active tenants:", data.tenants);
```

---

## Шаг 7: Генерация HMAC-подписей (будущие API хранилища)

```python
import hmac
import hashlib

SECRET = b"utah_akashic_sovereign_perimeter_authorization_vector"
tenant_id = "hello-world"
path = "/s3/assets/photo.jpg"
sig = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## Что вы построили

- Развернули приложение через API `/command`
- Прошли поток оплаты Tycoon HTTP 402
- Настроили `handler.py`
- Подключили фронтенд к `/status`

---

## Следующие шаги

- [Справочник разработчика](../DEVELOPER_COOKBOOK.md)
- [Индекс рецептов](../recipes/README.md)
- [Справочник API](../API_REFERENCE.md)
