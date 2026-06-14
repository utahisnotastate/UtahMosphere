# UtahMosphere-dokumentationsportal

Välkommen till UtahMosphere OS dokumentation. **v25.1 Migration Ready** — enhetlig bare-metal-kärna med Utah-Tycoon, UtahNetes och Global Swarm fullt integrerade. Innehållet är organiserat efter **roll**, **guider**, **recept** och **startprojekt**.

---

## Börja här

| Dokument | Bäst för |
|----------|----------|
| [Kapacitetsmatris](CAPABILITY_MATRIX.md) | Alla — vad som fungerar idag vs. roadmap |
| [API-referens](API_REFERENCE.md) | Utvecklare och operatörer |
| [Guide för lokal utveckling](LOCAL_DEVELOPMENT.md) | Utvecklare på Windows, macOS eller Linux |

---

## Rollguider

| Roll | Översikt | Guide | Recept |
|------|----------|-------|--------|
| **Barn och familjer** | [Förklarat för barn](ELI5_FOR_KIDS.md) | [Din första robotbutler](tutorials/01-kids-first-robot-butler.md) | [Receptindex](recipes/README.md) |
| **Chefer (CEO/CTO)** | [Sammanfattning för ledningen](EXECUTIVE_SUMMARY.md) | — | [Receptindex](recipes/README.md) |
| **Arkitekter** | [Teknisk djupdykning](TECHNICAL_DEEP_DIVE.md) | — | [Receptindex](recipes/README.md) |
| **Utvecklare** | [Utvecklarkokbok](DEVELOPER_COOKBOOK.md) | [Din första app](tutorials/05-developer-first-app.md) | [Receptindex](recipes/README.md) |
| **Icke-tekniska användare** | [Icke-teknisk guide](NON_TECHNICAL_GUIDE.md) | [Installation utan jargong](tutorials/06-non-technical-setup.md) | [Receptindex](recipes/README.md) |

---

## Guider

1. [Din första robotbutler](tutorials/01-kids-first-robot-butler.md) — barn och familjer
2. [Din första app](tutorials/05-developer-first-app.md) — utvecklarens hela flöde
3. [Installation utan jargong](tutorials/06-non-technical-setup.md) — icke-teknisk onboarding

---

## Recept

- [Receptindex](recipes/README.md)

---

## Mallar och startprojekt

| Mall | Syfte |
|------|-------|
| [python-http-service](../../templates/python-http-service/) | HTTP-mikrotjänst |
| [container-handler](../../templates/container-handler/) | `handler.py` |
| [voice-command-client](../../templates/voice-command-client/) | `/command`-klient |
| [frontend-upload](../../templates/frontend-upload/) | Webbläsarklient |
| [tycoon-payment-client](../../templates/tycoon-payment-client/) | HTTP 402-betalning |

| Exempel | Beskrivning |
|---------|-------------|
| [hello-world](../../examples/hello-world/) | Driftsättning via `/command` |
| [check-node-health](../../examples/check-node-health/) | Hälsokontroll |
| [paid-app-access](../../examples/paid-app-access/) | Tycoon-betalningsgrind |
| [voice-deploy-simulator](../../examples/voice-deploy-simulator/) | Utan mikrofon |

| Startprojekt | Beskrivning |
|--------------|-------------|
| [minimal-api](../../starter-projects/minimal-api/) | Minimalt API |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Röst + instrumentpanel |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Betald åtkomst |

---

## UtahMosphere OS v25.0

- **Suverän edge-plattform** i Python — port `8999`
- **Röstdriftsättning** — Voice Bridge eller `POST /command`
- **Biometrisk claim** — kommandot «Claim node»
- **Tycoon HTTP 402** — `GET /app/{name}`
