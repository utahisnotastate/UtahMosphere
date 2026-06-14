# Tutoriel : Configuration sans jargon

**Public :** Utilisateurs non techniques, propriétaires de petites entreprises  
**Durée :** 20 minutes (avec l'aide d'une personne à l'aise avec la technique)  
**Objectif :** Faire tourner UtahMosphere et déployer votre première application

---

## Qu'est-ce qu'UtahMosphere ?

Pensez-y comme un **petit cerveau informatique** qui fait tourner votre site web ou application **dans votre bureau ou votre maison** — sans facture cloud mensuelle d'Amazon ou Google.

Vous pouvez même **lui parler** : « Deploy application my-store » et il configure tout.

Guide complet en langage simple : [Guide non technique](../NON_TECHNICAL_GUIDE.md)

---

## Ce dont vous avez besoin

| Élément | Pourquoi |
|---------|----------|
| Mini PC ou Raspberry Pi | Le matériel « cerveau » |
| Internet (pour la configuration) | Télécharger le logiciel une fois |
| Une personne aidante (optionnel) | Pour la commande d'installation |
| Microphone USB (optionnel) | Pour le contrôle vocal |

---

## Étape 1 : Installer le cerveau

Votre aidant exécute **une seule commande** sur le mini PC (Linux) :

```bash
sudo bash setup.sh
```

Cela installe tout automatiquement. Comptez environ 10 à 15 minutes.

**Pas de Linux ?** Votre aidant peut utiliser Docker à la place :

```bash
docker-compose up -d
```

---

## Étape 2 : Vérifier que ça fonctionne

Votre aidant ouvre un navigateur ou un terminal et vérifie :

```bash
curl http://127.0.0.1:8999/health
```

Si vous voyez `"healthy"` — le cerveau est éveillé.

---

## Étape 3 : Lui apprendre votre voix (optionnel)

Votre aidant exécute :

```bash
python voice_bridge.py
```

Vous dites clairement : **"Claim node"**

Désormais, seule votre voix (ou un aidant approuvé) peut contrôler le système.

---

## Étape 4 : Mettre votre application en ligne

**Avec la voix :** Dites **"Deploy application my-store"**

**Sans voix :** Votre aidant exécute :

```bash
python examples/voice-deploy-simulator/deploy.py my-store
```

C'est tout. Pas de réglages serveur compliqués.

---

## Étape 5 : Voir ce qui tourne

Votre aidant peut ouvrir le tableau de bord vert :

```bash
python flux_gui.py
```

Ou vérifier depuis n'importe quel ordinateur sur le même réseau :

```bash
curl http://YOUR-MINI-PC-IP:8999/status
```

---

## Tâches quotidiennes (demandez à votre aidant)

| Vous voulez… | Dites ou demandez… |
|--------------|-------------------|
| Ajouter une nouvelle application | "Deploy application [name]" |
| Vérifier ce qui tourne | "Status grid" |
| Voir le tableau de bord | Ouvrir l'interface Utah-Flux |
| Réparer quelque chose | Redémarrer : `sudo systemctl restart utahmosphere` |

---

## La promesse « sans maintenance »

UtahMosphere nettoie les anciennes ressources et se répare en arrière-plan. Vous le configurez une fois et il continue de tourner.

Pour la sauvegarde et la récupération, votre aidant devrait consulter le [Guide de développement local](../LOCAL_DEVELOPMENT.md).

---

## Glossaire

| Mot | Signification simple |
|-----|----------------------|
| **Deploy** | Mettre une application sur le cerveau |
| **Claim node** | Apprendre au cerveau votre voix |
| **Tenant** | Une application qui tourne sur le système |
| **Healthy** | Le cerveau fonctionne correctement |

Plus d'aide : [Index des recettes](../recipes/README.md)
