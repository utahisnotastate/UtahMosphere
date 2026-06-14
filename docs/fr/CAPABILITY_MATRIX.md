# Matrice des capacités

UtahMosphere OS **v27.0 Production Immutable** — ancres de confiance souveraines complètes.

---

## Points de terminaison HTTP API

| Point de terminaison | Méthode | Statut | Notes |
|----------------------|---------|--------|-------|
| `/health` | GET | **Implémenté** | Sonde de disponibilité + `build: omega-build-v27-production` + `attestation` |
| `/nonce` | GET | **Implémenté** | Émet un nonce frais pour commande vocale (fenêtre 30 s) |
| `/status` | GET | **Implémenté** | État UI, locataires, attestation, statistiques de basculement mempool |
| `/command` | POST | **Implémenté** | Intention vocale + signature nonce automatique (`voice_bridge_signed.py`) |
| `/admin/revoke-node` | POST | **Implémenté** | Révocation de nœud autorisée (racine uniquement) |
| `/app/unlock` | POST | **Implémenté** | Soumettre le paiement ; règlement avec basculement mempool |
| `/app/{name}` | GET | **Implémenté** | Porte Tycoon 402 + proxy UtahX vers le conteneur |
| `/app/{name}/{path}` | GET | **Implémenté** | Proxy sous-chemin vers le backend conteneur |
| `/s3/{bucket}/{key}` | GET | **Implémenté** | Lecture d'objet (NVMe local) |
| `/s3/{bucket}/{key}` | PUT/POST | **Implémenté** | Écriture d'objet ; en-têtes HMAC optionnels |
| `/s3/{bucket}/{prefix}*` | GET | **Implémenté** | Lister les objets |
| `/lambda/{fn}/invoke` | POST | **Implémenté** | Invocation de handler serverless |
| `/lambda/{fn}` | GET | **Implémenté** | Invocation GET avec événement vide |
| `/rds/write` | POST | **Implémenté** | Écriture clé-valeur |
| `/rds/read/{key}` | GET | **Implémenté** | Lecture clé-valeur |

---

## Sous-systèmes principaux

| Composant | Statut | Ce qui fonctionne aujourd'hui |
|-----------|--------|-------------------------------|
| **Golden Master (`utahmosphere_master.py`)** | **Implémenté** | Point d'entrée unifié |
| **Noyau (`utahmosphere_os.py`)** | **Implémenté** | Multiplexeur HTTP complet, registre, maillage |
| **Attestation matérielle (`attestation_guard.py`)** | **Implémenté** | Porte PCR0 TPM 2.0 dans bootstrap + health |
| **Basculement mempool (`tycoon_failover.py`)** | **Implémenté** | Basculement silencieux mempool US/EU/ASIE |
| **Voice Bridge signé (`voice_bridge_signed.py`)** | **Implémenté** | `GET /nonce` automatique + signature HMAC |
| **Proxy UtahX (`utahx_proxy.py`)** | **Implémenté** | Proxy HTTP en direct vers les ports conteneur |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Implémenté** | Serveurs HTTP par locataire sur 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Implémenté** | Mutation de handler validée AST + OTA |
| **S3 / Lambda / RDS** | **Implémenté** | Parité cloud complète |
| **Quantum Ledger** | **Implémenté** | Revendication biométrique + vérification |
| **Utah-Tycoon** | **Implémenté** | Basculement mempool + electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Implémenté** | Application de `authorized_nodes[]` |
| **Nonce-Guard (`nonce_guard.py`)** | **Implémenté** | Anti-rejeu 30 s pour commandes vocales |
| **UtahNetes + Swarm DHT** | **Implémenté** | Gossip signé + routage déterministe |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Implémenté** | Alpine vmlinuz + bootstrap compatible attestation |
| **Interface révocation Utah-Flux** | **Implémenté** | Panneau admin dans `flux_gui.py` |
| **Auto-Genesis / Bootstrap** | **Implémenté** | systemd + porte d'attestation |

---

## Commandes vocales

| Modèle de commande | Statut | Exemple |
|--------------------|--------|---------|
| Revendiquer le nœud | Implémenté | `"Claim node"` |
| Autoriser un nœud | Implémenté | `"authorize node <64-char-vibe-hash>"` |
| Déployer une application | Implémenté | `"deploy application my-app"` |
| Corriger une application | Implémenté | `"patch app my-app to add logging"` |
| Statut / grille | Implémenté | `"status grid"` |

**Voice Bridge v27.0** récupère automatiquement `GET /nonce` et signe chaque commande. Les clients manuels utilisent `voice_bridge_signed.get_signed_payload()`.

---

## Options de déploiement

| Méthode | Statut | Plateforme |
|---------|--------|------------|
| `python3 utahmosphere_master.py` | **Recommandé** | Toutes |
| `sudo bash bootstrap.sh` | **Recommandé prod** | Linux + TPM (saut optionnel) |
| `python3 genesis_iso_builder.py` | **Implémenté** | Génère `utah_genesis_v27.iso` |
| `./mk_iso.sh` | **Implémenté** | Wrapper Genesis ISO |
| `python3 voice_bridge.py` | **Implémenté** | Client vocal avec nonce automatique |

---

## Feuille de route

Tous les éléments de la feuille de route v26.0 et antérieurs sont **implémentés** en v27.0.

Améliorations futures :

- Vérification distante de citation d'attestation TPM (RA-TLS)
- Quatrième région mempool (Océanie)
- Liaison vibe-print au PCR TPM

Consultez la [Référence API](API_REFERENCE.md) et le [Guide du développeur](DEVELOPER_COOKBOOK.md) pour les détails d'implémentation actuels.
