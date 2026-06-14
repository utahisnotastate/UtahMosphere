# Matrice des capacités

Cette matrice documente ce qu'UtahMosphere OS **v25.0** implémente aujourd'hui par rapport à ce qui est décrit dans la documentation marketing ou planifié pour les versions futures. Utilisez-la pour fixer des attentes réalistes lors de la migration et du développement.

---

## Points de terminaison HTTP API

| Point de terminaison | Méthode | Statut | Notes |
|----------------------|---------|--------|-------|
| `/health` | GET | **Implémenté** | Sonde de disponibilité du nœud |
| `/status` | GET | **Implémenté** | État UI, liste des locataires, statut de revendication |
| `/command` | POST | **Implémenté** | Exécution d'intention vocale (corps JSON) |
| `/app/{name}` | GET | **Implémenté** | Accès application protégé Tycoon (402 jusqu'au paiement) |
| `/s3/*` | * | Planifié | Documenté dans le guide de migration ; pas encore routé |
| `/lambda/*/invoke` | POST | Planifié | Stubs de handler créés uniquement au déploiement |
| `/rds/read/*`, `/rds/write` | * | Planifié | Registre existant ; routes HTTP non connectées |

---

## Sous-systèmes principaux

| Composant | Statut | Ce qui fonctionne aujourd'hui |
|-----------|--------|-------------------------------|
| **Noyau (`utahmosphere_os.py`)** | Implémenté | Registre, intentions vocales, manifestes de routes UtahX, gossip maillage |
| **Quantum Ledger** | Implémenté | Revendication vibe racine, vérification hash biométrique, mode ouvert avant revendication |
| **Voice Bridge** | Implémenté | Google STT + extraction vibe-print MFCC → `/command` |
| **Utah-Tycoon** | Partiel | Génération de factures, règlement simulé 60 s, porte HTTP 402 |
| **Gossip UtahNetes** | Partiel | Synchronisation locataires multidiffusion UDP sur LAN |
| **Global Swarm** | Partiel | Table de pairs UDP, keep-alive ping ; recherche Kademlia complète en stub |
| **Démon Lazarus** | Partiel | Ajoute des commentaires de correctif à `handler.py` (pas de réécriture AST complète) |
| **Interface Utah-Flux** | Implémenté | Tableau de bord Tkinter lisant `flux_ui_manifest.json` |
| **Proxy UtahX** | Partiel | Manifestes de routes JSON écrits ; pas de processus proxy TCP en direct |

---

## Commandes vocales (autorisées)

| Modèle de commande | Statut | Exemple |
|--------------------|--------|---------|
| Revendiquer le nœud | Implémenté | `"Claim node"` |
| Déployer une application | Implémenté | `"deploy application my-app"` |
| Corriger une application | Partiel | `"patch app my-app to add logging"` |
| Statut / grille | Implémenté | `"status grid"` |

---

## Options de déploiement

| Méthode | Statut | Plateforme |
|---------|--------|------------|
| `python3 utahmosphere_os.py` | Implémenté | Toutes (définir `UTAH_DATA_DIR` localement) |
| `python3 genesis_deploy.py` | Implémenté | Linux préféré ; dev Windows OK |
| `sudo bash setup.sh` | Implémenté | Linux (service systemd) |
| `docker-compose up` | Implémenté | Optionnel ; utilise le réseau hôte |

---

## Modèle de sécurité

| Fonctionnalité | Statut | Notes |
|----------------|--------|-------|
| Titulaire vibe racine unique | Implémenté | Le premier locuteur à revendiquer possède le nœud |
| Champ `authorized_nodes[]` | Stub | Stocké dans le JSON du registre ; non appliqué dans le code |
| Signatures HMAC locataire | Documenté | Recette fournie ; application noyau partielle |
| Signature Ed25519 | Planifié | Référencé dans la doc ; non implémenté |
| `UTAH_SECRET_VECTOR` par défaut | Implémenté | À changer en production |

---

## Relation Docker / Nginx

Le **runtime principal** d'UtahMosphere est Python bare-metal. Docker et Nginx sont des **chemins hérités optionnels** :

- `docker-compose.yaml` — enveloppe pratique pour essais locaux
- `nginx.conf` — configuration de référence ; les manifestes JSON UtahX sont le chemin souverain
- `setup.sh` — supprime Docker/Nginx sur les installations Linux propres (nœuds souverains en production)

Pour les environnements hybrides, conservez Docker/Nginx aux côtés d'UtahMosphere pendant la migration.

---

## Feuille de route (pas encore implémenté)

- API HTTP de stockage d'objets compatible S3
- API HTTP d'invocation style Lambda
- API HTTP lecture/écriture du registre RDS
- Commande vocale de déploiement basée sur Git
- Mutation AST complète via Lazarus
- Intégration réelle du mempool Bitcoin dans Tycoon

Consultez la [Référence API](API_REFERENCE.md) et le [Guide du développeur](DEVELOPER_COOKBOOK.md) pour les détails d'implémentation actuels.
