# Матрица возможностей

UtahMosphere OS **v32.0 Lazarus Self-Healing** — суверенная цепочка доверия завершена.

---

## HTTP API — конечные точки

| Конечная точка | Метод | Статус | Примечания |
|----------------|-------|--------|------------|
| `/health` | GET | **Реализовано** | `build: omega-build-v32-lazarus-self-healing` + полный снимок аттестации |
| `/attestation/quote` | GET |
| `/registry/quotes` | GET | **Implemented** | Global hardware quote registry |
| `/registry/purge` | POST |
| `/witness/status` | GET | **Реализовано** | Кворум-свидетели в нескольких регионах |
| `/lazarus/status` | GET | **Реализовано** | Контрольная точка Lazarus |
| `/lazarus/restore` | POST | **Реализовано** | Восстановление Golden Master |
| `/quorum/consensus` | GET | **Implemented** | Majority-quorum ledger |
| `/dht/consensus` | GET | **Implemented** | DHT golden ledger |
| `/dht/challenge` | POST | **Implemented** | Swarm attestation challenge | **Implemented** | Purge compromised hardware | **Реализовано** | RA-TLS TPM quote для проверки mesh-узлов |
| `/nonce` | GET | **Реализовано** | Nonce против повторного воспроизведения голосовых команд |
| `/status` | GET | **Реализовано** | TPM lock, RA-TLS, регионы mempool Океании |
| `/command` | POST | **Реализовано** | Голос + nonce + TPM-привязанная проверка vibe |
| `/admin/revoke-node` | POST | **Реализовано** | Только root — отзыв узла |
| `/app/unlock` | POST | **Реализовано** | Расчёт через failover mempool в 4 регионах |
| `/app/{name}` | GET | **Реализовано** | Шлюз Tycoon 402 + прокси UtahX |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Реализовано** | Полная облачная паритетность |

---

## Основные подсистемы

| Компонент | Статус | Что работает сегодня |
|-----------|--------|----------------------|
| **TPM Locker (`tpm_lock.py`)** | **Реализовано** | Vibe-Print запечатан в PCR0 через `tpm2_create` / `tpm2_unseal` |
| **Кворум-свидетели (`quorum_witness.py`)** | **Реализовано** | Арбитры США/ЕС/Океания/Азия |
| **Восстановление Lazarus (`lazarus_restore.py`)** | **Реализовано** | Golden Master + атомный kexec |
| **Дельта состояния (`state_diff_engine.py`)** | **Реализовано** | Запутанные mesh-дельты |
| **Quorum Engine (`dht_consensus_engine.py`)** | **Implemented** | 51%+ vote consensus |
| **DHT Golden Registry (`dht_quote_registry.py`)** | **Implemented** | Swarm consensus verify |
| **PCR Drift (`drift_detector.py`)** | **Implemented** | Auto-quarantine on drift |
| **Quote Registry (`quote_registry.py`)** | **Implemented** | Register, purge, merge hardware quotes |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Implemented** | CA pinning; UtahX ingress |
| **RA-TLS (`ra_tls_attest.py`)** | **Реализовано** | TPM quote в mesh gossip; проверка узлов перед синхронизацией |
| **Failover mempool (`tycoon_failover.py`)** | **Реализовано** | Failover US / EU / global / **Океания** в 4 регионах |
| **Аттестация оборудования (`attestation_guard.py`)** | **Реализовано** | Шлюз PCR0 в bootstrap |
| **Voice Bridge Signed** | **Реализовано** | Автоматический nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Реализовано** | Безопасность mesh + голоса |
| **UtahNetes + Swarm DHT** | **Реализовано** | RA-TLS + подписанный gossip |
| **Genesis ISO v32** | **Реализовано** | `utah_genesis_v32.iso` |
| **Полная облачная паритетность** | **Реализовано** | S3, Lambda, RDS, UtahX, контейнеры |

---

## Развёртывание

| Метод | Статус |
|-------|--------|
| `python3 utahmosphere_master.py` | **Рекомендуется** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v32 ISO** |

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Требовать TPM seal при claim |
| `UTAH_QUORUM_ENFORCE` | `1` | Majority quorum |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | Требовать RA-TLS quote в mesh |
| `UTAH_MEMPOOL_NODES` | 4 по умолчанию | Переопределить список failover mempool |

## Дорожная карта

Все пункты дорожной карты v28.0 **реализованы** в v32.0.

Будущее: удалённое закрепление RA-TLS CA, сервис реестра hardware quote.

См. [Справочник API](API_REFERENCE.md) и [Справочник разработчика](DEVELOPER_COOKBOOK.md).
