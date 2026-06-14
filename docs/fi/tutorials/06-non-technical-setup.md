# Opas: Käyttöönotto ilman jargon

**Kohderyhmä:** Ei-tekniset käyttäjät, pienyritysten omistajat  
**Aika:** 20 minuuttia (teknisesti taitavan avustajan kanssa)  
**Tavoite:** Saada UtahMosphere käyntiin ja ottaa ensimmäinen sovellus käyttöön

---

## Mikä on UtahMosphere?

Ajattele sitä **pienenä tietokoneaivoina**, joka ajaa verkkosivustosi tai sovelluksesi **toimistossasi tai kotona** — ei kuukausittaista pilvilaskua Amazonilta tai Googlelta.

Voit jopa **puhua sille**: "Deploy application my-store" ja se hoitaa asennuksen.

Täydellinen selkokieliopas: [Ei-tekninen käyttäjäopas](../NON_TECHNICAL_GUIDE.md)

---

## Mitä tarvitset

| Kohde | Miksi |
|-------|-------|
| Mini PC tai Raspberry Pi | "Aivojen" laitteisto |
| Internet (asennusta varten) | Lataa ohjelmiston kerran |
| Tekninen avustaja (valinnainen) | Asennuskomentoa varten |
| USB-mikrofoni (valinnainen) | Ääniohjausta varten |

---

## Vaihe 1: Asenna aivot

Avustajasi suorittaa **yhden komennon** Mini PC:llä (Linux):

```bash
sudo bash setup.sh
```

Tämä asentaa kaiken automaattisesti. Kestää noin 10–15 minuuttia.

**Ei Linuxia?** Avustajasi voi käyttää Dockeria sen sijaan:

```bash
docker-compose up -d
```

---

## Vaihe 2: Tarkista, että se toimii

Avustajasi avaa selaimen tai terminaalin ja tarkistaa:

```bash
curl http://127.0.0.1:8999/health
```

Jos näet `"healthy"` — aivot ovat hereillä.

---

## Vaihe 3: Opeta se äänellesi (valinnainen)

Avustajasi suorittaa:

```bash
python voice_bridge.py
```

Sanot selkeästi: **"Claim node"**

Nyt vain sinun äänesi (tai hyväksytty avustaja) voi ohjata järjestelmää.

---

## Vaihe 4: Laita sovelluksesi verkkoon

**Äänellä:** Sano **"Deploy application my-store"**

**Ilman ääntä:** Avustajasi suorittaa:

```bash
python examples/voice-deploy-simulator/deploy.py my-store
```

Siinä se. Ei monimutkaisia palvelinasetuksia.

---

## Vaihe 5: Katso mitä on käynnissä

Avustajasi voi avata vihreän hallintapaneelin:

```bash
python flux_gui.py
```

Tai tarkista mistä tahansa tietokoneesta samassa verkossa:

```bash
curl http://YOUR-MINI-PC-IP:8999/status
```

---

## Arjen tehtävät (pyydä avustajaa)

| Haluat… | Sano tai pyydä… |
|---------|-----------------|
| Lisätä uuden sovelluksen | "Deploy application [name]" |
| Tarkistaa mitä on käynnissä | "Status grid" |
| Nähdä hallintapaneelin | Avaa Utah-Flux GUI |
| Korjata jotain | Käynnistä uudelleen: `sudo systemctl restart utahmosphere` |

---

## "Nollahuolto"-lupaus

UtahMosphere siivoaa vanhat resurssit ja parantaa itseään taustalla. Asennat sen kerran ja se pysyy käynnissä.

Varmuuskopiointia ja palautusta varten avustajasi noudattaa: [Operaatiokäsikirja](../LOCAL_DEVELOPMENT.md) (varmuuskopiointiosio).

---

## Sanasto

| Sana | Yksinkertainen merkitys |
|------|------------------------|
| **Deploy** | Laita sovellus aivoihin |
| **Claim node** | Opeta aivot äänellesi |
| **Tenant** | Yksi sovellus järjestelmässä |
| **Healthy** | Aivot toimivat hyvin |

Lisäapua: [Ops-reseptit](../recipes/README.md)
