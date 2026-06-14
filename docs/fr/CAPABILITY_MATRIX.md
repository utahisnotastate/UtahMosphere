# Matrice des capacités

UtahMosphere OS **v26.0 Omega-Build FINAL** — implémentation complète de la feuille de route.

---

## Points de terminaison HTTP API

| Point de terminaison | Méthode | Statut | Notes |
|----------------------|---------|--------|-------|
| `/health` | GET | **Implémenté** | Sonde de disponibilité + `build: omega-build-v26-final` |
| `/nonce` | GET | **Implémenté** | Émet un nonce frais pour commande vocale (fenêtre 30 s) |
| `/status` | GET | **Implémenté** | État UI, locataires, statut de revendication, S3 root |
| `/command` | POST | **Implémenté** | Intention vocale + anti-rejeu nonce si revendiqué |
| `/admin/revoke-node` | POST | **Implémenté** | Révocation de nœud autorisée (racine uniquement) |
| `/app/unlock` | POST | **Implémenté** | Soumettre le paiement ; renvoie 202 en attente de règlement |
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
| **Proxy UtahX (`utahx_proxy.py`)** | **Implémenté** | Proxy HTTP en direct vers les ports conteneur |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Implémenté** | Serveurs HTTP par locataire sur 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Implémenté** | Mutation de handler validée AST + canal OTA |
| **S3 Mesh (`utah_s3_mesh.py`)** | **Implémenté** | Stockage d'objets local + HMAC |
| **Lambda Engine (`utah_lambda_engine.py`)** | **Implémenté** | Invocation de handler sans images |
| **RDS Ledger (`utah_rds_ledger.py`)** | **Implémenté** | Registre clé-valeur JSON |
| **Quantum Ledger** | **Implémenté** | Revendication biométrique + vérification |
| **Utah-Tycoon** | **Implémenté** | Règlement mempool/electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Implémenté** | Application de `authorized_nodes[]` pour voix + maillage |
| **Nonce-Guard (`nonce_guard.py`)** | **Implémenté** | Anti-rejeu 30 s pour commandes vocales |
| **Gossip UtahNetes** | **Implémenté** | Multidiffusion 5 s signée AuthGuard via `utah_mesh_engine.py` |
| **Global Swarm** | **Implémenté** | DHT déterministe + synchronisation de registre signée |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Implémenté** | ISO hybride Alpine vmlinuz/initramfs |
| **Interface révocation Utah-Flux (`ui_revocation.py`)** | **Implémenté** | Panneau admin dans `flux_gui.py` |
| **Interface Utah-Flux** | **Implémenté** | Tableau de bord Tkinter de statut + révocation |
| **Auto-Genesis (`genesis_deploy.py`)** | **Implémenté** | Orchestrateur multi-processus |
| **Bootstrap (`bootstrap.sh`)** | **Implémenté** | Installation bare-metal systemd |

---

## Commandes vocales

| Modèle de commande | Statut | Exemple |
|--------------------|--------|---------|
| Revendiquer le nœud | Implémenté | `"Claim node"` |
| Autoriser un nœud | **Implémenté** | `"authorize node <64-char-vibe-hash>"` |
| Déployer une application | Implémenté | `"deploy application my-app"` |
| Corriger une application | **Implémenté** | `"patch app my-app to add logging"` |
| Statut / grille | Implémenté | `"status grid"` |

**Après revendication :** inclure `nonce` + `command_signature` de `GET /nonce` sur chaque requête `/command`.

---

## Options de déploiement

| Méthode | Statut | Plateforme |
|---------|--------|------------|
| `python3 utahmosphere_master.py` | **Recommandé** | Toutes |
| `python3 utahmosphere_os.py` | Implémenté | Toutes |
| `python3 genesis_deploy.py` | Implémenté | Linux / dev |
| `sudo bash bootstrap.sh` | **Recommandé prod** | Linux systemd |
| `sudo bash setup.sh` | Implémenté | Alias de bootstrap |
| `python3 genesis_iso_builder.py` | **Implémenté** | Linux — génère `utah_genesis_v26.iso` |
| `./mk_iso.sh` | **Implémenté** | Wrapper pour le générateur Genesis ISO |
| `docker-compose up` | Optionnel | Commodité héritée uniquement |

---

## Feuille de route

Tous les éléments de la feuille de route v25.x sont **implémentés** en v26.0. Travaux futurs :

- Attestation matérielle pour l'autoinstall Genesis ISO
- Basculement mempool multi-région
- Signature automatique de nonce par le pont vocal

Consultez la [Référence API](API_REFERENCE.md) et le [Guide du développeur](DEVELOPER_COOKBOOK.md) pour les détails d'implémentation actuels.
