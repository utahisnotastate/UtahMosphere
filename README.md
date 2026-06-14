# 🌌 UtahMosphere OS (v25.0 Omega-Genesis)

**The Sovereign, Decentralized, Zero-Maintenance Autonomous Cloud Platform.**

UtahMosphere OS is a unified sovereign edge platform that runs on bare-metal hardware (Mini PC, Raspberry Pi, x86) and provides voice-driven deployment, biometric node ownership, and optional pay-per-access monetization.

---

## 📚 Documentation Portal

**[Full documentation index →](docs/README.md)**  
**[Other languages →](docs/LANGUAGES.md)** — separate single-language sites (Estonian, Russian, French, Finnish, Swedish, Chamorro, Spanish, Chinese)

### By role

| Role | Overview | Tutorial | Recipes |
|------|----------|----------|---------|
| Kids & families | [ELI5](docs/ELI5_FOR_KIDS.md) | [First Robot Butler](docs/tutorials/01-kids-first-robot-butler.md) | [Kids Activities](docs/recipes/kids-activities.md) |
| Executives | [Executive Summary](docs/EXECUTIVE_SUMMARY.md) | [Executive Quickstart](docs/tutorials/02-executive-quickstart.md) | [Executive Recipes](docs/recipes/executive-recipes.md) |
| Architects | [Technical Deep-Dive](docs/TECHNICAL_DEEP_DIVE.md) | [Architect Deployment](docs/tutorials/03-architect-deployment.md) | [Architect Recipes](docs/recipes/architect-recipes.md) |
| Cloud migrators | [Migration Guide](docs/CLOUD_PARITY_MIGRATION.md) | [Migration Walkthrough](docs/tutorials/04-cloud-migration-walkthrough.md) | [Migration Recipes](docs/recipes/migration-recipes.md) |
| Developers | [Developer Cookbook](docs/DEVELOPER_COOKBOOK.md) | [Your First App](docs/tutorials/05-developer-first-app.md) | [All Recipes](docs/recipes/README.md) |
| Non-technical | [User Guide](docs/NON_TECHNICAL_GUIDE.md) | [Setup Without Jargon](docs/tutorials/06-non-technical-setup.md) | [Ops Recipes](docs/recipes/ops-recipes.md) |

### Reference

- [API Reference](docs/API_REFERENCE.md) — `/health`, `/status`, `/command`, `/app/{name}`
- [Capability Matrix](docs/CAPABILITY_MATRIX.md) — what works today vs. roadmap
- [Local Development](docs/LOCAL_DEVELOPMENT.md) — Windows, macOS, Linux without root
- [Operations Runbook](docs/OPERATIONS_RUNBOOK.md) — backup, recovery, monitoring

### Templates & projects

- **[templates/](templates/)** — boilerplate handlers, clients, upload helpers
- **[examples/](examples/)** — runnable scripts against the live API
- **[starter-projects/](starter-projects/)** — forkable mini-apps

---

## 🚀 Quick Start

### Linux (production)

```bash
sudo bash setup.sh
sudo python3 genesis_deploy.py
```

### Local dev (any OS)

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"   # PowerShell: $env:UTAH_DATA_DIR = "$PWD\.utah-data"
pip install -r requirements.txt
python utahmosphere_os.py
```

Verify:

```bash
curl http://127.0.0.1:8999/health
python examples/voice-deploy-simulator/deploy.py hello
```

### Voice (optional)

```bash
python voice_bridge.py
```

Say: **"Claim node"** then **"deploy application my-app"**

### Docker (optional)

```bash
docker-compose up -d
```

> Docker and Nginx configs are **optional** convenience paths. The sovereign runtime is bare-metal Python. See [Capability Matrix](docs/CAPABILITY_MATRIX.md).

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `UTAH_SECRET_VECTOR` | (in-code default) | HMAC secret — **change in production** |
| `UTAH_DATA_DIR` | `/var/lib/utahmosphere` | Registry, containers, UtahX manifests |
| `UTAH_PROXY_CONF_DIR` | `/etc/nginx/sites-enabled` | Legacy proxy path |
| `UTAH_XPUB` | placeholder | Tycoon master xpub |
| `UTAH_ENV` | — | Environment label |

---

## 🛠 Features

- **UtahX** — Declarative proxy route manifests (JSON)
- **UtahContainerEngine** — Tenant workspaces with `handler.py`
- **UtahNetes** — LAN multicast gossip sync
- **Lazarus Daemon** — Live handler patching (partial)
- **Quantum Ledger** — Biometric vibe-print node claim
- **Global Swarm** — UDP P2P peer table
- **Utah-Tycoon** — HTTP 402 payment gate
- **Utah-Flux** — Reactive Tkinter dashboard

---

## 🔒 Security

HMAC-SHA256 tenant isolation (future storage APIs), single-owner biometric claim for voice commands. See [Access Control](docs/ACCESS_CONTROL.md).

---

## 🤝 Contributing

See [CONTRIBUTING](docs/CONTRIBUTING.md) and [CHANGELOG](docs/CHANGELOG.md).

---
*UtahMosphere: Reclaiming the Digital Horizon.*
