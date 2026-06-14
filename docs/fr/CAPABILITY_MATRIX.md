# Matrice des capacités

UtahMosphere OS **v25.1 Migration Ready** — état d'implémentation au titre d'Omega-Build.

---

## Points de terminaison HTTP API

| Point de terminaison | Méthode | Statut | Notes |
|----------------------|---------|--------|-------|
| `/health` | GET | **Implémenté** | Sonde de disponibilité + `build: golden-master-v25.1` |
| `/status` | GET | **Implémenté** | État UI, locataires, statut de revendication, S3 root |
| `/command` | POST | **Implémenté** | Exécution d'intention vocale |
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
| **Quantum Ledger** | Implémenté | Revendication biométrique + vérification |
| **Utah-Tycoon** | **Implémenté** | Règlement mempool/electrum (`tycoon_settlement.py`), `POST /app/unlock`, porte HTTP 402 |
| **Gossip UtahNetes** | **Implémenté** | Multidiffusion 5 s signée AuthGuard via `utah_mesh_engine.py` |
| **Global Swarm** | **Implémenté** | DHT déterministe + synchronisation de registre signée |
| **AuthGuard (`ledger_auth.py`)** | **Implémenté** | Application de `authorized_nodes[]` pour voix + maillage |
| **Genesis ISO (`mk_iso.sh`)** | **Implémenté** | Générateur d'installateur flash UEFI/hybride |
| **Interface Utah-Flux** | Implémenté | Tableau de bord Tkinter de statut |
| **Auto-Genesis (`genesis_deploy.py`)** | **Implémenté** | Orchestrateur multi-processus |
| **Bootstrap (`bootstrap.sh`)** | **Implémenté** | Installation bare-metal systemd |

---

## Commandes vocales

| Modèle de commande | Statut | Exemple |
|--------------------|--------|---------|
| Revendiquer le nœud | Implémenté | `"Claim node"` |
| Déployer une application | Implémenté | `"deploy application my-app"` |
| Corriger une application | **Implémenté** | `"patch app my-app to add logging"` |
| Autoriser un nœud | **Implémenté** | `"authorize node <64-char-vibe-hash>"` |
| Statut / grille | Implémenté | `"status grid"` |

---

## Options de déploiement

| Méthode | Statut | Plateforme |
|---------|--------|------------|
| `python3 utahmosphere_master.py` | **Recommandé** | Toutes |
| `python3 utahmosphere_os.py` | Implémenté | Toutes |
| `python3 genesis_deploy.py` | Implémenté | Linux / dev |
| `sudo bash bootstrap.sh` | **Recommandé prod** | Linux systemd |
| `sudo bash setup.sh` | Implémenté | Alias de bootstrap |
| `./mk_iso.sh` | **Implémenté** | Linux — génère `utah_genesis_v25.iso` |
| `docker-compose up` | Optionnel | Commodité héritée uniquement |

---

## Feuille de route (restant)

- Intégration Alpine/vmlinuz dans Genesis ISO (le menu de démarrage documente aujourd'hui le chemin d'installation manuel)
- Anti-rejeu nonce/horodatage pour les commandes vocales
- Interface de révocation `authorized_nodes`

Consultez la [Référence API](API_REFERENCE.md) et le [Guide du développeur](DEVELOPER_COOKBOOK.md) pour les détails d'implémentation actuels.
