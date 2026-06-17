# Kapacitetsmatris

UtahMosphere OS **v33.0 Omni-Mind** — suverän förtroendekedja komplett.

---

## HTTP API-endpoints

| Endpoint | Metod | Status | Noteringar |
|----------|-------|--------|------------|
| `/health` | GET | **Implementerat** | `build: omega-build-v33-omni-mind` + fullständig attesteringsögonblicksbild |
| `/attestation/quote` | GET | **Implementerat** | RA-TLS TPM quote för mesh-nodverifiering |
| `/registry/quotes` | GET | **Implementerat** | Globalt register för hårdvarucitat |
| `/registry/purge` | POST | **Implementerat** | Rensa komprometterad hårdvara |
| `/omni/compile` | POST | **Implemented** | Agentic intent compile |
| `/omni/status` | GET | **Implemented** | Omni-Mind stats |
| `/omni/glass` | GET | **Implemented** | Agentic event log |
| `/witness/status` | GET | **Implementerat** | Flerregions vittnen |
| `/lazarus/status` | GET | **Implementerat** | Lazarus-kontrollpunkt |
| `/lazarus/restore` | POST | **Implementerat** | Golden Master-återställning |
| `/quorum/consensus` | GET | **Implementerat** | Majoritetskvorum-ledger |
| `/dht/consensus` | GET | **Implementerat** | DHT gyllene ledger |
| `/dht/challenge` | POST | **Implementerat** | Svärm-attesteringsutmaning |
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
| **Kvorumvittnen (`quorum_witness.py`)** | **Implementerat** | USA/EU/Oceanien/Asien-domare |
| **Lazarus-återställning (`lazarus_restore.py`)** | **Implementerat** | Golden Master + atomisk kexec-återställning |
| **Tillståndsdiff (`state_diff_engine.py`)** | **Implementerat** | Entanglade mesh-deltor |
| **Quorum Engine (`dht_consensus_engine.py`)** | **Implemented** | 51%+ vote consensus |
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
| **Genesis ISO v33** | **Implementerat** | `utah_genesis_v33.iso` |
| **Full molnparitet** | **Implementerat** | S3, Lambda, RDS, UtahX, containers |

---

## Driftsättning

| Metod | Status |
|-------|--------|
| `python3 utahmosphere_master.py` | **Rekommenderas** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v32 ISO** |

## Miljö

| Variabel | Standard | Syfte |
|----------|----------|-------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Kräv TPM-försegling vid claim |
| `UTAH_QUORUM_ENFORCE` | `1` | Majoritetskvorum |
| `UTAH_WITNESS_ENFORCE` | `1` | Flerregions vittnen |
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Autoåterställning |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec Lazarus |
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Entanglad deltasynk |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | Kräv RA-TLS quote i mesh |
| `UTAH_MEMPOOL_NODES` | 4 standardvärden | Åsidosätt mempool-failoverlista |

## Roadmap

Alla roadmap-poster för v28.0 är **implementerade** i v33.0.

Framtid: fjärr-RA-TLS CA-pinning, tjänst för hardware quote-register.

Se [API-referens](API_REFERENCE.md) och [Utvecklarkokbok](DEVELOPER_COOKBOOK.md).
