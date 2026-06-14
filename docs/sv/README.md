# UtahMosphere-dokumentationsportal

Välkommen till UtahMosphere OS dokumentation. **v27.0 Production Immutable** — suveräna förtroendeankare: TPM-hårdvaruattestering, mempool-failover i flera regioner och Voice Bridge med automatisk nonce-signering. Innehållet är organiserat efter **roll**, **guider**, **recept** och **startprojekt**.

---

## Börja här

| Dokument | Bäst för |
|----------|----------|
| [Kapacitetsmatris](CAPABILITY_MATRIX.md) | Alla — vad som fungerar idag vs. framtida arbete |
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
| [omega-build-verify](../../examples/omega-build-verify/) | Fullständigt S3/Lambda/RDS/container-test |

| Startprojekt | Beskrivning |
|--------------|-------------|
| [minimal-api](../../starter-projects/minimal-api/) | Minimalt API |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Röst + instrumentpanel |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Betald åtkomst |

---

## UtahMosphere OS v27.0

- **Suverän edge-plattform** i Python — port `8999`, `build: omega-build-v27-production`
- **Röstdriftsättning** — Voice Bridge (`voice_bridge_signed.py`) anropar automatiskt `GET /nonce` och signerar
- **TPM-attestering** — `attestation_guard.py` i bootstrap; fält i `/health` och `/status`
- **Mempool-failover** — `tycoon_failover.py` (mempool.space, signet, blockstream)
- **Biometrisk claim** — kommandot «Claim node»; `GET /nonce` mot återuppspelning
- **Nodåterkallande** — `POST /admin/revoke-node` och Utah-Flux-panel
- **Genesis ISO** — `genesis_iso_builder.py` / `mk_iso.sh` → `utah_genesis_v27.iso`
- **Tycoon HTTP 402** — `GET /app/{name}` med mempool-failover-avveckling
