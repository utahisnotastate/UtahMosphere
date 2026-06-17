# Ominaisuusmatriisi

UtahMosphere OS **v34.0 Etätodentamisinfra** — suvereenit luottamusankkurit: globaali laitteisto quote -rekisteri, RA-TLS CA -kiinnitys, biometrinen TPM-sidonta.

---

## HTTP API -päätepisteet

| Päätepiste | Metodi | Tila | Huomiot |
|------------|--------|------|---------|
| `/desk/apps` | GET | **Toteutettu** | Genesis Suite -rekisteri |
| `/desk/status` | GET | **Toteutettu** | Omni-Desk-tila |
| `/desk/ui` | GET | **Toteutettu** | Holografinen työpöytä HTML |
| `/desk/intent` | POST | **Toteutettu** | Genesis-sovelluksen intent |
| `/health` | GET | **Toteutettu** | `build: omega-build-v35-omni-desk` + täydellinen todentamistilannekuva |
| `/attestation/quote` | GET | **Toteutettu** | RA-TLS TPM quote + `hardware_id` |
| `/registry/quotes` | GET | **Toteutettu** | Globaalin laitteisto quote -rekisterin vienti |
| `/registry/purge` | POST | **Toteutettu** | Poista vaarantunut laitteisto |
| `/claw/void` | POST | **Toteutettu** | Epistemisen tyhjiön käsittely |
| `/claw/status` | GET | **Toteutettu** | UtahClaw-käynnistimen tilastot |
| `/chrono/status` | GET | **Toteutettu** | Chrono-State-tila |
| `/siphon/ghost-tune` | GET | **Toteutettu** | Ghost Tune -binääri |
| `/omni/compile` | POST | **Toteutettu** | Agenttisen intentin käännös |
| `/omni/status` | GET | **Toteutettu** | Omni-Mind-tilastot |
| `/omni/glass` | GET | **Toteutettu** | Agenttisten tapahtumien loki |
| `/witness/status` | GET | **Toteutettu** | Monialueiset todistajat |
| `/lazarus/status` | GET | **Toteutettu** | Lazarus-tarkistuspiste |
| `/lazarus/restore` | POST | **Toteutettu** | Golden Master -palautus |
| `/quorum/consensus` | GET | **Toteutettu** | Enemmistökvoorumin kirjanpito |
| `/dht/consensus` | GET | **Toteutettu** | DHT kultainen kirjanpito |
| `/dht/challenge` | POST | **Toteutettu** | Parven todentamishaaste |
| `/nonce` | GET | **Toteutettu** | Äänikomennon uudelleentoiston eston nonce |
| `/status` | GET | **Toteutettu** | TPM lock, RA-TLS guard, quote-rekisterin tilastot |
| `/command` | POST | **Toteutettu** | Ääni + nonce + TPM-sidottu vibe + rekisterin push claimissä |
| `/admin/revoke-node` | POST | **Toteutettu** | Vain juuri — solmun peruutus |
| `/app/unlock` | POST | **Toteutettu** | 4 alueen mempool-varajärjestelmän selvitys |
| `/app/{name}` | GET | **Toteutettu** | Tycoon 402 + UtahX-välitys RA-TLS-sisääntulolla |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Toteutettu** | Täysi pilvipariteetti |

---

## Ydinalijärjestelmät

| Komponentti | Tila | Mitä toimii tänään |
|-------------|------|-------------------|
| **Quote-rekisteri (`quote_registry.py`)** | **Toteutettu** | Laitteisto quote -rekisteröinti, poisto, yhdistäminen, pysyvyys |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Toteutettu** | CA-kiinnitys; UtahX-sisääntulo; X.509 OID -vahvistus |
| **RA-TLS (`ra_tls_attest.py`)** | **Toteutettu** | TPM quote mesh-gossipissa; rekisterin replikointi |
| **TPM Locker (`tpm_lock.py`)** | **Toteutettu** | Vibe-Print sinetöity PCR0:een `tpm2_create` / `tpm2_unseal` -kautta |
| **Mempool-varajärjestelmä (`tycoon_failover.py`)** | **Toteutettu** | US / EU / global / **Oseania** 4 alueen varajärjestelmä |
| **Laitteiston todentaminen (`attestation_guard.py`)** | **Toteutettu** | Bootstrap PCR0-portti |
| **Voice Bridge Signed** | **Toteutettu** | Automaattinen nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Toteutettu** | Mesh + ääniturvallisuus |
| **UtahNetes + Swarm DHT** | **Toteutettu** | RA-TLS + allekirjoitettu gossip + rekisterin yhdistäminen |
| **Genesis ISO v35** | **Toteutettu** | `utah_genesis_v35.iso` |
| **Täysi pilvipariteetti** | **Toteutettu** | S3, Lambda, RDS, UtahX, kontit |

---

## Käyttöönotto

| Menetelmä | Tila |
|-----------|------|
| `python3 utahmosphere_master.py` | **Suositeltu** |
| `sudo bash bootstrap.sh` | **Tuotanto** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v35 ISO** |

## Ympäristö

| Muuttuja | Oletus | Tarkoitus |
|----------|--------|-----------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Vaadi TPM-sinetti claimissä |
| `UTAH_RA_TLS_ENFORCE` | `1` | Vaadi RA-TLS quote meshissä |
| `UTAH_QUORUM_ENFORCE` | `1` | Enemmistökvoorum |
| `UTAH_WITNESS_ENFORCE` | `1` | Monialueiset todistajat |
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Automaattinen palautus |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec Lazarus-palautus |
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Kietoutunut deltasynk |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX-sisääntulon CA-kiinnitys |
| `UTAH_MEMPOOL_NODES` | 4 oletusta | Korvaa mempool-varajärjestelmän lista |

## Tiekartta

Kaikki v28.0:n tiekartan kohdat on **toteutettu** v34.0:ssa (etä-RA-TLS CA -kiinnitys, laitteisto quote -rekisteri).

Tulevaisuus: laitteisto quote -DHT-federointi, automaattinen PCR-driftin tunnistus.

Katso [Quote-rekisteri](QUOTE_REGISTRY.md), [Todentaminen](ATTESTATION.md), [RA-TLS](RA_TLS.md), [Genesis ISO](GENESIS_ISO.md) ja [Muutosloki](CHANGELOG.md).
