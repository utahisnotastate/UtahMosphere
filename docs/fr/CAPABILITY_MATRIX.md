# Matrice des capacités

UtahMosphere OS **v32.0 Infrastructure d'attestation à distance** — ancres de confiance souveraines : registre global des citations matérielles, épinglage CA RA-TLS, liaison biométrique au TPM.

---

## Points de terminaison HTTP API

| Point de terminaison | Méthode | Statut | Notes |
|----------------------|---------|--------|-------|
| `/health` | GET | **Implémenté** | `build: omega-build-v32-lazarus-self-healing` + instantané d'attestation complet |
| `/attestation/quote` | GET | **Implémenté** | Citation TPM RA-TLS + `hardware_id` |
| `/registry/quotes` | GET | **Implémenté** | Export du registre global des citations matérielles |
| `/registry/purge` | POST | **Implémenté** | Purger le matériel compromis |
| `/witness/status` | GET | **Implémenté** | Témoins multi-régions |
| `/lazarus/status` | GET | **Implémenté** | Point de contrôle Lazarus |
| `/lazarus/restore` | POST | **Implémenté** | Restauration Golden Master |
| `/quorum/consensus` | GET | **Implémenté** | Registre de votes quorum |
| `/dht/consensus` | GET | **Implémenté** | Registre doré DHT |
| `/dht/challenge` | POST | **Implémenté** | Défi d'attestation de l'essaim |
| `/nonce` | GET | **Implémenté** | Nonce anti-rejeu pour commande vocale |
| `/status` | GET | **Implémenté** | Verrou TPM, garde RA-TLS, statistiques du registre de citations |
| `/command` | POST | **Implémenté** | Voix + nonce + vibe liée au TPM + envoi au registre lors de la revendication |
| `/admin/revoke-node` | POST | **Implémenté** | Révocation de nœud (racine uniquement) |
| `/app/unlock` | POST | **Implémenté** | Règlement avec basculement mempool 4 régions |
| `/app/{name}` | GET | **Implémenté** | Tycoon 402 + proxy UtahX avec attestation RA-TLS à l'ingress |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Implémenté** | Parité cloud complète |

---

## Sous-systèmes principaux

| Composant | Statut | Ce qui fonctionne aujourd'hui |
|-----------|--------|-------------------------------|
| **Registre de citations (`quote_registry.py`)** | **Implémenté** | Enregistrer, purger, fusionner, persister les citations matérielles |
| **Garde RA-TLS (`ra_tls_guard.py`)** | **Implémenté** | Épinglage CA ; ingress UtahX ; vérification OID X.509 |
| **RA-TLS (`ra_tls_attest.py`)** | **Implémenté** | Citation TPM sur gossip du maillage ; réplication du registre |
| **TPM Locker (`tpm_lock.py`)** | **Implémenté** | Vibe-Print scellé au PCR0 via `tpm2_create` / `tpm2_unseal` |
| **Basculement mempool (`tycoon_failover.py`)** | **Implémenté** | Basculement US / EU / global / **Océanie** sur 4 régions |
| **Attestation matérielle (`attestation_guard.py`)** | **Implémenté** | Porte PCR0 au bootstrap |
| **Voice Bridge signé** | **Implémenté** | Nonce automatique + HMAC |
| **AuthGuard + Nonce-Guard** | **Implémenté** | Sécurité maillage + voix |
| **UtahNetes + Swarm DHT** | **Implémenté** | RA-TLS + gossip signé + fusion du registre |
| **Genesis ISO v32** | **Implémenté** | `utah_genesis_v32.iso` |
| **Parité cloud complète** | **Implémenté** | S3, Lambda, RDS, UtahX, conteneurs |

---

## Déploiement

| Méthode | Statut |
|---------|--------|
| `python3 utahmosphere_master.py` | **Recommandé** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **v32 ISO** |

## Variables d'environnement

| Variable | Défaut | Objectif |
|----------|--------|----------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Exiger le scellement TPM à la revendication |
| `UTAH_RA_TLS_ENFORCE` | `1` | Exiger les citations RA-TLS sur le maillage |
| `UTAH_QUORUM_ENFORCE` | `1` | Quorum majoritaire |
| `UTAH_WITNESS_ENFORCE` | `1` | Témoins multi-régions |
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Restauration automatique |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | kexec Lazarus |
| `UTAH_STATE_DIFF_ENFORCE` | `1` | Sync delta entrelacée |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | Épinglage CA à l'ingress UtahX |
| `UTAH_MEMPOOL_NODES` | 4 valeurs par défaut | Remplacer la liste de basculement mempool |

## Feuille de route

Tous les éléments de la feuille de route v28.0 sont **implémentés** en v32.0 (épinglage CA RA-TLS distant, registre des citations matérielles).

À venir : fédération DHT des citations matérielles, détection automatisée de la dérive PCR.

Consultez le [Registre des citations](QUOTE_REGISTRY.md), l'[Attestation](ATTESTATION.md), le [RA-TLS](RA_TLS.md), le [Genesis ISO](GENESIS_ISO.md) et le [Journal des modifications](CHANGELOG.md).
