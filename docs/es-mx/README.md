# Portal de documentación UtahMosphere

Bienvenido al centro de documentación de UtahMosphere OS v25.1 — plataforma soberana edge Python, puerto **8999**. **Migration Ready v25.1**: núcleo unificado bare-metal con liquidación mempool Tycoon, aplicación AuthGuard `authorized_nodes[]`, instalador Genesis ISO (`mk_iso.sh`), UtahNetes y Global Swarm totalmente operativos. El contenido está organizado por **perfil de audiencia**, **tutoriales prácticos**, **recetas listas para copiar y pegar** y **proyectos de arranque**.

---

## Empieza aquí

| Documento | Ideal para |
|-----------|------------|
| [Matriz de capacidades](CAPABILITY_MATRIX.md) | Todos — qué funciona hoy vs. hoja de ruta |
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

## Acerca de esta documentación

Esta sección de documentación está completamente en español de México. UtahMosphere OS v25.1 Migration Ready es una plataforma soberana edge basada en Python, build `golden-master-v25.1`, accesible por defecto en el puerto **8999**. Funciones clave: liquidación mempool Tycoon, aplicación `authorized_nodes[]` vía AuthGuard, instalador Genesis ISO (`./mk_iso.sh`), comando de voz `authorize node`.
