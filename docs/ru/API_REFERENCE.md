# Справочник API

Базовый URL (по умолчанию): `http://127.0.0.1:8999`

Все ответы — JSON, если не указано иное.

---

## GET /health

Проверка живости для балансировщиков нагрузки и мониторинга.

**Ответ `200`:**

```json
{
  "status": "healthy",
  "node": "my-hostname",
  "version": "25.1",
  "build": "golden-master-v25.1"
}
```

**Пример:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /status

Операционный снимок: состояние UI, развёрнутые арендаторы, статус claim, `authorized_nodes`, `swarm_peers` и расширенные поля Tycoon.

**Ответ `200`:**

```json
{
  "ui_state": {
    "node_status": "Active [Sovereign Core v25.0]",
    "active_workloads": 1,
    "last_voice_command": "deploy application my-app",
    "cluster_health": "Resilient",
    "mutation_count": 0
  },
  "tenants": ["my-app"],
  "claimed": true,
  "authorized_nodes": ["abc123..."],
  "swarm_peers": 2,
  "tycoon": {
    "pending": 0,
    "settled_invoices": 1,
    "swept_funds": 5000,
    "settlement_mode": "auto",
    "mempool_api": "https://mempool.space/api"
  }
}
```

---

## POST /command

Выполнение голосового интента программно. Тот же payload, что отправляет Voice Bridge.

**Тело запроса:**

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| `transcript` | string | Да | Произнесённая команда (без учёта регистра) |
| `acoustic_hash` | string | Да | 64-символьный SHA-256 хеш vibe-print |
| `request_signature` | string | Нет | Опциональный HMAC AuthGuard для делегированных узлов |

**Ответ `200`:**

```json
{
  "status": "manifested",
  "response": "Application successfully anchored into UtahContainerEngine loop on workspace port 8200."
}
```

### Поддерживаемые транскрипты

| Интент | Пример транскрипта |
|--------|-------------------|
| Закрепление узла | `"Claim node"` |
| Authorize node | `"authorize node <64-char-vibe-hash>"` |
| Развёртывание приложения | `"deploy application hello"` или `"manifest app hello"` |
| Патч приложения | `"patch app hello to add feature x"` |
| Статус | `"status grid"` |

**Закрепление узла (первый запуск):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Claim node", "acoustic_hash": "abc123..."}'
```

**Развёртывание приложения (открытый режим — до claim, любой хеш принимается):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "deploy application hello", "acoustic_hash": "0000000000000000000000000000000000000000000000000000000000000000"}'
```

**После claim:** `acoustic_hash` должен совпадать с закреплённым корневым vibe-хешем **или** быть записью в `authorized_nodes[]`, иначе ядро вернёт:

```json
{
  "status": "manifested",
  "response": "Access Denied. Biological signature does not match the Akashic Record."
}
```

---

## GET /app/{app_name}

Доступ к развёрнутому приложению арендатора. Контролируется авторизацией оплаты Utah-Tycoon.

**Заголовки:**

| Заголовок | Описание |
|-----------|----------|
| `X-Client-ID` | Опциональный идентификатор клиента (по умолчанию — IP клиента) |

### Неоплативший клиент — ответ `402 Payment Required`

```json
{
  "error": "Payment Required for UtahContainer Execution",
  "payment_address": "bc1q_utah_ephemeral_a1b2c3d4e5f6",
  "amount_sats": 5000,
  "message": "Transmit value to unlock silicon processing path."
}
```

Счета автоматически закрываются примерно через 60 секунд в текущей симуляции.

### Оплативший клиент — ответ `200`

```json
{
  "status": "Unlocked",
  "message": "Container hello executing."
}
```

**Пример:**

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## POST /app/unlock

Отправьте запрос на разблокировку оплаты. Tycoon опрашивает mempool.space (или electrum-server) для финальности платежа. Dev-адреса (`bc1q_utah_*`) используют отложенное закрытие в режиме `auto`.

**Тело запроса:**

```json
{
  "app_name": "hello",
  "client_id": "demo-client",
  "payment_tx": "optional-tx-hint",
  "amount_sats": 5000
}
```

**Ответ `202`:**

```json
{
  "status": "pending",
  "message": "Payment required. Awaiting ledger consensus.",
  "tx_id": "tx_abc123",
  "payment_address": "bc1q_utah_ephemeral_...",
  "amount_sats": 5000
}
```

После закрытия `GET /app/{app_name}` с тем же `X-Client-ID` проксирует в контейнер.

---

## Ответы с ошибками

| Код | Когда |
|-----|-------|
| `404` | Неизвестный путь |
| `402` | Приложение существует, но клиент не оплатил счёт Tycoon |

---

## Порты и мультикаст

| Сервис | Порт / адрес |
|--------|--------------|
| HTTP-вход | `8999` |
| UtahNetes gossip | UDP `9001`, мультикаст `239.255.43.21` |
| Global Swarm | UDP `9055` |

---

## Файлы данных

| Файл | Назначение |
|------|------------|
| `{UTAH_DATA_DIR}/secure_registry.json` | Арендаторы, маршруты UtahX, индекс хранилища |
| `{UTAH_DATA_DIR}/flux_ui_manifest.json` | Состояние UI Utah-Flux |
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Заглушка развёрнутого обработчика |
| `security/biometric_ledger.json` | Корневой vibe-хеш (локальный fallback, если `/etc` недоступен для записи) |
| `tycoon/settlement_ledger.json` | Состояние счетов и платежей |

По умолчанию `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (при ошибках прав — локальные каталоги).
