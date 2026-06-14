# Matriz de capacidades

Esta matriz documenta lo que UtahMosphere OS **v25.0** implementa hoy frente a lo descrito en documentación de marketing o planificado para versiones futuras. Úsala para fijar expectativas realistas durante migración y desarrollo.

---

## Endpoints HTTP de la API

| Endpoint | Método | Estado | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Implementado** | Sonda de disponibilidad del nodo |
| `/status` | GET | **Implementado** | Estado UI, lista de inquilinos, estado de claim |
| `/command` | POST | **Implementado** | Ejecución de intención de voz (cuerpo JSON) |
| `/app/{name}` | GET | **Implementado** | Acceso a app protegido por Tycoon (402 hasta pagar) |
| `/s3/*` | * | Planificado | Documentado en guía de migración; aún no enrutado |
| `/lambda/*/invoke` | POST | Planificado | Stubs de handler creados solo al desplegar |
| `/rds/read/*`, `/rds/write` | * | Planificado | Registro existe; rutas HTTP no conectadas |

---

## Subsistemas principales

| Componente | Estado | Qué funciona hoy |
|------------|--------|------------------|
| **Kernel (`utahmosphere_os.py`)** | Implementado | Registro, intenciones de voz, manifiestos de rutas UtahX, gossip de malla |
| **Quantum Ledger** | Implementado | Claim vibe raíz, verificación de hash biométrico, modo abierto antes del claim |
| **Voice Bridge** | Implementado | Google STT + extracción vibe-print MFCC → `/command` |
| **Utah-Tycoon** | Parcial | Generación de facturas, liquidación simulada 60 s, puerta HTTP 402 |
| **Gossip UtahNetes** | Parcial | Sincronización de inquilinos por multidifusión UDP en LAN |
| **Global Swarm** | Parcial | Tabla de pares UDP, keep-alive ping; búsqueda Kademlia completa en stub |
| **Lazarus Daemon** | Parcial | Agrega comentarios de parche a `handler.py` (no reescritura AST completa) |
| **UI Utah-Flux** | Implementado | Tablero Tkinter leyendo `flux_ui_manifest.json` |
| **Proxy UtahX** | Parcial | Manifiestos de rutas JSON escritos; sin proceso proxy TCP en vivo |

---

## Comandos de voz (autorizados)

| Patrón de comando | Estado | Ejemplo |
|-------------------|--------|---------|
| Reclamar nodo | Implementado | `"Claim node"` |
| Desplegar aplicación | Implementado | `"deploy application my-app"` |
| Parchear aplicación | Parcial | `"patch app my-app to add logging"` |
| Estado / grid | Implementado | `"status grid"` |

---

## Opciones de despliegue

| Método | Estado | Plataforma |
|--------|--------|------------|
| `python3 utahmosphere_os.py` | Implementado | Todas (configura `UTAH_DATA_DIR` localmente) |
| `python3 genesis_deploy.py` | Implementado | Linux preferido; desarrollo en Windows OK |
| `sudo bash setup.sh` | Implementado | Linux (servicio systemd) |
| `docker-compose up` | Implementado | Opcional; usa red del host |

---

## Modelo de seguridad

| Característica | Estado | Notas |
|----------------|--------|-------|
| Titular vibe raíz único | Implementado | El primer hablante en reclamar es dueño del nodo |
| Campo `authorized_nodes[]` | Stub | Almacenado en ledger JSON; no aplicado en código |
| Firmas HMAC de inquilino | Documentado | Receta provista; aplicación parcial en kernel |
| Firma Ed25519 | Planificado | Referenciado en docs; no implementado |
| `UTAH_SECRET_VECTOR` predeterminado | Implementado | Cámbialo en producción (consulta [Referencia de API](API_REFERENCE.md)) |

---

## Relación Docker / Nginx

El **runtime principal** de UtahMosphere es Python bare-metal. Docker y Nginx son **rutas heredadas opcionales**:

- `docker-compose.yaml` — envoltorio de conveniencia para pruebas locales
- `nginx.conf` — configuración de referencia; los manifiestos JSON UtahX son la ruta soberana
- `setup.sh` — purga Docker/Nginx en instalaciones Linux limpias (nodos soberanos de producción)

Para entornos híbridos, mantén Docker/Nginx junto a UtahMosphere durante la migración.

---

## Hoja de ruta (aún no implementado)

- API HTTP de almacenamiento de objetos compatible con S3
- API HTTP de invocación estilo Lambda
- API HTTP de lectura/escritura del ledger RDS
- Comando de voz de despliegue basado en Git
- Mutación AST completa vía Lazarus
- Integración real de mempool Bitcoin en Tycoon

Consulta la [Matriz de capacidades](CAPABILITY_MATRIX.md) y el [Portal de documentación](README.md) para más detalles.
