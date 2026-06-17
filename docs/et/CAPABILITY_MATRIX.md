# Võimekuste maatriks

UtahMosphere OS **v35.0 Omni-Desk** — suveräänne usaldusahel on täielik.

---

## HTTP API lõpp-punktid

| Lõpp-punkt | Meetod | Olek | Märkused |
|------------|--------|------|----------|
| `/desk/apps` | GET | **Rakendatud** | Genesis Suite register |
| `/desk/status` | GET | **Rakendatud** | Omni-Desk olek |
| `/desk/ui` | GET | **Rakendatud** | Holograafiline töölaud HTML |
| `/desk/intent` | POST | **Rakendatud** | Genesis rakenduse kavatsus |
| `/health` | GET | **Rakendatud** | `build: omega-build-v35-omni-desk` + täielik tõendamise hetktõmmis |
| `/attestation/quote` | GET | **Rakendatud** | RA-TLS TPM quote mesh-sõlmede kontrolliks |
| `/registry/quotes` | GET | **Rakendatud** | Globaalne riistvara tsitaadi register |
| `/registry/purge` | POST | **Rakendatud** | Kompromiteeritud riistvara eemaldamine |
| `/claw/void` | POST | **Rakendatud** | Epistemilise tühimiku käsitlemine |
| `/claw/status` | GET | **Rakendatud** | UtahClawi käivitaja olek |
| `/chrono/status` | GET | **Rakendatud** | Chrono-State olek |
| `/siphon/ghost-tune` | GET | **Rakendatud** | Ghost Tune binaar |
| `/omni/compile` | POST | **Rakendatud** | Agentliku kavatsuse kompileerimine |
| `/omni/status` | GET | **Rakendatud** | Omni-Mind statistika |
| `/omni/glass` | GET | **Rakendatud** | Agentide sündmuste logi |
| `/witness/status` | GET | **Rakendatud** | Mitmeregiooni tunnistajad |
| `/lazarus/status` | GET | **Rakendatud** | Lazarus kontrollpunkt |
| `/lazarus/restore` | POST | **Rakendatud** | Golden Master taastamine |
| `/quorum/consensus` | GET | **Rakendatud** | Enamuse kvoorumi register |
| `/dht/consensus` | GET | **Rakendatud** | DHT kuldne register |
| `/dht/challenge` | POST | **Rakendatud** | Parve tõendamise väljakutse |
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
| **Kvoorumi tunnistajad (`quorum_witness.py`)** | **Rakendatud** | USA/EL/Okeaania/Aasia vahekohtunikud |
| **Lazarus taastamine (`lazarus_restore.py`)** | **Rakendatud** | Golden Master + kexec aatomtaastamine |
| **Oleku-erinevus (`state_diff_engine.py`)** | **Rakendatud** | Põimunud mesh-deltad |
| **Kvoorumi mootor (`dht_consensus_engine.py`)** | **Rakendatud** | 51%+ häälte konsensus |
| **DHT kuldne register (`dht_quote_registry.py`)** | **Rakendatud** | Parve konsensuse kontroll |
| **PCR triiv (`drift_detector.py`)** | **Rakendatud** | Automaatne karantiin triivil |
| **Tsitaadi register (`quote_registry.py`)** | **Rakendatud** | Registreeri, eemalda, ühenda tsitaadid |
| **RA-TLS kaitse (`ra_tls_guard.py`)** | **Rakendatud** | CA kinnitamine; UtahX sisend |
| **RA-TLS (`ra_tls_attest.py`)** | **Rakendatud** | TPM quote mesh gossip-is; sõlme kontroll enne sünkroniseerimist |
| **Mempool varuühendus (`tycoon_failover.py`)** | **Rakendatud** | USA / EL / globaalne / **Okeaania** 4-piirkonniline varuühendus |
| **Riistvara tõendamine (`attestation_guard.py`)** | **Rakendatud** | Bootstrap PCR0 värav |
| **Voice Bridge Signed** | **Rakendatud** | Automaatne nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **Rakendatud** | Mesh + hääle turvalisus |
| **UtahNetes + Swarm DHT** | **Rakendatud** | RA-TLS + allkirjastatud gossip |
| **Genesis ISO v35** | **Rakendatud** | `utah_genesis_v35.iso` |
| **Täielik pilve pariteet** | **Rakendatud** | S3, Lambda, RDS, UtahX, konteinerid |

---

## Juurutamine

| Meetod | Olek |
|--------|------|
| `python3 utahmosphere_master.py` | **Soovitatav** |
| `sudo bash bootstrap.sh` | **Tootmine** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v35 ISO** |

## Keskkond

| Muutuja | Vaikimisi | Eesmärk |
|---------|-----------|---------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Nõua TPM pitst claim-il |
| `UTAH_QUORUM_ENFORCE` | `1` | Enamuse kvoorum |
| `UTAH_WITNESS_ENFORCE` | `1` | Mitmeregiooni tunnistajad |
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Automaatne taastamine |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec Lazarus taastamine |
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Põimunud delta sünk |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | Nõua RA-TLS quote mesh-is |
| `UTAH_MEMPOOL_NODES` | 4 vaikimisi | Mempool varuühenduse loendi alistamine |

| `UTAH_OMNI_DESK_ENFORCE` | `1` | Omni-Desk |
| `UTAH_CLAW_ENFORCE` | `1` | UtahClaw ambient runner |
| `UTAH_CHRONO_ENFORCE` | `1` | Chrono-State tagasikerimine |
| `UTAH_OMNI_GLASS_STREAM` | `1` | Omni-Glass SSE voog |
| `UTAH_OMNI_ENFORCE` | `1` | Omni-Compiler |

## Teekaart

Kõik v28.0 teekaardi punktid on v34.0-s **rakendatud**.

Tulevik: kaug-RA-TLS CA kinnitamine, riistvara quote registriteenus.

Vaata [API viidet](API_REFERENCE.md) ja [Arendaja retseptiraamatut](DEVELOPER_COOKBOOK.md).
