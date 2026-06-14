# Portail de documentation UtahMosphere

Bienvenue sur le hub de documentation d'UtahMosphere OS v25.0 — cloud souverain edge Python, port **8999**. Le contenu est organisé par **profil d'audience**, **tutoriels pratiques**, **recettes prêtes à copier-coller** et **projets de démarrage**.

---

## Commencer ici

| Document | Idéal pour |
|----------|------------|
| [Matrice des capacités](CAPABILITY_MATRIX.md) | Tous — ce qui fonctionne aujourd'hui vs. feuille de route |
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
| `templates/python-http-service/` | Microservice HTTP autonome |
| `templates/container-handler/` | `handler.py` pour UtahContainerEngine |
| `templates/voice-command-client/` | Client programmatique pour `/command` |
| `templates/frontend-upload/` | Client de téléversement navigateur |
| `templates/tycoon-payment-client/` | Flux de paiement HTTP 402 |

### Exemples (`examples/`)

Petits scripts exécutables qui utilisent l'API en direct :

| Exemple | Ce qu'il démontre |
|---------|-------------------|
| `examples/hello-world/` | Déployer une application via `/command` |
| `examples/check-node-health/` | Sondes de santé et de statut |
| `examples/paid-app-access/` | Règlement du péage Tycoon |
| `examples/voice-deploy-simulator/` | Déployer sans microphone |

### Projets de démarrage (`starter-projects/`)

Mini-projets complets à forker et étendre :

| Projet | Description |
|--------|-------------|
| `starter-projects/minimal-api/` | Charge de travail API déployable la plus simple |
| `starter-projects/voice-controlled-dashboard/` | Tableau de bord vocal + statut |
| `starter-projects/monetized-endpoint/` | Modèle d'application payante |

---

## À propos de cette documentation

Cette section de documentation est entièrement en français. UtahMosphere OS v25.0 est un cloud souverain edge basé sur Python, accessible par défaut sur le port **8999**.
