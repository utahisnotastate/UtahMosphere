# Portal Dokumentasion UtahMosphere

Håfa adai ya bien binidu gi sentro dokumentasion UtahMosphere OS. **Golden Master Final v25.0** — unifikådo na bare-metal kernel yan Utah-Tycoon, UtahNetes, yan Global Swarm må'pos implement. Ma organisat i kontenidu pot **rol siha**, **leksion paso-paso**, **recepta kodu**, yan **proyektu inicio**.

---

## Tutuhon Guini

| Dokumentu | Mas maolek para |
|-----------|-----------------|
| [Matrisis Kapasidad](CAPABILITY_MATRIX.md) | Todu — håfa mumuña på'go vs plan futuru |
| [Referensia API](API_REFERENCE.md) | Desarrollador siha yan operadot siha |
| [Guia Desarrollu Lokal](LOCAL_DEVELOPMENT.md) | Desarrollador siha gi Windows, macOS, pat Linux |
| [Sumario Executivo](EXECUTIVE_SUMMARY.md) | CEO/CTO yan lideråt |
| [Guia Teknikal Deep-Dive](TECHNICAL_DEEP_DIVE.md) | Arquitecto siha yan engineer siha |

---

## Guias pot Rol

| Rol | Dokumentu overview | Leksion | Recepta |
|-----|-------------------|---------|---------|
| **Familia yan famagu'on** | [ELI5 para Famagu'on](ELI5_FOR_KIDS.md) | [Leksion: Primeru Robott Butler](tutorials/01-kids-first-robot-butler.md) | [Indeks Recepta](recipes/README.md) |
| **Executivo siha (CEO/CTO)** | [Sumario Executivo](EXECUTIVE_SUMMARY.md) | — | [Indeks Recepta](recipes/README.md) |
| **Arquitecto siha** | [Deep-Dive Teknikal](TECHNICAL_DEEP_DIVE.md) | — | [Indeks Recepta](recipes/README.md) |
| **Desarrollador siha** | [Cookbook Desarrollador](DEVELOPER_COOKBOOK.md) | [Leksion: Primeru App](tutorials/05-developer-first-app.md) | [Indeks Recepta](recipes/README.md) |
| **Usuarios ti teknikal** | [Guia Ti Teknikal](NON_TECHNICAL_GUIDE.md) | [Leksion: Setup Sin Jargon](tutorials/06-non-technical-setup.md) | [Indeks Recepta](recipes/README.md) |

---

## Leksion siha (Paso-paso)

1. [Primeru Robott Butler](tutorials/01-kids-first-robot-butler.md) — familia yan famagu'on
2. [Primeru App](tutorials/05-developer-first-app.md) — flujo kompleto desarrollador
3. [Setup Sin Jargon](tutorials/06-non-technical-setup.md) — onboarding ti teknikal

---

## Recepta siha (Kodu Copy-Paste)

- [Indeks Recepta](recipes/README.md) — lista kompleto gi docs/gu/

---

## Templates yan Starter Projects

### Templates (`templates/`)

Boilerplate para un copia gi proyecto-mu:

| Template | Para håfa |
|----------|-----------|
| [python-http-service](../../templates/python-http-service/) | HTTP microservice standalone |
| [container-handler](../../templates/container-handler/) | UtahContainerEngine `handler.py` |
| [voice-command-client](../../templates/voice-command-client/) | Client programmatico para `/command` |
| [frontend-upload](../../templates/frontend-upload/) | Client upload gi browser |
| [tycoon-payment-client](../../templates/tycoon-payment-client/) | HTTP 402 payment flow |

### Examples (`examples/`)

Scripts dikike' para usa i live API:

| Example | Håfa ma demo |
|---------|--------------|
| [hello-world](../../examples/hello-world/) | Deploy app via `/command` |
| [check-node-health](../../examples/check-node-health/) | Health yan status probes |
| [paid-app-access](../../examples/paid-app-access/) | Tycoon tollbooth settlement |
| [voice-deploy-simulator](../../examples/voice-deploy-simulator/) | Deploy sin mikrofonu |

### Starter Projects (`starter-projects/`)

Mini-proyectos kompleto para copia yan extend:

| Proyecto | Deskripsion |
|----------|-------------|
| [minimal-api](../../starter-projects/minimal-api/) | Menos workload API deployable |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Voice + status dashboard |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Pay-to-access app pattern |

---

## UtahMosphere OS v25.0 Golden Master Final

Suveranu edge Python platform — port `8999`, voice deploy, biometric claim, HTTP 402, `POST /app/unlock`.

**Mas dokumentu:** [Referensia API](API_REFERENCE.md) · [Matrisis Kapasidad](CAPABILITY_MATRIX.md)
