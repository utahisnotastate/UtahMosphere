# Leksion: Primeru Robott Butler

**Para håyi:** Familia yan famagu'on  
**Tiempo:** 15 minutos  
**Necessita:** Kompiuter yan UtahMosphere install, mikrofonu ti necesario

---

## Håfa un na' build

Un dikike' "Robott Butler" gi kompiuter-mu na ma listen yan ma deploy apps yanggen un request.

---

## Paso 1: Familiariza yan i Butler

UtahMosphere komo Robott Butler gi dikike' na box (Mini PC pat Raspberry Pi). Instead of paying big company para hosting, i butler mañana gi **kuartu-mu**.

Tutuhon i butler brains:

```bash
python utahmosphere_os.py
```

Eskueha adult para set `UTAH_DATA_DIR` gi folder gi kompiuter-mu yanggen ti Linux.

---

## Paso 2: Say hello gi Butler

Open otro window ya run:

```bash
python voice_bridge.py
```

Yanggen ma sångan **"Listening..."**, try sångan:

> **"Claim node"**

Este ma teach i butler i bos-mu. Komo giving keys na solo i bos-mu puede usa.

---

## Paso 3: Build lemonade stand

Sångan:

> **"Deploy application lemonade"**

I butler create dikike' "lemonade stand" app gi kompiuter. Chek success:

```bash
curl http://127.0.0.1:8999/status
```

Espiha `"lemonade"` gi tenant list.

---

## Paso 4: Ti mikrofonu? Ti problema!

Eskueha adult run este instead:

```bash
python examples/voice-deploy-simulator/deploy.py lemonade
```

Same result — i butler build i stand ha'.

---

## Paso 5: Li'e i control screen

Yanggen guaha screen, run:

```bash
python flux_gui.py
```

Un li'e green text showing håfa i butler doing — komo spaceship dashboard!

---

## Håfa un aprende

- **Claim node** = teach butler i bos-mu (biometric claim)
- **Deploy application** = build something new (voice deploy)
- I butler keep list of everything built

---

## Fun Challenges

1. Deploy tres apps: `toys`, `games`, yan `art`
2. Sångan **"status grid"** ya lee håfa i butler report
3. Draw picture of Robott Butler-mu ya label: Voice, Brains, Apps

Mas: [ELI5 para Famagu'on](../ELI5_FOR_KIDS.md) · [Referensia API](../API_REFERENCE.md)
