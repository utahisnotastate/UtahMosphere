# UtahMosphere Documentation Portal

Welcome to the UtahMosphere OS documentation hub. Content is organized by **audience role**, **hands-on tutorials**, **copy-paste recipes**, and **starter projects**.

**Other languages:** Each locale is a fully separate site (one language per page). See [Documentation Languages](LANGUAGES.md).

---

## Start Here

| Document | Best for |
|----------|----------|
| [Omega-Build Golden Master](OMEGA_BUILD.md) | Everyone — unified kernel architecture |
| [UtahClaw](UTAH_CLAW.md) | Ambient epistemic void resolver |
| [Omni-Glass UI](OMNI_GLASS_UI.md) | Real-time agentic visual telemetry |
| [Chrono-State](CHRONO_STATE.md) | Live mutation rewind (no CI/CD) |
| [Kinematic Siphon](KINEMATIC_SIPHON.md) | Ghost Tune GPU client protocol |
| [Omni-Compiler](OMNI_COMPILER.md) | Agentic intent → live deployment |
| [MCP Omni-Bridge](MCP_OMNI_BRIDGE.md) | Context-aware code generation |
| [Utah-Omni-Mind](UTAH_OMNI_MIND.md) | Sovereign local LLM inference |
| [Quorum Witnesses](QUORUM_WITNESSES.md) | Multi-region ISP-outage tie-breakers |
| [Lazarus Auto-Restore](LAZARUS_RESTORE.md) | Clean-room Golden Master restoration |
| [State-Diff Engine](STATE_DIFF_ENGINE.md) | Entangled <1KB mesh synchronization |
| [Federated Quorum Consensus](QUORUM_CONSENSUS.md) | 51%+ majority DHT vote ledger |
| [PCR Drift Detection](PCR_DRIFT.md) | Automated PCR0 monitor + emergency quarantine |
| [Hardware Quote Registry](QUOTE_REGISTRY.md) | Global TPM hardware fingerprint ledger |
| [RA-TLS Mesh Attestation](RA_TLS.md) | TPM quote verification + CA pinning for mesh peers |
| [Hardware Attestation](ATTESTATION.md) | TPM PCR0 + Vibe-Print sealing |
| [Genesis ISO Installer](GENESIS_ISO.md) | Flash-drive UEFI boot image |
| [OTA Lazarus Channel](OTA_LAZARUS.md) | Over-the-air swarm kernel updates |
| [API Reference](API_REFERENCE.md) | Developers and operators |
| [Access Control Model](ACCESS_CONTROL.md) | Architects and security reviewers |
| [Local Development Guide](LOCAL_DEVELOPMENT.md) | Developers on Windows, macOS, or Linux |
| [Operations Runbook](OPERATIONS_RUNBOOK.md) | Sysadmins and on-call engineers |

---

## Role Guides (Overview)

| Role | Overview doc | Tutorial | Recipes |
|------|--------------|----------|---------|
| **Kids & families** | [ELI5 For Kids](ELI5_FOR_KIDS.md) | [Tutorial: Your First Robot Butler](tutorials/01-kids-first-robot-butler.md) | [Kids Activities](recipes/kids-activities.md) |
| **Executives (CEO/CTO)** | [Executive Summary](EXECUTIVE_SUMMARY.md) | [Tutorial: Executive Quickstart](tutorials/02-executive-quickstart.md) | [Executive Recipes](recipes/executive-recipes.md) |
| **Architects** | [Technical Deep-Dive](TECHNICAL_DEEP_DIVE.md) | [Tutorial: Architect Deployment](tutorials/03-architect-deployment.md) | [Architect Recipes](recipes/architect-recipes.md) |
| **Cloud migrators** | [Cloud Parity Migration](CLOUD_PARITY_MIGRATION.md) | [Tutorial: Migration Walkthrough](tutorials/04-cloud-migration-walkthrough.md) | [Migration Recipes](recipes/migration-recipes.md) |
| **Developers** | [Developer Cookbook](DEVELOPER_COOKBOOK.md) | [Tutorial: Your First App](tutorials/05-developer-first-app.md) | [Frontend](recipes/frontend-recipes.md) · [Backend](recipes/backend-recipes.md) · [Voice](recipes/voice-recipes.md) |
| **Non-technical users** | [Non-Technical Guide](NON_TECHNICAL_GUIDE.md) | [Tutorial: Setup Without Jargon](tutorials/06-non-technical-setup.md) | [Ops Recipes](recipes/ops-recipes.md) |

---

## Tutorials (Step-by-Step)

1. [Your First Robot Butler](tutorials/01-kids-first-robot-butler.md) — kids & families
2. [Executive Quickstart](tutorials/02-executive-quickstart.md) — business leaders
3. [Architect Deployment](tutorials/03-architect-deployment.md) — system design & topology
4. [Cloud Migration Walkthrough](tutorials/04-cloud-migration-walkthrough.md) — AWS/GCP/Azure owners
5. [Your First App](tutorials/05-developer-first-app.md) — end-to-end developer flow
6. [Setup Without Jargon](tutorials/06-non-technical-setup.md) — non-technical onboarding

---

## Recipes (Copy-Paste Code)

- [Recipes Index](recipes/README.md) — master list of all recipes
- [Executive Recipes](recipes/executive-recipes.md) — ROI worksheets, hybrid migration checklists
- [Architect Recipes](recipes/architect-recipes.md) — topology diagrams, port maps, mesh config
- [Migration Recipes](recipes/migration-recipes.md) — S3/Lambda/RDS parity patterns
- [Frontend Recipes](recipes/frontend-recipes.md) — uploads, API clients, payment flows
- [Backend Recipes](recipes/backend-recipes.md) — handlers, sessions, HMAC signing
- [Voice Recipes](recipes/voice-recipes.md) — custom intents, biometric calibration
- [Ops Recipes](recipes/ops-recipes.md) — systemd, backups, troubleshooting
- [Kids Activities](recipes/kids-activities.md) — fun experiments with the butler

---

## Templates & Starter Projects

### Templates (`templates/`)

Reusable boilerplate you can copy into your own project:

| Template | Purpose |
|----------|---------|
| [python-http-service](../templates/python-http-service/) | Standalone HTTP microservice |
| [container-handler](../templates/container-handler/) | UtahContainerEngine `handler.py` |
| [voice-command-client](../templates/voice-command-client/) | Programmatic `/command` client |
| [frontend-upload](../templates/frontend-upload/) | Browser upload client |
| [tycoon-payment-client](../templates/tycoon-payment-client/) | HTTP 402 payment flow |

### Examples (`examples/`)

Small runnable scripts that exercise the live API:

| Example | What it demonstrates |
|---------|---------------------|
| [hello-world](../examples/hello-world/) | Deploy an app via `/command` |
| [check-node-health](../examples/check-node-health/) | Health and status probes |
| [paid-app-access](../examples/paid-app-access/) | Tycoon tollbooth settlement |
| [omega-build-verify](../examples/omega-build-verify/) | Full S3/Lambda/RDS/container parity test |

### Starter Projects (`starter-projects/`)

Full mini-projects to fork and extend:

| Project | Description |
|---------|-------------|
| [minimal-api](../starter-projects/minimal-api/) | Smallest deployable API workload |
| [voice-controlled-dashboard](../starter-projects/voice-controlled-dashboard/) | Voice + status dashboard |
| [monetized-endpoint](../starter-projects/monetized-endpoint/) | Pay-to-access app pattern |

---

## Contributing & History

- [Contributing Guide](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
