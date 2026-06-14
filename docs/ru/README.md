# Портал документации UtahMosphere

Добро пожаловать в центр документации UtahMosphere OS. **v28.0 TPM-Hardened Attested** — суверенная цепочка доверия: TPM Locker, RA-TLS mesh-аттестация, mempool Океании и Voice Bridge с автоподписанием nonce. Материалы организованы по **ролям аудитории**, **практическим руководствам**, **готовым рецептам** и **стартовым проектам**.

---

## С чего начать

| Документ | Для кого |
|----------|----------|
| [Матрица возможностей](CAPABILITY_MATRIX.md) | Все — что работает сегодня и будущая работа |
| [Справочник API](API_REFERENCE.md) | Разработчики и операторы |
| [Руководство по локальной разработке](LOCAL_DEVELOPMENT.md) | Разработчики на Windows, macOS или Linux |

---

## Руководства по ролям (обзор)

| Роль | Обзорный документ | Руководство | Рецепты |
|------|-------------------|-------------|---------|
| **Дети и семьи** | [Объяснение для детей](ELI5_FOR_KIDS.md) | [Учебник: Ваш первый робот-дворецкий](tutorials/01-kids-first-robot-butler.md) | [Индекс рецептов](recipes/README.md) |
| **Руководители (CEO/CTO)** | [Резюме для руководства](EXECUTIVE_SUMMARY.md) | — | [Индекс рецептов](recipes/README.md) |
| **Архитекторы** | [Техническое погружение](TECHNICAL_DEEP_DIVE.md) | — | [Индекс рецептов](recipes/README.md) |
| **Разработчики** | [Справочник разработчика](DEVELOPER_COOKBOOK.md) | [Учебник: Ваше первое приложение](tutorials/05-developer-first-app.md) | [Индекс рецептов](recipes/README.md) |
| **Нетехнические пользователи** | [Руководство без жаргона](NON_TECHNICAL_GUIDE.md) | [Учебник: Настройка без жаргона](tutorials/06-non-technical-setup.md) | [Индекс рецептов](recipes/README.md) |

---

## Учебники (пошагово)

1. [Ваш первый робот-дворецкий](tutorials/01-kids-first-robot-butler.md) — дети и семьи
2. [Ваше первое приложение](tutorials/05-developer-first-app.md) — сквозной поток для разработчиков
3. [Настройка без жаргона](tutorials/06-non-technical-setup.md) — онбординг для нетехнических пользователей

---

## Рецепты (готовый код для копирования)

- [Индекс рецептов](recipes/README.md) — полный список всех рецептов

---

## Шаблоны и стартовые проекты

### Шаблоны (`templates/`)

Переиспользуемый каркас, который можно скопировать в свой проект:

| Шаблон | Назначение |
|--------|------------|
| [python-http-service](../../templates/python-http-service/) | Автономный HTTP-микросервис |
| [container-handler](../../templates/container-handler/) | `handler.py` для UtahContainerEngine |
| [voice-command-client](../../templates/voice-command-client/) | Программный клиент `/command` |
| [frontend-upload](../../templates/frontend-upload/) | Клиент загрузки из браузера |
| [tycoon-payment-client](../../templates/tycoon-payment-client/) | Поток оплаты HTTP 402 |

### Примеры (`examples/`)

Небольшие запускаемые скрипты, демонстрирующие работу с живым API:

| Пример | Что демонстрирует |
|--------|-------------------|
| [hello-world](../../examples/hello-world/) | Развёртывание приложения через `/command` |
| [check-node-health](../../examples/check-node-health/) | Проверки работоспособности и статуса |
| [paid-app-access](../../examples/paid-app-access/) | Расчёт через Tycoon |
| [omega-build-verify](../../examples/omega-build-verify/) | Полный тест S3/Lambda/RDS/контейнер |

### Стартовые проекты (`starter-projects/`)

Полноценные мини-проекты для форка и расширения:

| Проект | Описание |
|--------|----------|
| [minimal-api](../../starter-projects/minimal-api/) | Минимальная развёртываемая API-нагрузка |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Голосовое управление и панель статуса |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Паттерн приложения с оплатой за доступ |

---

## Ключевые характеристики UtahMosphere OS v28.0

- **Суверенное периферийное облако** на Python — порт `8999`, `build: omega-build-v28-attested`
- **TPM Locker** — `tpm_lock.py` запечатывает Vibe-Print в PCR0 при claim
- **RA-TLS mesh-аттестация** — `ra_tls_attest.py` + `GET /attestation/quote`
- **Голосовое развёртывание** — Voice Bridge автоматически вызывает `GET /nonce` и подписывает
- **Failover mempool** — `tycoon_failover.py` в 4 регионах (US, EU, global, Океания)
- **Биометрическое закрепление узла** — команда «Claim node»; TPM-привязанная проверка vibe
- **Отзыв узлов** — `POST /admin/revoke-node` и панель Utah-Flux
- **Genesis ISO** — `genesis_iso_builder.py` → `utah_genesis_v28.iso`
- **Tycoon HTTP 402** — `GET /app/{name}` с расчётом через mempool в 4 регионах

---

## Дополнительные материалы

- [Матрица возможностей](CAPABILITY_MATRIX.md) — статус реализации v28.0
- [Справочник API](API_REFERENCE.md) — все конечные точки HTTP
- [Техническое погружение](TECHNICAL_DEEP_DIVE.md) — архитектура платформы
