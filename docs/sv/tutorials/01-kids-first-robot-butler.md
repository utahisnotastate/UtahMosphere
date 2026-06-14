# Guide: Din första robotbutler

**Målgrupp:** Barn och familjer  
**Tid:** 15 minuter  
**Du behöver:** En dator med UtahMosphere installerat, valfri mikrofon

---

## Vad du bygger

En liten "Robotbutler" på din dator som lyssnar på dig och driftsätter appar när du ber om det.

---

## Steg 1: Möt butlern

UtahMosphere är som att ha en robotbutler i en liten låda (Mini PC eller Raspberry Pi). Istället för att betala ett stort företag för att hosta dina saker bor butlern i **ditt** rum.

Starta butlerns hjärna:

```bash
python utahmosphere_os.py
```

Be en vuxen hjälpa till att sätta `UTAH_DATA_DIR` till en mapp på din dator om du inte är på Linux.

---

## Steg 2: Säg hej till butlern

Öppna ett andra fönster och kör:

```bash
python voice_bridge.py
```

När den säger **"Listening..."**, prova att säga:

> **"Claim node"**

Detta lär butlern din röst. Det är som att ge butlern en nyckel som bara din röst kan använda.

---

## Steg 3: Bygg en limonadkiosk

Säg:

> **"Deploy application lemonade"**

Butlern skapar en liten "limonadkiosk"-app på datorn. Kontrollera att det fungerade:

```bash
curl http://127.0.0.1:8999/status
```

Leta efter `"lemonade"` i tenant-listan.

---

## Steg 4: Ingen mikrofon? Inga problem!

Be en vuxen köra detta istället:

```bash
python examples/voice-deploy-simulator/deploy.py lemonade
```

Samma resultat — butlern bygger fortfarande din kiosk.

---

## Steg 5: Titta på kontrollskärmen

Om du har en skärm, kör:

```bash
python flux_gui.py
```

Du ser grön text som visar vad butlern gör — som en rymdskeppspanel!

---

## Vad du lärde dig

- **Claim node** = lär butlern din röst
- **Deploy application** = bygg något nytt
- Butlern håller en lista över allt den har byggt

---

## Roliga utmaningar

1. Driftsätt tre appar: `toys`, `games` och `art`
2. Säg **"status grid"** och läs vad butlern rapporterar
3. Rita en bild av din Robotbutler och märk: Röst, Hjärna, Appar

Fler aktiviteter: [Barnrecept](../recipes/README.md)

Föräldraguide: [Förklarat för barn](../ELI5_FOR_KIDS.md)
