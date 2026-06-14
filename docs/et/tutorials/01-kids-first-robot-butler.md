# Õpetus: Sinu esimene robot-kammerjäger

**Sihtgrupp:** Lapsed ja pered  
**Aeg:** 15 minutit  
**Vajad:** Arvuti UtahMosphere paigaldatud, valikuline mikrofon

---

## Mida sa ehitad

Väike "robot-kammerjäger" sinu arvutis, kes kuulab sind ja juurutab rakendusi, kui palud.

---

## Samm 1: Tutvu kammerjägriga

UtahMosphere on nagu robot-kammerjäger väikeses karbis (Mini PC või Raspberry Pi). Selle asemel, et maksta hiigelfirmale oma asjade majutamise eest, elab kammerjäger **sinu** toas.

Käivita kammerjängra aju:

```bash
python utahmosphere_os.py
```

Palu täiskasvanul seada `UTAH_DATA_DIR` kausta sinu arvutis, kui sa pole Linuxis.

---

## Samm 2: Ütle kammerjägrale tere

Ava teine aken ja käivita:

```bash
python voice_bridge.py
```

Kui see ütleb **"Listening..."**, proovi öelda:

> **"Claim node"**

See õpetab kammerjägrale sinu hääle. Nagu annaksid kammerjägrale võtme, mida ainult sinu hääl saab kasutada.

---

## Samm 3: Ehita limonaadiputka

Ütle:

> **"Deploy application lemonade"**

Kammerjäger loob arvutisse väikese "limonaadiputka" rakenduse. Kontrolli, et see töötas:

```bash
curl http://127.0.0.1:8999/status
```

Otsi rentnikute nimekirjast `"lemonade"`.

---

## Samm 4: Pole mikrofoni? Pole probleemi!

Palu täiskasvanul käivitada selle asemel:

```bash
python examples/voice-deploy-simulator/deploy.py lemonade
```

Sama tulemus — kammerjäger ehitab su putka ikkagi.

---

## Samm 5: Vaata juhtpaneeli

Kui sul on ekraan, käivita:

```bash
python flux_gui.py
```

Näed rohelist teksti, mis näitab, mida kammerjäger teeb — nagu kosmoselaeva armatuurlaud!

---

## Mida sa õppisid

- **Claim node** = õpeta kammerjägrale oma hääl
- **Deploy application** = ehita midagi uut
- Kammerjäger hoiab nimekirja kõigest, mida ta ehitas

---

## Lõbusad väljakutsed

1. Juuruta kolm rakendust: `toys`, `games` ja `art`
2. Ütle **"status grid"** ja loe, mida kammerjäger teatab
3. Joonista pilt oma robot-kammerjägrast ja märgi: Hääl, Aju, Rakendused

Rohkem tegevusi: [Laste retseptid](../recipes/README.md)

Vanemate juhend: [Lihtsas keeles lastele](../ELI5_FOR_KIDS.md)
