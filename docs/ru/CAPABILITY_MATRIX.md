# Матрица возможностей

UtahMosphere OS **v26.0 Omega-Build FINAL** — полная реализация дорожной карты.

---

## HTTP API — конечные точки

| Конечная точка | Метод | Статус | Примечания |
|----------------|-------|--------|------------|
| `/health` | GET | **Реализовано** | Проверка живости + `build: omega-build-v26-final` |
| `/nonce` | GET | **Реализовано** | Выдача свежего nonce для голосовой команды (окно 30 с) |
| `/status` | GET | **Реализовано** | Состояние UI, арендаторы, статус claim, корень S3 |
| `/command` | POST | **Реализовано** | Голосовой интент + защита от повторного воспроизведения nonce после claim |
| `/admin/revoke-node` | POST | **Реализовано** | Только root — отзыв делегированного узла |
| `/app/unlock` | POST | **Реализовано** | Отправка оплаты; возвращает 202 до закрытия |
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
| **Прокси UtahX (`utahx_proxy.py`)** | **Реализовано** | Живой HTTP-прокси на порты контейнеров |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Реализовано** | HTTP-серверы арендаторов на портах 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Реализовано** | AST-валидированная мутация обработчика + OTA-канал |
| **S3 Mesh (`utah_s3_mesh.py`)** | **Реализовано** | Локальное объектное хранилище + HMAC |
| **Lambda Engine (`utah_lambda_engine.py`)** | **Реализовано** | Вызов обработчика без образов |
| **RDS Ledger (`utah_rds_ledger.py`)** | **Реализовано** | JSON-реестр ключ-значение |
| **Quantum Ledger** | **Реализовано** | Биометрический claim + проверка |
| **Utah-Tycoon** | **Реализовано** | Расчёт через mempool/electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Реализовано** | Применение `authorized_nodes[]` для голоса и сети |
| **Nonce-Guard (`nonce_guard.py`)** | **Реализовано** | Защита от повторного воспроизведения голосовых команд (30 с) |
| **Gossip UtahNetes** | **Реализовано** | Мультикаст 5 с с подписью AuthGuard через `utah_mesh_engine.py` |
| **Global Swarm** | **Реализовано** | Детерминированный DHT + подписанная синхронизация реестра |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Реализовано** | Гибридный ISO Alpine vmlinuz/initramfs |
| **UI отзыва Utah-Flux (`ui_revocation.py`)** | **Реализовано** | Панель администратора в `flux_gui.py` |
| **UI Utah-Flux** | **Реализовано** | Панель состояния Tkinter + отзыв узлов |
| **Auto-Genesis (`genesis_deploy.py`)** | **Реализовано** | Многопроцессный оркестратор |
| **Bootstrap (`bootstrap.sh`)** | **Реализовано** | Установка bare-metal systemd |

---

## Голосовые команды

| Шаблон команды | Статус | Пример |
|----------------|--------|--------|
| Claim node | Реализовано | `"Claim node"` |
| Authorize node | **Реализовано** | `"authorize node <64-char-vibe-hash>"` |
| Развёртывание приложения | Реализовано | `"deploy application my-app"` |
| Патч приложения | **Реализовано** | `"patch app my-app to add logging"` |
| Статус / сетка | Реализовано | `"status grid"` |

**После claim:** включайте `nonce` + `command_signature` из `GET /nonce` в каждый запрос `/command`.

---

## Варианты развёртывания

| Метод | Статус | Платформа |
|-------|--------|-----------|
| `python3 utahmosphere_master.py` | **Рекомендуется** | Все |
| `python3 utahmosphere_os.py` | Реализовано | Все |
| `python3 genesis_deploy.py` | Реализовано | Linux / разработка |
| `sudo bash bootstrap.sh` | **Рекомендуется для prod** | Linux systemd |
| `sudo bash setup.sh` | Реализовано | Псевдоним bootstrap |
| `python3 genesis_iso_builder.py` | **Реализовано** | Linux — собирает `utah_genesis_v26.iso` |
| `./mk_iso.sh` | **Реализовано** | Обёртка для сборщика Genesis ISO |
| `docker-compose up` | Опционально | Только унаследованное удобство |

---

## Дорожная карта

Все пункты дорожной карты v25.x **реализованы** в v26.0. Будущая работа:

- Аттестация оборудования для автоустановки Genesis ISO
- Отказоустойчивость mempool в нескольких регионах
- Автоматическое подписание nonce в Voice Bridge

См. [Справочник API](API_REFERENCE.md) и [Справочник разработчика](DEVELOPER_COOKBOOK.md) для текущих деталей реализации.
