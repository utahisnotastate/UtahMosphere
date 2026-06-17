# Omni-Desk — суверенный магазин приложений (v35.0)

**Omni-Desk** — голографический рабочий стол UtahMosphere с ускорением GPU. В Time-3 мы не скачиваем приложения — **мы их манифестируем**.

## Genesis Suite

| ID | Название | Назначение |
|----|----------|------------|
| `web_forge` | **Omni-WebForge** | Сайт из документа, репозитория или голоса |
| `zeo_canvas` | **ZEO-Canvas** | Локальная генерация изображений |
| `app_smith` | **Kinematic-AppSmith** | Описание UI → Ghost Tune клиент |
| `holo_notebook` | **Holographic-Notebook** | Корпус PDF → автономные инструменты |
| `claw_harvester` | **UtahClaw-Harvester** | Извлечение MCP из кодовых баз |

## HTTP API (ядро 8999)

- `GET /desk/apps` — реестр Genesis
- `POST /desk/intent` — маршрутизация intent

См. [Omni-Compiler](../OMNI_COMPILER.md), [UtahClaw](UTAH_CLAW.md).
