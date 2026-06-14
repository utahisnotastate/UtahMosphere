# Kapacitetsmatris

UtahMosphere OS **v29.0 Remote Attestation Infrastructure** — suverän förtroendekedja komplett.

---

## HTTP API-endpoints

| Endpoint | Metod | Status | Noteringar |
|----------|-------|--------|------------|
| `/health` | GET | **Implementerat** | `build: omega-build-v29-remote-attested` + fullständig attesteringsögonblicksbild |
| `/attestation/quote` | GET |
| `/registry/quotes` | GET | **Implemented** | Global hardware quote registry |
| `/registry/purge` | POST | **Implemented** | Purge compromised hardware | **Implementerat** | RA-TLS TPM quote för mesh-nodverifiering |
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
| **Quote Registry (`quote_registry.py`)** | **Implemented** | Register, purge, merge hardware quotes |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Implemented** | CA pinning; UtahX ingress |
| **RA-TLS (`ra_tls_attest.py`)** | **Implementerat** | TPM quote i mesh-gossip; nodverifiering före synk |
| **Mempool-failover (`tycoon_failover.py`)** | **Implementerat** | US / EU / global / **Oceanien** failover i 4 regioner |
| **Hårdvaruattestering (`attestation_guard.py`)** | **Implementerat** | Bootstrap PCR0-grind |
| **Voice Bridge Signed** | **Implementerat** | Automatiskt nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Implementerat** | Mesh + röstsäkerhet |
| **UtahNetes + Swarm DHT** | **Implementerat** | RA-TLS + signerad gossip |
| **Genesis ISO v29** | **Implementerat** | `utah_genesis_v29.iso` |
| **Full molnparitet** | **Implementerat** | S3, Lambda, RDS, UtahX, containers |

---

## Driftsättning

| Metod | Status |
|-------|--------|
| `python3 utahmosphere_master.py` | **Rekommenderas** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v29 ISO** |

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Kräv TPM-försegling vid claim |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | Kräv RA-TLS quote i mesh |
| `UTAH_MEMPOOL_NODES` | 4 standardvärden | Åsidosätt mempool-failoverlista |

## Roadmap

Alla roadmap-poster för v28.0 är **implementerade** i v29.0.

Framtid: fjärr-RA-TLS CA-pinning, tjänst för hardware quote-register.

Se [API-referens](API_REFERENCE.md) och [Utvecklarkokbok](DEVELOPER_COOKBOOK.md).
