# Tutoriel : Votre premier majordome robot

**Public :** Enfants et familles  
**Durée :** 15 minutes  
**Il vous faut :** Un ordinateur avec UtahMosphere installé, microphone optionnel

---

## Ce que vous allez construire

Un petit « majordome robot » sur votre ordinateur qui vous écoute et déploie des applications quand vous le demandez.

---

## Étape 1 : Faire connaissance avec le majordome

UtahMosphere, c'est comme avoir un majordome robot dans une petite boîte (mini PC ou Raspberry Pi). Au lieu de payer une grosse entreprise pour héberger vos trucs, le majordome vit dans **votre** chambre.

Démarrez le cerveau du majordome :

```bash
python utahmosphere_os.py
```

Demandez à un adulte de vous aider à définir `UTAH_DATA_DIR` vers un dossier sur votre ordinateur si vous n'êtes pas sous Linux.

---

## Étape 2 : Dire bonjour au majordome

Ouvrez une deuxième fenêtre et exécutez :

```bash
python voice_bridge.py
```

Quand il affiche **"Listening..."**, essayez de dire :

> **"Claim node"**

Cela apprend au majordome à reconnaître votre voix. C'est comme lui donner une clé que seule votre voix peut utiliser.

---

## Étape 3 : Construire un stand de limonade

Dites :

> **"Deploy application lemonade"**

Le majordome crée une petite application « stand de limonade » sur l'ordinateur. Vérifiez que ça a fonctionné :

```bash
curl http://127.0.0.1:8999/status
```

Cherchez `"lemonade"` dans la liste des locataires.

---

## Étape 4 : Pas de microphone ? Pas de problème !

Demandez à un adulte d'exécuter ceci à la place :

```bash
python examples/voice-deploy-simulator/deploy.py lemonade
```

Même résultat — le majordome construit quand même votre stand.

---

## Étape 5 : Regarder l'écran de contrôle

Si vous avez un écran, exécutez :

```bash
python flux_gui.py
```

Vous verrez du texte vert montrant ce que fait le majordome — comme le tableau de bord d'un vaisseau spatial !

---

## Ce que vous avez appris

- **Claim node** = apprendre au majordome votre voix
- **Deploy application** = construire quelque chose de nouveau
- Le majordome garde une liste de tout ce qu'il a construit

---

## Défis amusants

1. Déployez trois applications : `toys`, `games` et `art`
2. Dites **"status grid"** et lisez ce que le majordome rapporte
3. Dessinez une image de votre majordome robot et étiquetez : Voix, Cerveau, Applications

Plus d'activités : [Index des recettes](../recipes/README.md)

Guide pour les parents : [Explication pour les enfants](../ELI5_FOR_KIDS.md)
