# Матрица возможностей

UtahMosphere OS **v34.0 Utah-Claw** — суверенная цепочка доверия завершена.

---

## HTTP API — конечные точки

| Конечная точка | Метод | Статус | Примечания |
|----------------|-------|--------|------------|
| `/health` | GET | **Реализовано** | `build: omega-build-v34-utah-claw` + полный снимок аттестации |
| `/attestation/quote` | GET | **Реализовано** | RA-TLS TPM quote для проверки mesh-узлов |
| `/registry/quotes` | GET | **Реализовано** | Глобальный реестр аппаратных цитат |
| `/registry/purge` | POST | **Реализовано** | Удаление скомпрометированного оборудования |
| `/claw/void` | POST | **Реализовано** | Диспетчеризация эпистемической пустоты |
| `/claw/status` | GET | **Реализовано** | Статистика UtahClaw runner |
| `/chrono/status` | GET | **Реализовано** | Статус Chrono-State |
| `/siphon/ghost-tune` | GET | **Реализовано** | Бинарник Ghost Tune |
| `/omni/compile` | POST | **Реализовано** | Компиляция агентного намерения |
| `/omni/status` | GET | **Реализовано** | Статистика Omni-Mind |
| `/omni/glass` | GET | **Реализовано** | Журнал агентных событий |
| `/witness/status` | GET | **Реализовано** | Кворум-свидетели в нескольких регионах |
| `/lazarus/status` | GET | **Реализовано** | Контрольная точка Lazarus |
| `/lazarus/restore` | POST | **Реализовано** | Восстановление Golden Master |
| `/quorum/consensus` | GET | **Реализовано** | Реестр кворум-голосов |
| `/dht/consensus` | GET | **Реализовано** | DHT золотой реестр |
| `/dht/challenge` | POST | **Реализовано** | Вызов аттестации роя |
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
| **Quorum Engine (`dht_consensus_engine.py`)** | **Реализовано** | 51%+ vote consensus |
| **DHT Golden Registry (`dht_quote_registry.py`)** | **Реализовано** | Swarm consensus verify |
| **PCR Drift (`drift_detector.py`)** | **Реализовано** | Auto-quarantine on drift |
| **Quote Registry (`quote_registry.py`)** | **Реализовано** | Register, purge, merge hardware quotes |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Реализовано** | CA pinning; UtahX ingress |
| **RA-TLS (`ra_tls_attest.py`)** | **Реализовано** | TPM quote в mesh gossip; проверка узлов перед синхронизацией |
| **Failover mempool (`tycoon_failover.py`)** | **Реализовано** | Failover US / EU / global / **Океания** в 4 регионах |
| **Аттестация оборудования (`attestation_guard.py`)** | **Реализовано** | Шлюз PCR0 в bootstrap |
| **Voice Bridge Signed** | **Реализовано** | Автоматический nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Реализовано** | Безопасность mesh + голоса |
| **UtahNetes + Swarm DHT** | **Реализовано** | RA-TLS + подписанный gossip |
| **Genesis ISO v34** | **Реализовано** | `utah_genesis_v34.iso` |
| **Полная облачная паритетность** | **Реализовано** | S3, Lambda, RDS, UtahX, контейнеры |

---

## Развёртывание

| Метод | Статус |
|-------|--------|
| `python3 utahmosphere_master.py` | **Рекомендуется** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v34 ISO** |

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Требовать TPM seal при claim |
| `UTAH_QUORUM_ENFORCE` | `1` | Кворум большинства |
| `UTAH_WITNESS_ENFORCE` | `1` | Мультирегиональные свидетели |
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Автовосстановление |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec при восстановлении |
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Запутанная delta-синхронизация |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | Требовать RA-TLS quote в mesh |
| `UTAH_MEMPOOL_NODES` | 4 по умолчанию | Переопределить список failover mempool |

| `UTAH_CLAW_ENFORCE` | `1` | Фоновый UtahClaw |
| `UTAH_CHRONO_ENFORCE` | `1` | Откат Chrono-State |
| `UTAH_OMNI_GLASS_STREAM` | `1` | SSE-поток Omni-Glass |
| `UTAH_OMNI_ENFORCE` | `1` | Omni-Compiler |

## Дорожная карта

Все пункты дорожной карты v28.0 **реализованы** в v34.0.

Будущее: удалённое закрепление RA-TLS CA, сервис реестра hardware quote.

См. [Справочник API](API_REFERENCE.md) и [Справочник разработчика](DEVELOPER_COOKBOOK.md).
