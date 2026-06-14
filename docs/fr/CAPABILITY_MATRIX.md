# Matrice des capacités

UtahMosphere OS **v28.0 TPM-Hardened Attested** — chaîne de confiance souveraine complète.

---

## Points de terminaison HTTP API

| Point de terminaison | Méthode | Statut | Notes |
|----------------------|---------|--------|-------|
| `/health` | GET | **Implémenté** | `build: omega-build-v28-attested` + instantané d'attestation complet |
| `/attestation/quote` | GET | **Implémenté** | Citation TPM RA-TLS pour vérification des pairs du maillage |
| `/nonce` | GET | **Implémenté** | Nonce anti-rejeu pour commande vocale |
| `/status` | GET | **Implémenté** | Verrou TPM, RA-TLS, régions mempool Océanie |
| `/command` | POST | **Implémenté** | Voix + nonce + vérification vibe liée au TPM |
| `/admin/revoke-node` | POST | **Implémenté** | Révocation de nœud (racine uniquement) |
| `/app/unlock` | POST | **Implémenté** | Règlement avec basculement mempool 4 régions |
| `/app/{name}` | GET | **Implémenté** | Tycoon 402 + proxy UtahX |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Implémenté** | Parité cloud complète |

---

## Sous-systèmes principaux

| Composant | Statut | Ce qui fonctionne aujourd'hui |
|-----------|--------|-------------------------------|
| **TPM Locker (`tpm_lock.py`)** | **Implémenté** | Vibe-Print scellé au PCR0 via `tpm2_create` / `tpm2_unseal` |
| **RA-TLS (`ra_tls_attest.py`)** | **Implémenté** | Citation TPM sur gossip du maillage ; vérification des pairs avant sync |
| **Basculement mempool (`tycoon_failover.py`)** | **Implémenté** | Basculement US / EU / global / **Océanie** sur 4 régions |
| **Attestation matérielle (`attestation_guard.py`)** | **Implémenté** | Porte PCR0 au bootstrap |
| **Voice Bridge signé** | **Implémenté** | Nonce automatique + HMAC |
| **AuthGuard + Nonce-Guard** | **Implémenté** | Sécurité maillage + voix |
| **UtahNetes + Swarm DHT** | **Implémenté** | RA-TLS + gossip signé |
| **Genesis ISO v28** | **Implémenté** | `utah_genesis_v28.iso` |
| **Parité cloud complète** | **Implémenté** | S3, Lambda, RDS, UtahX, conteneurs |

---

## Déploiement

| Méthode | Statut |
|---------|--------|
| `python3 utahmosphere_master.py` | **Recommandé** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **ISO v28** |

## Variables d'environnement

| Variable | Défaut | Objectif |
|----------|--------|----------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Exiger le scellement TPM à la revendication |
| `UTAH_RA_TLS_ENFORCE` | `1` | Exiger les citations RA-TLS sur le maillage |
| `UTAH_MEMPOOL_NODES` | 4 valeurs par défaut | Remplacer la liste de basculement mempool |

## Feuille de route

Tous les éléments de la feuille de route v27.0 sont **implémentés** en v28.0.

À venir : épinglage CA RA-TLS distant, service de registre de citations matérielles.

Consultez la [Référence API](API_REFERENCE.md) et le [Guide du développeur](DEVELOPER_COOKBOOK.md).
