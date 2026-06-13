# 🌌 UtahMosphere OS (v16.0 Master)

**The Sovereign, Decentralized, Zero-Maintenance Edge Cloud Platform.**

UtahMosphere OS is a state-of-the-art platform designed to liberate enterprises and individuals from the high costs and complexities of centralized cloud providers (AWS, GCP, Azure). By utilizing local hardware footprints and a peer-to-peer gossip mesh, UtahMosphere provides infinite compute and storage with zero egress fees.

---

## 📚 Documentation Portal

We have tailored documentation for every role:

- **[For Children (ELI5)](docs/ELI5_FOR_KIDS.md)** - House and Robot Butler analogy.
- **[Executive Summary](docs/EXECUTIVE_SUMMARY.md)** - Value prop and ROI for CEOs/CTOs.
- **[Technical Deep-Dive](docs/TECHNICAL_DEEP_DIVE.md)** - Architecture, P2P, and Security for Architects.
- **[Cloud Migration Guide](docs/CLOUD_PARITY_MIGRATION.md)** - Recipes for GCP/AWS/Azure owners and developers.
- **[Developer Cookbook](docs/DEVELOPER_COOKBOOK.md)** - Code recipes and boilerplate for Frontend/Backend devs.
- **[Non-Technical User Guide](docs/NON_TECHNICAL_GUIDE.md)** - The "It Just Works" overview.

---

## 🚀 Quick Start

1.  **Provision Hardware:**
    Run the automated setup script on a clean Ubuntu/Debian installation:
    ```bash
    sudo bash setup.sh
    ```

2.  **Start the Engine:**
    ```bash
    docker-compose up -d
    ```

3.  **Calibrate Voice Interface:**
    ```bash
    python3 voice_bridge.py
    ```

4.  **Deploy your first App:**
    Just say: *"Butler, deploy application my-app from git https://github.com/example/repo"*

---

## ⚙️ Configuration

UtahMosphere OS can be configured via environment variables:

- `UTAH_SECRET_VECTOR`: The HMAC secret key for tenant isolation (default: provided in code).
- `UTAH_DATA_DIR`: The root directory for storage and registry (default: `/var/lib/utahmosphere`).
- `UTAH_PROXY_CONF_DIR`: The path for Nginx virtual host configs (default: `/etc/nginx/sites-enabled`).

---

## 🛠 Features
- **S3 Mesh:** S3-compatible object storage with zero egress costs.
- **Lambda Realtime:** Serverless execution with microsecond cold-starts.
- **RDS Quantum Ledger:** State-synchronized distributed database.
- **Vibe-Coding:** Semantic intent parsing for infrastructure management.
- **Self-Healing:** Automated resource compaction and error correction.

---

## 🔒 Security
UtahMosphere uses HMAC-SHA256 tokenization for multi-tenant isolation. Your data is anchored locally and synchronized only with trusted mesh peers.

---
*UtahMosphere: Reclaiming the Digital Horizon.*
