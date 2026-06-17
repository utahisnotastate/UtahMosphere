# UtahClaw Ambient Runner (v34.0)

**UtahClaw** es el subconsciente compilado de UtahMosphere: un daemon ambiental no bloqueante que llena **vacíos epistémicos** cuando Omni-Compiler encuentra capacidades desconocidas (Stripe GraphQL, Twilio).

## Topología

```
Intención no resuelta → EpistemicVoid
        |
        v
[UtahClaw Ambient Runner]
   /        |        \
Web/DHT   Memoria       Sandbox
scraper   holográfica   compilador
        |
[Herramienta MCP forjada → inyección Lazarus]
```

## Módulos (`utahclaw/`)

| Módulo | Propósito |
|--------|-----------|
| `ambient_runner.py` | Investigación asíncrona + forja de herramientas MCP |
| `holographic_memory.py` | Patrones de interferencia conceptual |
| `epistemic_void.py` | Excepción `EpistemicVoid` + detección |
| `kinematic_siphon.py` | Codificación binaria Ghost Tune B-Web |
| `service.py` | HTTP fast-socket en puerto **9090** |

## API HTTP

### POST /claw/void (kernel, puerto 8999)

```bash
curl -X POST http://127.0.0.1:8999/claw/void \
  -H "Content-Type: application/json" \
  -d '{"concept": "Integrate with Stripe GraphQL API"}'
```

### GET /claw/status

Investigaciones pendientes, herramientas forjadas, estadísticas de memoria holográfica.

## Integración Omni-Compiler

Cuando la intención coincide con palabras clave de vacío (`stripe`, `graphql`, `twilio`), `omni_compiler.py` delega a UtahClaw.

## Entorno

| Variable | Predeterminado | Propósito |
|----------|----------------|-----------|
| `UTAH_CLAW_ENFORCE` | `1` | Habilitar runner (`0` = dev) |
| `UTAH_CLAW_PORT` | `9090` | Fast-socket UtahClaw |
| `UTAH_CLAW_TOOLS_DIR` | `{UTAH_DATA_DIR}/mcp_tools` | Herramientas MCP forjadas |

## Ver también

- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [Chrono-State](CHRONO_STATE.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
