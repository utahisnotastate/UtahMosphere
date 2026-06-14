# Opas: Ensimmäinen robottihovimestari

**Kohderyhmä:** Lapset ja perheet  
**Aika:** 15 minuuttia  
**Tarvitset:** Tietokoneen UtahMosphere-asennuksella, valinnainen mikrofoni

---

## Mitä rakennat

Pienen "Robottihovimestarin" tietokoneellesi, joka kuuntelee sinua ja ottaa sovelluksia käyttöön pyynnöstäsi.

---

## Vaihe 1: Tapaa hovimestari

UtahMosphere on kuin robottihovimestari pienessä laatikossa (Mini PC tai Raspberry Pi). Sen sijaan, että maksaisit isosta yhtiöstä isännöinnistä, hovimestari asuu **sinun** huoneessasi.

Käynnistä hovimestarin aivot:

```bash
python utahmosphere_os.py
```

Pyydä aikuista asettamaan `UTAH_DATA_DIR` kansioon tietokoneellasi, jos et ole Linuxissa.

---

## Vaihe 2: Tervehdi hovimestaria

Avaa toinen ikkuna ja suorita:

```bash
python voice_bridge.py
```

Kun se sanoo **"Listening..."**, kokeile sanoa:

> **"Claim node"**

Tämä opettaa hovimestaria äänellesi. Se on kuin antaisit hovimestarille avaimen, jota vain sinun äänesi voi käyttää.

---

## Vaihe 3: Rakenna limonadikioski

Sano:

> **"Deploy application lemonade"**

Hovimestari luo pienen "limonadikioski"-sovelluksen tietokoneelle. Tarkista, että se onnistui:

```bash
curl http://127.0.0.1:8999/status
```

Etsi `"lemonade"` vuokralaisluettelosta.

---

## Vaihe 4: Ei mikrofonia? Ei ongelmaa!

Pyydä aikuista suorittamaan tämä sen sijaan:

```bash
python examples/voice-deploy-simulator/deploy.py lemonade
```

Sama tulos — hovimestari rakentaa kioskin silti.

---

## Vaihe 5: Katso ohjausnäyttöä

Jos sinulla on näyttö, suorita:

```bash
python flux_gui.py
```

Näet vihreää tekstiä, joka näyttää mitä hovimestari tekee — kuin avaruusaluksen hallintapaneeli!

---

## Mitä opit

- **Claim node** = opeta hovimestaria äänellesi
- **Deploy application** = rakenna jotain uutta
- Hovimestari pitää luettelon kaikesta mitä se on rakentanut

---

## Hauskoja haasteita

1. Ota käyttöön kolme sovellusta: `toys`, `games` ja `art`
2. Sano **"status grid"** ja lue mitä hovimestari raportoi
3. Piirrä kuva Robottihovimestariistasi ja merkitse: Ääni, Aivot, Sovellukset

Lisää aktiviteetteja: [Lasten reseptit](../recipes/README.md)

Vanhempien opas: [Selitettynä lapsille](../ELI5_FOR_KIDS.md)
