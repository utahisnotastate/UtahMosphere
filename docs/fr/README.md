# Portail de documentation UtahMosphere

Bienvenue sur le hub de documentation d'UtahMosphere OS **v28.0 TPM-Hardened Attested** — plateforme souveraine edge bare-metal unifiée, port **8999**. La v28.0 complète la chaîne de confiance souveraine : **verrouillage TPM Vibe-Print**, **attestation RA-TLS du maillage**, **basculement mempool 4 régions** et **signature automatique des nonces vocaux** — du silicium à l'essaim mondial. Le contenu est organisé par **profil d'audience**, **tutoriels pratiques**, **recettes prêtes à copier-coller** et **projets de démarrage**.

---

## Commencer ici

| Document | Idéal pour |
|----------|------------|
| [Matrice des capacités](CAPABILITY_MATRIX.md) | Tous — v28.0 TPM-Hardened Attested vs. travaux futurs |
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

## Fonctionnalités v28.0 TPM-Hardened Attested

- **TPM Locker :** Vibe-Print scellé au PCR0 via `tpm2_create` / `tpm2_unseal` (`tpm_lock.py`)
- **RA-TLS :** citations TPM sur gossip du maillage ; vérification des pairs avant sync (`ra_tls_attest.py`)
- **Basculement mempool :** basculement US / EU / global / Océanie sur 4 régions (`tycoon_failover.py`)
- **Attestation matérielle :** porte PCR0 TPM 2.0 (`attestation_guard.py`) dans bootstrap
- **Voice Bridge signé :** `GET /nonce` automatique + HMAC (`voice_bridge_signed.py`)
- **UtahX / ContainerEngine / S3 / Lambda / RDS :** parité cloud complète
- **AuthGuard + Nonce-Guard + révocation Utah-Flux :** gouvernance du maillage
- **Genesis ISO v28 :** `utah_genesis_v28.iso`

Build `omega-build-v28-attested`. Entrée recommandée : `python3 utahmosphere_master.py`.
