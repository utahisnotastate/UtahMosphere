# Kapacitetsmatris

UtahMosphere OS **v27.0 Production Immutable** — suveräna förtroendeankare är kompletta.

---

## HTTP API-endpoints

| Endpoint | Metod | Status | Noteringar |
|----------|-------|--------|------------|
| `/health` | GET | **Implementerat** | Liveness-probe + `build: omega-build-v27-production` + `attestation` |
| `/nonce` | GET | **Implementerat** | Utfärdar färskt nonce för röstkommando (30s fönster) |
| `/status` | GET | **Implementerat** | UI-tillstånd, tenants, attestering, mempool-failover-statistik |
| `/command` | POST | **Implementerat** | Röstintent + automatisk nonce-signering (`voice_bridge_signed.py`) |
| `/admin/revoke-node` | POST | **Implementerat** | Endast root — återkallande av delegerad nod |
| `/app/unlock` | POST | **Implementerat** | Skicka betalning; mempool-failover-avveckling |
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
| **Hårdvaruattestering (`attestation_guard.py`)** | **Implementerat** | TPM 2.0 PCR0-grind i bootstrap + health |
| **Mempool-failover (`tycoon_failover.py`)** | **Implementerat** | Tyst failover US/EU/ASIA mempool |
| **Voice Bridge Signed (`voice_bridge_signed.py`)** | **Implementerat** | Auto `GET /nonce` + HMAC-signering |
| **UtahX Proxy (`utahx_proxy.py`)** | **Implementerat** | Live HTTP-proxy till containerportar |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Implementerat** | HTTP-servrar per tenant på 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Implementerat** | AST-validerad handler-mutation + OTA |
| **S3 / Lambda / RDS** | **Implementerat** | Full molnparitet |
| **Quantum Ledger** | **Implementerat** | Biometrisk claim + verifiering |
| **Utah-Tycoon** | **Implementerat** | Failover mempool + electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Implementerat** | `authorized_nodes[]`-tillämpning |
| **Nonce-Guard (`nonce_guard.py`)** | **Implementerat** | 30s anti-replay för röstkommandon |
| **UtahNetes + Swarm DHT** | **Implementerat** | Signerad gossip + deterministisk routing |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Implementerat** | Alpine vmlinuz + TPM-medveten bootstrap |
| **Utah-Flux återkallande UI** | **Implementerat** | Adminpanel i `flux_gui.py` |
| **Auto-Genesis / Bootstrap** | **Implementerat** | systemd + attesteringsgrind |

---

## Röstkommandon

| Kommandomönster | Status | Exempel |
|-----------------|--------|---------|
| Claim node | Implementerat | `"Claim node"` |
| Authorize node | Implementerat | `"authorize node <64-char-vibe-hash>"` |
| Deploy application | Implementerat | `"deploy application my-app"` |
| Patch application | Implementerat | `"patch app my-app to add logging"` |
| Status / grid | Implementerat | `"status grid"` |

**Voice Bridge v27.0** hämtar automatiskt `GET /nonce` och signerar varje kommando. Manuella klienter använder `voice_bridge_signed.get_signed_payload()`.

---

## Driftsättningsalternativ

| Metod | Status | Plattform |
|-------|--------|-----------|
| `python3 utahmosphere_master.py` | **Rekommenderas** | Alla |
| `sudo bash bootstrap.sh` | **Rekommenderas prod** | Linux + TPM (valfritt hoppa över) |
| `python3 genesis_iso_builder.py` | **Implementerat** | Bygger `utah_genesis_v27.iso` |
| `./mk_iso.sh` | **Implementerat** | Omslag för Genesis ISO-byggare |
| `python3 voice_bridge.py` | **Implementerat** | Röstklient med automatisk nonce-signering |

---

## Roadmap

Alla roadmap-poster för v26.0 och tidigare är **implementerade** i v27.0.

Framtida förbättringar:

- Fjärrverifiering av TPM quote-attestering (RA-TLS)
- Fjärde mempool-region (Oceanien)
- Hårdvarubunden vibe-print-koppling till TPM PCR

Se [API-referens](API_REFERENCE.md) och [Utvecklarkokbok](DEVELOPER_COOKBOOK.md).
