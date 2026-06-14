# Ominaisuusmatriisi

UtahMosphere OS **v28.0 TPM-Hardened Attested** — suvereeni luottamusketju on valmis.

---

## HTTP API -päätepisteet

| Päätepiste | Metodi | Tila | Huomiot |
|------------|--------|------|---------|
| `/health` | GET | **Toteutettu** | `build: omega-build-v28-attested` + täydellinen todentamistilannekuva |
| `/attestation/quote` | GET | **Toteutettu** | RA-TLS TPM quote mesh-solmujen vahvistukseen |
| `/nonce` | GET | **Toteutettu** | Äänikomennon uudelleentoiston eston nonce |
| `/status` | GET | **Toteutettu** | TPM lock, RA-TLS, Oseanian mempool-alueet |
| `/command` | POST | **Toteutettu** | Ääni + nonce + TPM-sidottu vibe-vahvistus |
| `/admin/revoke-node` | POST | **Toteutettu** | Vain juuri — solmun peruutus |
| `/app/unlock` | POST | **Toteutettu** | 4 alueen mempool-varajärjestelmän selvitys |
| `/app/{name}` | GET | **Toteutettu** | Tycoon 402 + UtahX-välitys |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Toteutettu** | Täysi pilvipariteetti |

---

## Ydinalijärjestelmät

| Komponentti | Tila | Mitä toimii tänään |
|-------------|------|-------------------|
| **TPM Locker (`tpm_lock.py`)** | **Toteutettu** | Vibe-Print sinetöity PCR0:een `tpm2_create` / `tpm2_unseal` -kautta |
| **RA-TLS (`ra_tls_attest.py`)** | **Toteutettu** | TPM quote mesh-gossipissa; solmun vahvistus ennen synkronointia |
| **Mempool-varajärjestelmä (`tycoon_failover.py`)** | **Toteutettu** | US / EU / global / **Oseania** 4 alueen varajärjestelmä |
| **Laitteiston todentaminen (`attestation_guard.py`)** | **Toteutettu** | Bootstrap PCR0-portti |
| **Voice Bridge Signed** | **Toteutettu** | Automaattinen nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Toteutettu** | Mesh + ääniturvallisuus |
| **UtahNetes + Swarm DHT** | **Toteutettu** | RA-TLS + allekirjoitettu gossip |
| **Genesis ISO v28** | **Toteutettu** | `utah_genesis_v28.iso` |
| **Täysi pilvipariteetti** | **Toteutettu** | S3, Lambda, RDS, UtahX, kontit |

---

## Käyttöönotto

| Menetelmä | Tila |
|-----------|------|
| `python3 utahmosphere_master.py` | **Suositeltu** |
| `sudo bash bootstrap.sh` | **Tuotanto** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v28 ISO** |

## Ympäristö

| Muuttuja | Oletus | Tarkoitus |
|----------|--------|-----------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Vaadi TPM-sinetti claimissä |
| `UTAH_RA_TLS_ENFORCE` | `1` | Vaadi RA-TLS quote meshissä |
| `UTAH_MEMPOOL_NODES` | 4 oletusta | Korvaa mempool-varajärjestelmän lista |

## Tiekartta

Kaikki v27.0:n tiekartan kohdat on **toteutettu** v28.0:ssa.

Tulevaisuus: etä-RA-TLS CA -kiinnitys, laitteisto quote -rekisteripalvelu.

Katso [API-viite](API_REFERENCE.md) ja [Kehittäjän keittokirja](DEVELOPER_COOKBOOK.md).
