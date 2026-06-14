# Kapacitetsmatris

UtahMosphere OS **v30.0 DHT-Federated Attestation** — suverän förtroendekedja komplett.

---

## HTTP API-endpoints

| Endpoint | Metod | Status | Noteringar |
|----------|-------|--------|------------|
| `/health` | GET | **Implementerat** | `build: omega-build-v30-federated-attested` + fullständig attesteringsögonblicksbild |
| `/attestation/quote` | GET |
| `/registry/quotes` | GET | **Implemented** | Global hardware quote registry |
| `/registry/purge` | POST |
| `/dht/consensus` | GET | **Implemented** | DHT golden ledger |
| `/dht/challenge` | POST | **Implemented** | Swarm attestation challenge | **Implemented** | Purge compromised hardware | **Implementerat** | RA-TLS TPM quote för mesh-nodverifiering |
| `/nonce` | GET | **Implementerat** | Nonce mot återuppspelning av röstkommandon |
| `/status` | GET | **Implementerat** | TPM lock, RA-TLS, Oceanien mempool-regioner |
| `/command` | POST | **Implementerat** | Röst + nonce + TPM-bunden vibe-verifiering |
| `/admin/revoke-node` | POST | **Implementerat** | Endast root — nodåterkallande |
| `/app/unlock` | POST | **Implementerat** | Avveckling via mempool-failover i 4 regioner |
| `/app/{name}` | GET | **Implementerat** | Tycoon 402 + UtahX-proxy |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Implementerat** | Full molnparitet |

---

## Kärndelsystem

| Komponent | Status | Vad som fungerar idag |
|-----------|--------|----------------------|
| **TPM Locker (`tpm_lock.py`)** | **Implementerat** | Vibe-Print förseglad till PCR0 via `tpm2_create` / `tpm2_unseal` |
| **DHT Golden Registry (`dht_quote_registry.py`)** | **Implemented** | Swarm consensus verify |
| **PCR Drift (`drift_detector.py`)** | **Implemented** | Auto-quarantine on drift |
| **Quote Registry (`quote_registry.py`)** | **Implemented** | Register, purge, merge hardware quotes |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Implemented** | CA pinning; UtahX ingress |
| **RA-TLS (`ra_tls_attest.py`)** | **Implementerat** | TPM quote i mesh-gossip; nodverifiering före synk |
| **Mempool-failover (`tycoon_failover.py`)** | **Implementerat** | US / EU / global / **Oceanien** failover i 4 regioner |
| **Hårdvaruattestering (`attestation_guard.py`)** | **Implementerat** | Bootstrap PCR0-grind |
| **Voice Bridge Signed** | **Implementerat** | Automatiskt nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Implementerat** | Mesh + röstsäkerhet |
| **UtahNetes + Swarm DHT** | **Implementerat** | RA-TLS + signerad gossip |
| **Genesis ISO v30** | **Implementerat** | `utah_genesis_v30.iso` |
| **Full molnparitet** | **Implementerat** | S3, Lambda, RDS, UtahX, containers |

---

## Driftsättning

| Metod | Status |
|-------|--------|
| `python3 utahmosphere_master.py` | **Rekommenderas** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v30 ISO** |

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Kräv TPM-försegling vid claim |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | Kräv RA-TLS quote i mesh |
| `UTAH_MEMPOOL_NODES` | 4 standardvärden | Åsidosätt mempool-failoverlista |

## Roadmap

Alla roadmap-poster för v28.0 är **implementerade** i v30.0.

Framtid: fjärr-RA-TLS CA-pinning, tjänst för hardware quote-register.

Se [API-referens](API_REFERENCE.md) och [Utvecklarkokbok](DEVELOPER_COOKBOOK.md).
