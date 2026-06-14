# Матрица возможностей

UtahMosphere OS **v28.0 TPM-Hardened Attested** — суверенная цепочка доверия завершена.

---

## HTTP API — конечные точки

| Конечная точка | Метод | Статус | Примечания |
|----------------|-------|--------|------------|
| `/health` | GET | **Реализовано** | `build: omega-build-v28-attested` + полный снимок аттестации |
| `/attestation/quote` | GET | **Реализовано** | RA-TLS TPM quote для проверки mesh-узлов |
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
| **RA-TLS (`ra_tls_attest.py`)** | **Реализовано** | TPM quote в mesh gossip; проверка узлов перед синхронизацией |
| **Failover mempool (`tycoon_failover.py`)** | **Реализовано** | Failover US / EU / global / **Океания** в 4 регионах |
| **Аттестация оборудования (`attestation_guard.py`)** | **Реализовано** | Шлюз PCR0 в bootstrap |
| **Voice Bridge Signed** | **Реализовано** | Автоматический nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Реализовано** | Безопасность mesh + голоса |
| **UtahNetes + Swarm DHT** | **Реализовано** | RA-TLS + подписанный gossip |
| **Genesis ISO v28** | **Реализовано** | `utah_genesis_v28.iso` |
| **Полная облачная паритетность** | **Реализовано** | S3, Lambda, RDS, UtahX, контейнеры |

---

## Развёртывание

| Метод | Статус |
|-------|--------|
| `python3 utahmosphere_master.py` | **Рекомендуется** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v28 ISO** |

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Требовать TPM seal при claim |
| `UTAH_RA_TLS_ENFORCE` | `1` | Требовать RA-TLS quote в mesh |
| `UTAH_MEMPOOL_NODES` | 4 по умолчанию | Переопределить список failover mempool |

## Дорожная карта

Все пункты дорожной карты v27.0 **реализованы** в v28.0.

Будущее: удалённое закрепление RA-TLS CA, сервис реестра hardware quote.

См. [Справочник API](API_REFERENCE.md) и [Справочник разработчика](DEVELOPER_COOKBOOK.md).
