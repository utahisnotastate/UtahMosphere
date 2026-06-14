# Матрица возможностей

UtahMosphere OS **v27.0 Production Immutable** — суверенные якоря доверия полностью реализованы.

---

## HTTP API — конечные точки

| Конечная точка | Метод | Статус | Примечания |
|----------------|-------|--------|------------|
| `/health` | GET | **Реализовано** | Проверка живости + `build: omega-build-v27-production` + `attestation` |
| `/nonce` | GET | **Реализовано** | Выдача свежего nonce для голосовой команды (окно 30 с) |
| `/status` | GET | **Реализовано** | Состояние UI, арендаторы, аттестация, статистика failover mempool |
| `/command` | POST | **Реализовано** | Голосовой интент + автоподписание nonce (`voice_bridge_signed.py`) |
| `/admin/revoke-node` | POST | **Реализовано** | Только root — отзыв делегированного узла |
| `/app/unlock` | POST | **Реализовано** | Отправка оплаты; расчёт через failover mempool |
| `/app/{name}` | GET | **Реализовано** | Шлюз Tycoon 402 + прокси UtahX в контейнер |
| `/app/{name}/{path}` | GET | **Реализовано** | Прокси подпути в backend контейнера |
| `/s3/{bucket}/{key}` | GET | **Реализовано** | Чтение объекта (локальный NVMe) |
| `/s3/{bucket}/{key}` | PUT/POST | **Реализовано** | Запись объекта; опциональные заголовки HMAC |
| `/s3/{bucket}/{prefix}*` | GET | **Реализовано** | Список объектов |
| `/lambda/{fn}/invoke` | POST | **Реализовано** | Вызов serverless-обработчика |
| `/lambda/{fn}` | GET | **Реализовано** | GET-вызов с пустым событием |
| `/rds/write` | POST | **Реализовано** | Запись ключ-значение |
| `/rds/read/{key}` | GET | **Реализовано** | Чтение ключ-значение |

---

## Основные подсистемы

| Компонент | Статус | Что работает сегодня |
|-----------|--------|----------------------|
| **Golden Master (`utahmosphere_master.py`)** | **Реализовано** | Единая точка входа |
| **Ядро (`utahmosphere_os.py`)** | **Реализовано** | Полный HTTP-мультиплексор, реестр, сеть |
| **Аттестация оборудования (`attestation_guard.py`)** | **Реализовано** | Шлюз TPM 2.0 PCR0 в bootstrap + health |
| **Failover mempool (`tycoon_failover.py`)** | **Реализовано** | Бесшумный failover mempool US/EU/ASIA |
| **Voice Bridge Signed (`voice_bridge_signed.py`)** | **Реализовано** | Авто `GET /nonce` + HMAC-подписание |
| **Прокси UtahX (`utahx_proxy.py`)** | **Реализовано** | Живой HTTP-прокси на порты контейнеров |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Реализовано** | HTTP-серверы арендаторов на портах 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Реализовано** | AST-валидированная мутация обработчика + OTA |
| **S3 / Lambda / RDS** | **Реализовано** | Полная облачная паритетность |
| **Quantum Ledger** | **Реализовано** | Биометрический claim + проверка |
| **Utah-Tycoon** | **Реализовано** | Failover mempool + electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Реализовано** | Применение `authorized_nodes[]` |
| **Nonce-Guard (`nonce_guard.py`)** | **Реализовано** | Защита от повторного воспроизведения голосовых команд (30 с) |
| **UtahNetes + Swarm DHT** | **Реализовано** | Подписанный gossip + детерминированная маршрутизация |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Реализовано** | Alpine vmlinuz + TPM-aware bootstrap |
| **UI отзыва Utah-Flux** | **Реализовано** | Панель администратора в `flux_gui.py` |
| **Auto-Genesis / Bootstrap** | **Реализовано** | systemd + шлюз аттестации |

---

## Голосовые команды

| Шаблон команды | Статус | Пример |
|----------------|--------|--------|
| Claim node | Реализовано | `"Claim node"` |
| Authorize node | Реализовано | `"authorize node <64-char-vibe-hash>"` |
| Развёртывание приложения | Реализовано | `"deploy application my-app"` |
| Патч приложения | Реализовано | `"patch app my-app to add logging"` |
| Статус / сетка | Реализовано | `"status grid"` |

**Voice Bridge v27.0** автоматически вызывает `GET /nonce` и подписывает каждую команду. Ручные клиенты используют `voice_bridge_signed.get_signed_payload()`.

---

## Варианты развёртывания

| Метод | Статус | Платформа |
|-------|--------|-----------|
| `python3 utahmosphere_master.py` | **Рекомендуется** | Все |
| `sudo bash bootstrap.sh` | **Рекомендуется для prod** | Linux + TPM (опциональный пропуск) |
| `python3 genesis_iso_builder.py` | **Реализовано** | Собирает `utah_genesis_v27.iso` |
| `./mk_iso.sh` | **Реализовано** | Обёртка для сборщика Genesis ISO |
| `python3 voice_bridge.py` | **Реализовано** | Голосовой клиент с автоподписанием nonce |

---

## Дорожная карта

Все пункты дорожной карты v26.0 и более ранних версий **реализованы** в v27.0.

Будущие улучшения:

- Удалённая проверка TPM quote attestation (RA-TLS)
- Четвёртый регион mempool (Океания)
- Привязка vibe-print к TPM PCR на уровне оборудования

См. [Справочник API](API_REFERENCE.md) и [Справочник разработчика](DEVELOPER_COOKBOOK.md).
