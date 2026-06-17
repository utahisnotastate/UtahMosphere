# Portal Dokumentasion UtahMosphere

Håfa adai ya bien binidu gi sentro dokumentasion UtahMosphere OS **v34.0 Utah-Claw** — unifikådo na bare-metal sovereign edge platform, port **8999**. I v34.0 ma kompleta i sovereign trust chain: **TPM Vibe-Print lock**, **RA-TLS mesh attestation**, **4-region mempool failover**, yan **automatic voice nonce signing** — ginen silicon asta global swarm. Ma organisat i kontenidu pot **rol siha**, **leksion paso-paso**, **recepta kodu**, yan **proyektu inicio**.

---

## Tutuhon Guini

| Dokumentu | Mas maolek para |
|-----------|-----------------|
| [Quorum Witnesses](QUORUM_WITNESSES.md) | Multi-region ISP-outage tie-breakers |
| [Lazarus Auto-Restore](LAZARUS_RESTORE.md) | Clean-room Golden Master restoration |
| [State-Diff Engine](STATE_DIFF_ENGINE.md) | Entangled <1KB mesh synchronization |
| [Matrisis Kapasidad](CAPABILITY_MATRIX.md) | Todu — v34.0 Utah-Claw vs. trabahu futuru |
| [Referensia API](API_REFERENCE.md) | Desarrollador siha yan operadot siha |
| [Guia Desarrollu Lokal](LOCAL_DEVELOPMENT.md) | Desarrollador siha gi Windows, macOS, pat Linux |

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
| [paid-app-access](../../examples/paid-app-access/) | Mempool/electrum Tycoon settlement |
| [omega-build-verify](../../examples/omega-build-verify/) | Full S3/Lambda/RDS/container parity test |
| [voice-deploy-simulator](../../examples/voice-deploy-simulator/) | Deploy sin mikrofonu |

### Starter Projects (`starter-projects/`)

Mini-proyectos kompleto para copia yan extend:

| Proyecto | Deskripsion |
|----------|-------------|
| [minimal-api](../../starter-projects/minimal-api/) | Menos workload API deployable |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Voice + status dashboard |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Pay-to-access app pattern |

---

## Features v34.0 Utah-Claw

- **TPM Locker:** Vibe-Print sealed gi PCR0 via `tpm2_create` / `tpm2_unseal` (`tpm_lock.py`)
- **RA-TLS:** TPM quotes gi mesh gossip; peer verification antes sync (`ra_tls_attest.py`)
- **Mempool Failover:** US / EU / global / Oceania 4-region failover (`tycoon_failover.py`)
- **Hardware Attestation:** TPM 2.0 PCR0 gate (`attestation_guard.py`) gi bootstrap
- **Voice Bridge Signed:** Auto `GET /nonce` + HMAC (`voice_bridge_signed.py`)
- **UtahX / ContainerEngine / S3 / Lambda / RDS:** Full cloud parity
- **AuthGuard + Nonce-Guard + Utah-Flux Revocation:** Mesh governance
- **Genesis ISO v33:** `utah_genesis_v34.iso`

Build `omega-build-v34-utah-claw`. Ma recommend na entry: `python3 utahmosphere_master.py`.
