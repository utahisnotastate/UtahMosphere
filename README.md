# 🌌 UtahMosphere OS (v25.0 Omega-Genesis)

**The Sovereign, Decentralized, Zero-Maintenance Autonomous Cloud Platform.**

UtahMosphere OS is a revolutionary platform that completely discards legacy cloud abstractions (Docker, Nginx, K8s) in favor of a unified, sovereign architectural ecosystem. It leverages local bare-metal footprints to provide infinite compute, storage, and financial sovereignty.

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

2.  **Start the Sovereign Engine:**
    ```bash
    sudo python3 genesis_deploy.py
    ```
    *Or via Docker-Compose:*
    ```bash
    docker-compose up -d
    ```

3.  **Calibrate Biometric Voice Interface:**
    ```bash
    python3 voice_bridge.py
    ```
    *Say: "Claim node" to bind the hardware to your unique acoustic signature.*

4.  **Deploy your first Sovereign Container:**
    Just say: *"Butler, deploy application my-app"*

---

## ⚙️ Configuration

UtahMosphere OS can be configured via environment variables:

- `UTAH_SECRET_VECTOR`: The HMAC secret key for tenant isolation (default: provided in code).
- `UTAH_DATA_DIR`: The root directory for storage and registry (default: `/var/lib/utahmosphere`).
- `UTAH_PROXY_CONF_DIR`: The path for Nginx virtual host configs (default: `/etc/nginx/sites-enabled`).

---

## 🛠 Features
- **UtahX:** Fluidic TCP Proxy & Tollbooth Caching (Replaces Nginx).
- **UtahContainerEngine:** Cryptographic execution sandboxes (Replaces Docker).
- **UtahNetes:** Osmotic LAN/WAN discovery mesh (Replaces Kubernetes).
- **Lazarus Daemon:** Zero-downtime AST live code mutation.
- **Quantum Ledger:** Biometric Vibe-Print authentication.
- **Global Swarm:** DNS-bypassing P2P routing protocol.
- **Utah-Tycoon:** Automated cryptographic settlement daemon.
- **Utah-Flux:** Reactive, state-driven UI engine.

---

## 🔒 Security
UtahMosphere uses HMAC-SHA256 tokenization for multi-tenant isolation. Your data is anchored locally and synchronized only with trusted mesh peers.

---
*UtahMosphere: Reclaiming the Digital Horizon.*
