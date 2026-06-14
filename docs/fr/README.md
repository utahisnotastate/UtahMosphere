# Portail de documentation UtahMosphere

Bienvenue sur le hub de documentation d'UtahMosphere OS **v26.0 Omega-Build FINAL** — plateforme souveraine edge bare-metal unifiée, port **8999**. Le noyau Omega-Build FINAL (`utahmosphere_master.py`) fournit le règlement mempool Tycoon, l'application AuthGuard `authorized_nodes[]`, le provisionnement Genesis ISO Alpine, l'anti-rejeu nonce vocal et la révocation de nœuds Utah-Flux — plus la parité complète S3/Lambda/RDS. Le contenu est organisé par **profil d'audience**, **tutoriels pratiques**, **recettes prêtes à copier-coller** et **projets de démarrage**.

---

## Commencer ici

| Document | Idéal pour |
|----------|------------|
| [Matrice des capacités](CAPABILITY_MATRIX.md) | Tous — implémentation complète v26.0 vs. travaux futurs |
| [Référence API](API_REFERENCE.md) | Développeurs et opérateurs |
| [Guide de développement local](LOCAL_DEVELOPMENT.md) | Développeurs sous Windows, macOS ou Linux |

---

## Guides par profil (aperçu)

| Profil | Document d'aperçu | Tutoriel | Recettes |
|--------|-------------------|----------|----------|
| **Enfants et familles** | [Explication pour les enfants](ELI5_FOR_KIDS.md) | [Tutoriel : Votre premier majordome robot](tutorials/01-kids-first-robot-butler.md) | [Index des recettes](recipes/README.md) |
| **Dirigeants (PDG/CTO)** | [Résumé exécutif](EXECUTIVE_SUMMARY.md) | — | [Index des recettes](recipes/README.md) |
| **Architectes** | [Plongée technique](TECHNICAL_DEEP_DIVE.md) | — | [Index des recettes](recipes/README.md) |
| **Développeurs** | [Guide du développeur](DEVELOPER_COOKBOOK.md) | [Tutoriel : Votre première application](tutorials/05-developer-first-app.md) | [Index des recettes](recipes/README.md) |
| **Utilisateurs non techniques** | [Guide non technique](NON_TECHNICAL_GUIDE.md) | [Tutoriel : Configuration sans jargon](tutorials/06-non-technical-setup.md) | [Index des recettes](recipes/README.md) |

---

## Tutoriels (étape par étape)

1. [Votre premier majordome robot](tutorials/01-kids-first-robot-butler.md) — enfants et familles
2. [Votre première application](tutorials/05-developer-first-app.md) — flux développeur de bout en bout
3. [Configuration sans jargon](tutorials/06-non-technical-setup.md) — intégration pour non-techniciens

---

## Recettes (code prêt à copier-coller)

- [Index des recettes](recipes/README.md) — liste maîtresse de toutes les recettes

---

## Modèles et projets de démarrage

### Modèles (`templates/`)

Code réutilisable à copier dans votre propre projet :

| Modèle | Objectif |
|--------|----------|
| [python-http-service](../../templates/python-http-service/) | Microservice HTTP autonome |
| [container-handler](../../templates/container-handler/) | `handler.py` pour UtahContainerEngine |
| [voice-command-client](../../templates/voice-command-client/) | Client programmatique pour `/command` |
| [frontend-upload](../../templates/frontend-upload/) | Client de téléversement navigateur |
| [tycoon-payment-client](../../templates/tycoon-payment-client/) | Flux de paiement HTTP 402 |

### Exemples (`examples/`)

Petits scripts exécutables qui utilisent l'API en direct :

| Exemple | Ce qu'il démontre |
|---------|-------------------|
| [hello-world](../../examples/hello-world/) | Déployer une application via `/command` |
| [check-node-health](../../examples/check-node-health/) | Sondes de santé et de statut |
| [paid-app-access](../../examples/paid-app-access/) | Règlement mempool/electrum Tycoon |
| [omega-build-verify](../../examples/omega-build-verify/) | Test de parité S3/Lambda/RDS/conteneur complet |
| [voice-deploy-simulator](../../examples/voice-deploy-simulator/) | Déployer sans microphone |

### Projets de démarrage (`starter-projects/`)

Mini-projets complets à forker et étendre :

| Projet | Description |
|--------|-------------|
| [minimal-api](../../starter-projects/minimal-api/) | Charge de travail API déployable la plus simple |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Tableau de bord vocal + statut |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Modèle d'application payante |

---

## Fonctionnalités v26.0 Omega-Build FINAL

- **UtahX :** proxy HTTP/1.1 natif vers les conteneurs
- **UtahContainerEngine :** serveurs handler in-process sur les ports 8200+
- **Lazarus AST :** mutation de handler en direct sans reconstruction
- **S3 Mesh / Lambda / RDS :** parité cloud complète sur le port 8999
- **Utah-Tycoon :** règlement mempool/electrum (`tycoon_settlement.py`)
- **AuthGuard :** application de `authorized_nodes[]` (`ledger_auth.py`)
- **Nonce-Guard :** anti-rejeu vocal 30 s (`nonce_guard.py`, `GET /nonce`)
- **Interface révocation Utah-Flux :** purge de nœuds maillage (`ui_revocation.py` + `flux_gui.py`)
- **Genesis ISO :** bundling Alpine vmlinuz (`genesis_iso_builder.py` → `utah_genesis_v26.iso`)
- **UtahNetes + Swarm DHT :** gossip signé et routage déterministe
- **Quantum Ledger :** revendication de nœud par vibe-print biométrique

Build `omega-build-v26-final`. Entrée recommandée : `python3 utahmosphere_master.py`.
