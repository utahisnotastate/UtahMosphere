# Portal de documentación UtahMosphere

Bienvenido al centro de documentación de UtahMosphere OS **v32.0 Lazarus Self-Healing** — plataforma soberana edge bare-metal unificada, puerto **8999**. La v32.0 completa la cadena de confianza soberana: **bloqueo TPM Vibe-Print**, **attestation RA-TLS de malla**, **failover mempool de 4 regiones** y **firma automática de nonce de voz** — del silicio al enjambre global. El contenido está organizado por **perfil de audiencia**, **tutoriales prácticos**, **recetas listas para copiar y pegar** y **proyectos de arranque**.

---

## Empieza aquí

| Documento | Ideal para |
|-----------|------------|
| [Testigos de quórum](QUORUM_WITNESSES.md) | Desempates multi-región ante caídas ISP |
| [Restauración Lazarus](LAZARUS_RESTORE.md) | Restauración Golden Master en sala limpia |
| [Motor de delta de estado](STATE_DIFF_ENGINE.md) | Sincronización mesh entrelazada <1 KB |
| [Matriz de capacidades](CAPABILITY_MATRIX.md) | Todos — v32.0 Lazarus Self-Healing vs. trabajo futuro |
| [Referencia de API](API_REFERENCE.md) | Desarrolladores y operadores |
| [Guía de desarrollo local](LOCAL_DEVELOPMENT.md) | Desarrolladores en Windows, macOS o Linux |

---

## Guías por perfil (resumen)

| Perfil | Documento de resumen | Tutorial | Recetas |
|--------|----------------------|----------|---------|
| **Niños y familias** | [Explicación para niños](ELI5_FOR_KIDS.md) | [Tutorial: Tu primer mayordomo robot](tutorials/01-kids-first-robot-butler.md) | [Índice de recetas](recipes/README.md) |
| **Directivos (CEO/CTO)** | [Resumen ejecutivo](EXECUTIVE_SUMMARY.md) | — | [Índice de recetas](recipes/README.md) |
| **Arquitectos** | [Inmersión técnica](TECHNICAL_DEEP_DIVE.md) | — | [Índice de recetas](recipes/README.md) |
| **Desarrolladores** | [Recetario del desarrollador](DEVELOPER_COOKBOOK.md) | [Tutorial: Tu primera aplicación](tutorials/05-developer-first-app.md) | [Índice de recetas](recipes/README.md) |
| **Usuarios no técnicos** | [Guía no técnica](NON_TECHNICAL_GUIDE.md) | [Tutorial: Configuración sin tecnicismos](tutorials/06-non-technical-setup.md) | [Índice de recetas](recipes/README.md) |

---

## Tutoriales (paso a paso)

1. [Tu primer mayordomo robot](tutorials/01-kids-first-robot-butler.md) — niños y familias
2. [Tu primera aplicación](tutorials/05-developer-first-app.md) — flujo de desarrollo de punta a punta
3. [Configuración sin tecnicismos](tutorials/06-non-technical-setup.md) — incorporación para usuarios no técnicos

---

## Recetas (código listo para copiar y pegar)

- [Índice de recetas](recipes/README.md) — lista maestra de todas las recetas

---

## Plantillas y proyectos de arranque

### Plantillas (`templates/`)

Código reutilizable que puedes copiar a tu propio proyecto:

| Plantilla | Propósito |
|-----------|-----------|
| [python-http-service](../../templates/python-http-service/) | Microservicio HTTP independiente |
| [container-handler](../../templates/container-handler/) | `handler.py` para UtahContainerEngine |
| [voice-command-client](../../templates/voice-command-client/) | Cliente programático para `/command` |
| [frontend-upload](../../templates/frontend-upload/) | Cliente de carga desde el navegador |
| [tycoon-payment-client](../../templates/tycoon-payment-client/) | Flujo de pago HTTP 402 |

### Ejemplos (`examples/`)

Scripts pequeños y ejecutables que usan la API en vivo:

| Ejemplo | Qué demuestra |
|---------|---------------|
| [hello-world](../../examples/hello-world/) | Desplegar una aplicación vía `/command` |
| [check-node-health](../../examples/check-node-health/) | Sondas de salud y estado |
| [paid-app-access](../../examples/paid-app-access/) | Liquidación mempool/electrum Tycoon |
| [omega-build-verify](../../examples/omega-build-verify/) | Prueba de paridad S3/Lambda/RDS/contenedor completa |
| [voice-deploy-simulator](../../examples/voice-deploy-simulator/) | Desplegar sin micrófono |

### Proyectos de arranque (`starter-projects/`)

Mini-proyectos completos para bifurcar y extender:

| Proyecto | Descripción |
|----------|-------------|
| [minimal-api](../../starter-projects/minimal-api/) | Carga de trabajo API desplegable más simple |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Tablero de voz + estado |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Patrón de aplicación de pago por acceso |

---

## Funciones v32.0 Lazarus Self-Healing

- **TPM Locker:** Vibe-Print sellado al PCR0 vía `tpm2_create` / `tpm2_unseal` (`tpm_lock.py`)
- **RA-TLS:** citas TPM en gossip de malla; verificación de pares antes de sync (`ra_tls_attest.py`)
- **Failover mempool:** failover US / EU / global / Oceanía en 4 regiones (`tycoon_failover.py`)
- **Attestation de hardware:** puerta PCR0 TPM 2.0 (`attestation_guard.py`) en bootstrap
- **Voice Bridge firmado:** `GET /nonce` automático + HMAC (`voice_bridge_signed.py`)
- **UtahX / ContainerEngine / S3 / Lambda / RDS:** paridad cloud completa
- **AuthGuard + Nonce-Guard + revocación Utah-Flux:** gobernanza de malla
- **Genesis ISO v32:** `utah_genesis_v32.iso`

Build `omega-build-v32-lazarus-self-healing`. Entrada recomendada: `python3 utahmosphere_master.py`.
