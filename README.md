# 🌌 UtahMosphere OS (v29.0 Remote Attestation Infrastructure)

**The Sovereign, Decentralized, Zero-Maintenance Autonomous Cloud Platform.**

v29.0 completes **global swarm trust**: **Hardware Quote Registry**, **RA-TLS CA pinning**, and **biometric-to-TPM binding** — every node verifies every other node remotely via TPM-signed quotes.

**Architecture guide:** [Omega-Build Golden Master](docs/OMEGA_BUILD.md)

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

- [Omega-Build Golden Master Final](docs/OMEGA_BUILD.md) — unified kernel architecture
- [Genesis ISO Installer](docs/GENESIS_ISO.md) — flash-drive UEFI boot image (`mk_iso.sh`)
- [OTA Lazarus Channel](docs/OTA_LAZARUS.md) — over-the-air swarm kernel updates
- [API Reference](docs/API_REFERENCE.md) — S3, Lambda, RDS, `/app` proxy, `/app/unlock`, `/command`
- [Capability Matrix](docs/CAPABILITY_MATRIX.md) — what works today vs. roadmap
- [Local Development](docs/LOCAL_DEVELOPMENT.md) — Windows, macOS, Linux without root
- [Operations Runbook](docs/OPERATIONS_RUNBOOK.md) — backup, recovery, monitoring

### Templates & projects

- **[templates/](templates/)** — boilerplate handlers, clients, upload helpers
- **[examples/](examples/)** — runnable scripts against the live API
- **[starter-projects/](starter-projects/)** — forkable mini-apps

---

## 🚀 Quick Start

### Linux (production — Golden Master)

```bash
sudo bash bootstrap.sh
# or
sudo bash setup.sh
```

Installs `utah-genesis` systemd service and `utah-kernel` binary.

### Local dev (any OS)

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"   # PowerShell: $env:UTAH_DATA_DIR = "$PWD\.utah-data"
pip install -r requirements.txt
python3 utahmosphere_master.py
```

Verify Omega-Build:

```bash
curl http://127.0.0.1:8999/health
python examples/omega-build-verify/verify.py
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
| `UTAH_TYCOON_SETTLEMENT_MODE` | `auto` | `auto`, `real`, or `simulate` Bitcoin settlement |
| `UTAH_MEMPOOL_API` | `https://mempool.space/api` | Mempool confirmation endpoint |
| `UTAH_ELECTRUM_URL` | — | Optional electrum-server JSON-RPC URL |
| `UTAH_NONCE_ENFORCE` | `1` | Require nonce on `/command` after claim |
| `UTAH_NONCE_WINDOW_SEC` | `30` | Nonce freshness window |
| `UTAH_ATTESTATION_ENFORCE` | `1` | TPM PCR0 bootstrap gate |
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Seal Vibe-Print to TPM on claim |
| `UTAH_RA_TLS_ENFORCE` | `1` | Require RA-TLS quotes on mesh sync |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning + registry check |
| `UTAH_MEMPOOL_NODES` | 4 defaults | Comma-separated mempool API bases for failover |
| `UTAH_FLUX_ACOUSTIC_HASH` | — | Root hash for Utah-Flux revocation panel |

---

## 🛠 Features (v29.0 Remote Attested)

- **Quote Registry:** Global hardware fingerprint ledger (`quote_registry.py`)
- **RA-TLS Guard:** CA pinning + UtahX ingress (`ra_tls_guard.py`)
- **Biometric-to-TPM:** Claim registers hardware quote in global registry
- **Full v28 stack:** TPM Locker, RA-TLS mesh, Oceania mempool, nonce signing, AuthGuard, Genesis ISO

---

## 🔒 Security

HMAC-SHA256 tenant isolation (future storage APIs), single-owner biometric claim for voice commands. See [Access Control](docs/ACCESS_CONTROL.md).

---

## 🤝 Contributing

See [CONTRIBUTING](docs/CONTRIBUTING.md) and [CHANGELOG](docs/CHANGELOG.md).

---
*UtahMosphere: Reclaiming the Digital Horizon.*
