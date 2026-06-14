# Võimekuste maatriks

UtahMosphere OS **v32.0 Lazarus Self-Healing** — suveräänne usaldusahel on täielik.

---

## HTTP API lõpp-punktid

| Lõpp-punkt | Meetod | Olek | Märkused |
|------------|--------|------|----------|
| `/health` | GET | **Rakendatud** | `build: omega-build-v32-lazarus-self-healing` + täielik tõendamise hetktõmmis |
| `/attestation/quote` | GET |
| `/registry/quotes` | GET | **Implemented** | Global hardware quote registry |
| `/registry/purge` | POST |
| `/witness/status` | GET | **Rakendatud** | Mitmeregiooni tunnistajad |
| `/lazarus/status` | GET | **Rakendatud** | Lazarus kontrollpunkt |
| `/lazarus/restore` | POST | **Rakendatud** | Golden Master taastamine |
| `/quorum/consensus` | GET | **Implemented** | Majority-quorum ledger |
| `/dht/consensus` | GET | **Implemented** | DHT golden ledger |
| `/dht/challenge` | POST | **Implemented** | Swarm attestation challenge | **Implemented** | Purge compromised hardware | **Rakendatud** | RA-TLS TPM quote mesh-sõlmede kontrolliks |
| `/nonce` | GET | **Rakendatud** | Häälkäsu korduskasutuse vastu nonce |
| `/status` | GET | **Rakendatud** | TPM lock, RA-TLS, Okeaania mempool piirkonnad |
| `/command` | POST | **Rakendatud** | Hääl + nonce + TPM-iga seotud vibe kontroll |
| `/admin/revoke-node` | POST | **Rakendatud** | Ainult juur — sõlme tühistamine |
| `/app/unlock` | POST | **Rakendatud** | 4-piirkonniline mempool varuühenduse arveldus |
| `/app/{name}` | GET | **Rakendatud** | Tycoon 402 + UtahX proksi |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Rakendatud** | Täielik pilve pariteet |

---

## Tuuma alamsüsteemid

| Komponent | Olek | Mis täna töötab |
|-----------|------|-----------------|
| **TPM Locker (`tpm_lock.py`)** | **Rakendatud** | Vibe-Print pitstatud PCR0-sse `tpm2_create` / `tpm2_unseal` kaudu |
| **Kvoorumi tunnistajad (`quorum_witness.py`)** | **Rakendatud** | USA/EL/Okeaania vahekohtunikud |
| **Lazarus taastamine (`lazarus_restore.py`)** | **Rakendatud** | Automaatne taastamine pärast karantiini |
| **Oleku-erinevus (`state_diff_engine.py`)** | **Rakendatud** | Põimunud mesh-deltad |
| **Quorum Engine (`dht_consensus_engine.py`)** | **Implemented** | 51%+ vote consensus |
| **DHT Golden Registry (`dht_quote_registry.py`)** | **Implemented** | Swarm consensus verify |
| **PCR Drift (`drift_detector.py`)** | **Implemented** | Auto-quarantine on drift |
| **Quote Registry (`quote_registry.py`)** | **Implemented** | Register, purge, merge hardware quotes |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Implemented** | CA pinning; UtahX ingress |
| **RA-TLS (`ra_tls_attest.py`)** | **Rakendatud** | TPM quote mesh gossip-is; sõlme kontroll enne sünkroniseerimist |
| **Mempool varuühendus (`tycoon_failover.py`)** | **Rakendatud** | USA / EL / globaalne / **Okeaania** 4-piirkonniline varuühendus |
| **Riistvara tõendamine (`attestation_guard.py`)** | **Rakendatud** | Bootstrap PCR0 värav |
| **Voice Bridge Signed** | **Rakendatud** | Automaatne nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Rakendatud** | Mesh + hääle turvalisus |
| **UtahNetes + Swarm DHT** | **Rakendatud** | RA-TLS + allkirjastatud gossip |
| **Genesis ISO v32** | **Rakendatud** | `utah_genesis_v32.iso` |
| **Täielik pilve pariteet** | **Rakendatud** | S3, Lambda, RDS, UtahX, konteinerid |

---

## Juurutamine

| Meetod | Olek |
|--------|------|
| `python3 utahmosphere_master.py` | **Soovitatav** |
| `sudo bash bootstrap.sh` | **Tootmine** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v32 ISO** |

## Keskkond

| Muutuja | Vaikimisi | Eesmärk |
|---------|-----------|---------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Nõua TPM pitst claim-il |
| `UTAH_QUORUM_ENFORCE` | `1` | Majority quorum |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | Nõua RA-TLS quote mesh-is |
| `UTAH_MEMPOOL_NODES` | 4 vaikimisi | Mempool varuühenduse loendi alistamine |

## Teekaart

Kõik v28.0 teekaardi punktid on v32.0-s **rakendatud**.

Tulevik: kaug-RA-TLS CA kinnitamine, riistvara quote registriteenus.

Vaata [API viidet](API_REFERENCE.md) ja [Arendaja retseptiraamatut](DEVELOPER_COOKBOOK.md).
