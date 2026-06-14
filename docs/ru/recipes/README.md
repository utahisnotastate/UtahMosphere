# Индекс рецептов

Готовые рецепты для копирования, организованные по ролям. В каждом рецепте указано, работает ли он на **v25.0** сегодня или это **паттерн из дорожной карты**.

---

## По ролям

| Роль | Документ с рецептами |
|------|----------------------|
| Дети и семьи | См. [Учебник: Ваш первый робот-дворецкий](../tutorials/01-kids-first-robot-butler.md) |
| Руководители | См. [Резюме для руководства](../EXECUTIVE_SUMMARY.md) |
| Архитекторы | См. [Техническое погружение](../TECHNICAL_DEEP_DIVE.md) |
| Разработчики фронтенда | См. [Справочник разработчика](../DEVELOPER_COOKBOOK.md) |
| Разработчики бэкенда | См. [Справочник разработчика](../DEVELOPER_COOKBOOK.md) |
| Голос / UX | См. [Справочник разработчика](../DEVELOPER_COOKBOOK.md) |
| Операции | См. [Руководство по локальной разработке](../LOCAL_DEVELOPMENT.md) |

---

## Краткий справочник (реализовано сегодня)

| Задача | Где найти |
|------|-----------|
| Развёртывание приложения через API | [Справочник разработчика → /command](../DEVELOPER_COOKBOOK.md) |
| Проверка здоровья | [Руководство по локальной разработке](../LOCAL_DEVELOPMENT.md) |
| HMAC-подпись | [Справочник разработчика → подписи](../DEVELOPER_COOKBOOK.md) |
| Поток оплаты HTTP 402 | [Справочник разработчика → Tycoon](../DEVELOPER_COOKBOOK.md) · [Учебник: первое приложение](../tutorials/05-developer-first-app.md) |
| Голосовое развёртывание | [Учебник: робот-дворецкий](../tutorials/01-kids-first-robot-butler.md) |
| Биометрический claim узла | [Справочник API → POST /command](../API_REFERENCE.md) |

---

## Реализованные паттерны v25.0

### Развёртывание через /command

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

### Мониторинг здоровья

```bash
curl http://127.0.0.1:8999/health
curl http://127.0.0.1:8999/status
```

Или: `python examples/check-node-health/health_check.py`

### Поток Tycoon HTTP 402

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

Первый ответ — `402` со счётом; после ~60 с повторите запрос для `200`.

Или: `python examples/paid-app-access/access_app.py hello`

### HMAC-подпись арендатора

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## Паттерны из дорожной карты

Следующие рецепты описаны в [Справочнике разработчика](../DEVELOPER_COOKBOOK.md), но HTTP-маршруты ещё не подключены в v25.0:

- Загрузка в S3 Mesh (`POST /s3/*`)
- Хранилище сессий RDS (`/rds/read`, `/rds/write`)
- Вызов Lambda (`POST /lambda/*/invoke`)

Статус реализации: [Матрица возможностей](../CAPABILITY_MATRIX.md)

---

## Шаблоны и стартеры

Полноценные проекты — начните здесь:

- [templates/](../../templates/) — файлы каркаса
- [examples/](../../examples/) — небольшие запускаемые скрипты
- [starter-projects/](../../starter-projects/) — мини-приложения для форка
