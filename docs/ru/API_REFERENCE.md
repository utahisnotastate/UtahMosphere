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
  "version": "32.0",
  "build": "omega-build-v32-lazarus-self-healing",
  "attestation": {
    "tpm_present": false,
    "provisioned": false,
    "sealed": false,
    "enforce": true,
    "tpm_lock": {"sealed": false, "binding_ok": true, "enforce": true},
    "ra_tls": {"enforce": true, "kernel_root_ca": "utahmosphere_omega_build_v32_root_ca", "dht_federation": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true}},
    "quote_registry": {"active": 1, "purged": 0, "total": 1},
    "dht_federation": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true},
    "quorum": {"quorum_reached": 1, "pending": 0, "quarantined": 0, "total": 1, "threshold": 0.51, "enforce": true},
    "pcr_drift": {"enforce": true, "rollback_enforce": true, "golden_set": true, "drift_detected": false, "interval_sec": 10}
  }
}
```

**Пример:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /attestation/quote

Выдаёт RA-TLS TPM quote для проверки mesh-узлов UtahNetes.

**Ответ `200`:**

```json
{
  "hardware_id": "sha256-hardware-fingerprint",
  "ra_tls_quote": {
    "body": "{\"build\":\"omega-build-v32-lazarus-self-healing\",\"node_id\":\"my-host\",\"hardware_id\":\"...\",\"pcr0_digest\":\"...\",\"vibe_hash\":\"...\"}",
    "signature": "hmac-sha256-hex",
    "ca_signature": "optional-rsa-hex"
  }
}
```



---

## GET /registry/quotes

Export global hardware quote registry.

**Response `200`:**

```json
{
  "nodes": {
    "abc123...": {
      "public_quote": "{\"body\":\"...\",\"signature\":\"...\"}",
      "vibe_hash": "64-char-sha256",
      "pcr_digest": "...",
      "node_id": "my-host",
      "status": "active",
      "registered_at": 1718323200.0
    }
  },
  "stats": {"active": 1, "purged": 0, "total": 1}
}
```

```bash
curl http://127.0.0.1:8999/registry/quotes
```

---

## POST /registry/purge

Purge compromised hardware ID. Root vibe holder only.

**Request body:**

```json
{
  "hardware_id": "sha256-hardware-fingerprint",
  "acoustic_hash": "root-vibe-hash-64chars",
  "reason": "firmware tamper"
}
```

**Response `200`:**

```json
{"status": "purged", "hardware_id": "abc123..."}
```




---



---



---

## GET /witness/status

Multi-region quorum witness status.

```bash
curl http://127.0.0.1:8999/witness/status
```

---

## GET /lazarus/status

Lazarus auto-restore checkpoint status.

---

## POST /lazarus/restore

Trigger Golden Master restoration.

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```


## GET /quorum/consensus

Export majority-quorum vote ledger.

**Response `200`:**

```json
{
  "consensus": {
    "my-host": {
      "golden_quote": "sha256-fingerprint",
      "votes": {"voter-node": "sha256-fingerprint"},
      "quorum_ratio": 1.0,
      "vote_count": 1,
      "status": "quorum_reached"
    }
  },
  "stats": {"quorum_reached": 1, "pending": 0, "quarantined": 0, "total": 1, "threshold": 0.51, "enforce": true}
}
```

```bash
curl http://127.0.0.1:8999/quorum/consensus
```


## GET /dht/consensus

Export DHT golden measurement ledger.

**Response `200`:**

```json
{
  "golden": {
    "my-host": {
      "golden_quote": "sha256-fingerprint",
      "pcr_digest": "...",
      "hardware_id": "...",
      "status": "consensus",
      "recorded_at": 1718323200.0
    }
  },
  "stats": {"consensus": 1, "quarantined": 0, "total": 1, "enforce": true}
}
```

```bash
curl http://127.0.0.1:8999/dht/consensus
```

---

## POST /dht/challenge

Issue attestation challenge to swarm peer.

**Request body:**

```json
{"peer_hash": "64-char-node-hash"}
```

**Response `202`:**

```json
{"status": "challenge_sent", "peer_hash": "abc123..."}
```


---

## GET /nonce

Выдаёт свежий nonce для голосовой команды. Требуется после закрепления узла при `UTAH_NONCE_ENFORCE=1` (по умолчанию).

**Ответ `200`:**

```json
{
  "nonce": 1718323200,
  "window_sec": 30,
  "signature_hint": "HMAC-SHA256(acoustic_hash, f'{nonce}:{transcript}')"
}
```

**Пример:**

```bash
curl http://127.0.0.1:8999/nonce
```

---

## GET /status

Операционный снимок: состояние UI, развёрнутые арендаторы и статус закрепления узла.

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
    "mempool_failover_nodes": [
      {"region": "us-global", "url": "https://mempool.space/api"},
      {"region": "eu-signet", "url": "https://mempool.space/signet/api"},
      {"region": "global-blockstream", "url": "https://blockstream.info/api"},
      {"region": "oceania-apac", "url": "https://mempool.space/testnet/api"}
    ]
  },
  "attestation": {
    "tpm_present": false,
    "provisioned": false,
    "sealed": false,
    "enforce": true
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
| `nonce` | integer | После claim | Метка времени от сервера из `GET /nonce` |
| `command_signature` | string | После claim | `HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")` — alias: `signature` |
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

**Voice Bridge v27.0** автоматически вызывает `GET /nonce` и подписывает. Ручное подписание:

```python
from voice_bridge_signed import get_signed_payload
payload = get_signed_payload("deploy application hello", acoustic_hash)
```

**После claim:** `acoustic_hash` должен совпадать с корневым или `authorized_nodes[]`, а `nonce` + `command_signature` должны быть действительными, иначе ядро вернёт:

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
| `X-Utah-Hardware-ID` | RA-TLS hardware fingerprint (ingress attestation) |
| `X-Utah-RATLS-Quote` | JSON RA-TLS quote payload |

When `UTAH_RA_TLS_GUARD_ENFORCE=1`, missing or invalid attestation headers return **403** before proxy.

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

UtahX проксирует запрос в backend UtahContainerEngine на порту арендатора. Тело ответа — JSON-вывод обработчика.

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## PUT/POST /s3/{bucket}/{key}

Запись объекта в Utah S3 Mesh (локальное NVMe-хранилище).

**Заголовки (опционально):**

| Заголовок | Описание |
|-----------|----------|
| `X-Utah-Tenant-ID` | Идентификатор арендатора |
| `X-Utah-Signature` | HMAC-SHA256 `{tenant_id}:{path}` |

**Пример:**

```bash
curl -X PUT http://127.0.0.1:8999/s3/my-data/file.txt \
  -H "Content-Type: text/plain" \
  --data-binary "Hello Utah"
```

---

## GET /s3/{bucket}/{key}

Чтение объекта. Возвращает сырые байты. Используйте `GET /s3/{bucket}/prefix*` для списка.

```bash
curl http://127.0.0.1:8999/s3/my-data/file.txt
```

---

## POST /rds/write

Запись ключ-значение в Utah RDS Ledger.

**Тело запроса:**

```json
{"key": "user:123", "value": {"name": "Alice", "score": 9000}}
```

**Ответ `200`:**

```json
{"key": "user:123", "status": "written", "epoch": 1718280000.0}
```

---

## GET /rds/read/{key}

Чтение записи по ключу.

```bash
curl http://127.0.0.1:8999/rds/read/user:123
```

---

## POST /lambda/{function_name}/invoke

Вызов обработчика Utah Lambda (без загрузки образа контейнера).

**Тело запроса:** JSON-событие, передаваемое в `handler(event, context)`

```bash
curl -X POST http://127.0.0.1:8999/lambda/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "General 23"}'
```

**Ответ `200`:**

```json
{"result": {"message": "Hello General 23 from Utah Lambda!"}}
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

## POST /admin/revoke-node

Отзыв делегированного узла из `authorized_nodes[]`. Только владелец корневого vibe. Панель отзыва Utah-Flux вызывает эту конечную точку.

**Тело запроса:**

```json
{
  "node_hash": "abc123...64chars",
  "acoustic_hash": "root-vibe-hash-64chars"
}
```

**Ответ `200`:**

```json
{"status": "revoked", "node_hash": "abc123..."}
```

---

## Ответы с ошибками

| Код | Когда |
|-----|-------|
| `404` | Неизвестный путь или узел нельзя отозвать |
| `402` | Приложение существует, но клиент не оплатил счёт Tycoon |
| `403` | Недействительные учётные данные отзыва или HMAC |

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
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Обработчик контейнера |
| `{UTAH_DATA_DIR}/lambda/{fn}/handler.py` | Обработчик Lambda |
| `{UTAH_DATA_DIR}/s3/{bucket}/{key}` | Объекты S3 Mesh |
| `{UTAH_DATA_DIR}/rds/ledger.json` | Хранилище ключ-значение RDS |
| `security/biometric_ledger.json` | Корневой vibe-хеш (локальный fallback, если `/etc` недоступен для записи) |
| `tycoon/settlement_ledger.json` |
| `{UTAH_DATA_DIR}/quote_registry.json` | Global hardware quote registry |
| `{UTAH_DATA_DIR}/dht_golden_registry.json` | DHT golden ledger |
| `{UTAH_DATA_DIR}/golden_pcr0.txt` | Golden PCR0 |
| `{UTAH_DATA_DIR}/dht_quorum_registry.json` | Quorum ledger |
| `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Lazarus checkpoint |
| `{UTAH_DATA_DIR}/quorum_witness.json` | Witness registry |
| `{UTAH_DATA_DIR}/dht_quorum_registry.json` | Quorum vote ledger |
| `{UTAH_DATA_DIR}/golden_pcr0.txt` | Golden PCR0 |
| `{UTAH_DATA_DIR}/quote_registry.json` | Global hardware quote registry | | Состояние счетов и платежей |

По умолчанию `UTAH_DATA_DIR`: `/var/lib/utahmosphere` (при ошибках прав — локальные каталоги).
