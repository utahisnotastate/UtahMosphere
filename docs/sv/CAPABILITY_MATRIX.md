# Kapacitetsmatris

UtahMosphere OS **v25.1 Migration Ready** — implementeringsstatus enligt Omega-Build.

---

## HTTP API-endpoints

| Endpoint | Metod | Status | Noteringar |
|----------|-------|--------|------------|
| `/health` | GET | **Implementerat** | Liveness-probe + `build: golden-master-v25.1` |
| `/status` | GET | **Implementerat** | UI-tillstånd, tenants, claim-status, S3-rot |
| `/command` | POST | **Implementerat** | Röstintent-exekvering |
| `/app/unlock` | POST | **Implementerat** | Skicka betalning; returnerar 202 tills avveckling |
| `/app/{name}` | GET | **Implementerat** | Tycoon 402-grind + UtahX-proxy till container |
| `/app/{name}/{path}` | GET | **Implementerat** | Subpath-proxy till container-backend |
| `/s3/{bucket}/{key}` | GET | **Implementerat** | Objektläsning (lokal NVMe) |
| `/s3/{bucket}/{key}` | PUT/POST | **Implementerat** | Objekt-skrivning; valfria HMAC-headers |
| `/s3/{bucket}/{prefix}*` | GET | **Implementerat** | Lista objekt |
| `/lambda/{fn}/invoke` | POST | **Implementerat** | Serverlös handler-invokering |
| `/lambda/{fn}` | GET | **Implementerat** | GET-invokering med tomt event |
| `/rds/write` | POST | **Implementerat** | Nyckel-värde-skrivning |
| `/rds/read/{key}` | GET | **Implementerat** | Nyckel-värde-läsning |

---

## Kärndelsystem

| Komponent | Status | Vad som fungerar idag |
|-----------|--------|----------------------|
| **Golden Master (`utahmosphere_master.py`)** | **Implementerat** | Enhetlig ingångspunkt |
| **Kärna (`utahmosphere_os.py`)** | **Implementerat** | Full HTTP-multiplexer, register, mesh |
| **UtahX Proxy (`utahx_proxy.py`)** | **Implementerat** | Live HTTP-proxy till containerportar |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Implementerat** | HTTP-servrar per tenant på 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Implementerat** | AST-validerad handler-mutation + OTA-kanal |
| **S3 Mesh (`utah_s3_mesh.py`)** | **Implementerat** | Lokal objektlagring + HMAC |
| **Lambda Engine (`utah_lambda_engine.py`)** | **Implementerat** | Handler-invokering utan images |
| **RDS Ledger (`utah_rds_ledger.py`)** | **Implementerat** | JSON nyckel-värde-register |
| **Quantum Ledger** | Implementerat | Biometrisk claim + verifiering |
| **Utah-Tycoon** | **Implementerat** | Mempool/electrum-avveckling (`tycoon_settlement.py`), `POST /app/unlock`, HTTP 402-grind |
| **UtahNetes Gossip** | **Implementerat** | AuthGuard-signerad 5s multicast via `utah_mesh_engine.py` |
| **Global Swarm** | **Implementerat** | Deterministisk DHT + signerad register-synk |
| **AuthGuard (`ledger_auth.py`)** | **Implementerat** | `authorized_nodes[]`-tillämpning för röst och mesh |
| **Genesis ISO (`mk_iso.sh`)** | **Implementerat** | UEFI/hybrid flash-installationsbyggare |
| **Utah-Flux UI** | Implementerat | Tkinter-statuspanel |
| **Auto-Genesis (`genesis_deploy.py`)** | **Implementerat** | Multiprocess-orkestrator |
| **Bootstrap (`bootstrap.sh`)** | **Implementerat** | Bare-metal systemd-installation |

---

## Röstkommandon

| Kommandomönster | Status | Exempel |
|-----------------|--------|---------|
| Claim node | Implementerat | `"Claim node"` |
| Deploy application | Implementerat | `"deploy application my-app"` |
| Patch application | **Implementerat** | `"patch app my-app to add logging"` |
| Authorize node | **Implementerat** | `"authorize node <64-char-vibe-hash>"` |
| Status / grid | Implementerat | `"status grid"` |

---

## Driftsättningsalternativ

| Metod | Status | Plattform |
|-------|--------|-----------|
| `python3 utahmosphere_master.py` | **Rekommenderas** | Alla |
| `python3 utahmosphere_os.py` | Implementerat | Alla |
| `python3 genesis_deploy.py` | Implementerat | Linux / dev |
| `sudo bash bootstrap.sh` | **Rekommenderas prod** | Linux systemd |
| `sudo bash setup.sh` | Implementerat | Alias till bootstrap |
| `./mk_iso.sh` | **Implementerat** | Linux — bygger `utah_genesis_v25.iso` |
| `docker-compose up` | Valfritt | Endast legacy-bekvämlighet |

---

## Roadmap (återstående luckor)

- Alpine/vmlinuz-bundling i Genesis ISO (startmenyn dokumenterar för närvarande manuell installationsväg)
- Nonce/tidsstämpel mot återuppspelning av röstkommandon
- Användargränssnitt för återkallande av `authorized_nodes`
