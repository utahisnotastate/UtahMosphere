# UtahClaw ambient runner (v34.0)

**UtahClaw** — скомпилированное подсознание UtahMosphere: неблокирующий демон, заполняющий **эпистемические пустоты**, когда Omni-Compiler встречает неизвестные API (Stripe GraphQL, Twilio и т.д.).

## Топология

```
Неразрешённое намерение → EpistemicVoid
        |
        v
[UtahClaw Ambient Runner]
   /        |        \
Web/DHT   Голографическая   Песочница
скрейпер  память            компилятор
        |
[MCP-инструмент → Lazarus hot-inject]
```

## Модули (`utahclaw/`)

| Модуль | Назначение |
|--------|------------|
| `ambient_runner.py` | Асинхронное исследование + ковка MCP-инструментов |
| `holographic_memory.py` | Суперпозиция концептуальных интерференций |
| `epistemic_void.py` | Исключение `EpistemicVoid` + детекция пустоты |
| `kinematic_siphon.py` | Кодирование Ghost Tune B-Web |
| `service.py` | HTTP fast-socket на порту **9090** |

## HTTP API

### POST /claw/void (ядро, порт 8999)

```bash
curl -X POST http://127.0.0.1:8999/claw/void \
  -H "Content-Type: application/json" \
  -d '{"concept": "Integrate with Stripe GraphQL API"}'
```

### GET /claw/status

Ожидающие исследования, скованные инструменты, статистика голографической памяти.

## Интеграция с Omni-Compiler

При совпадении с ключевыми словами пустоты (`stripe`, `graphql`, `twilio`) `omni_compiler.py` передаёт задачу UtahClaw.

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `UTAH_CLAW_ENFORCE` | `1` | Включить runner (`0` = dev) |
| `UTAH_CLAW_PORT` | `9090` | Fast-socket UtahClaw |
| `UTAH_CLAW_TOOLS_DIR` | `{UTAH_DATA_DIR}/mcp_tools` | Скованные MCP-инструменты |

## См. также

- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [Chrono-State](CHRONO_STATE.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
