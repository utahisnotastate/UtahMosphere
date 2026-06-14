# Õpetus: Seadistus ilma žargoonita

**Sihtgrupp:** Mitte-tehnilised kasutajad, väikeettevõtete omanikud  
**Aeg:** 20 minutit (tehnilise abilisega)  
**Eesmärk:** Käivita UtahMosphere ja juuruta esimene rakendus

---

## Mis on UtahMosphere?

Mõtle sellele kui **väikesele arvuti ajule**, mis käitab sinu veebilehte või rakendust **sinu kontoris või kodus** — ilma igakuise pilve arveta Amazonilt või Google'ilt.

Sa saad isegi **rääkida sellega**: "Deploy application my-store" ja see seadistab asjad.

Täielik lihtsas keeles juhend: [Mitte-tehniline kasutajajuhend](../NON_TECHNICAL_GUIDE.md)

---

## Mida vajad

| Asi | Miks |
|-----|------|
| Mini PC või Raspberry Pi | "Aju" riistvara |
| Internet (seadistuseks) | Tarkvara allalaadimine üks kord |
| Tehniline abiline (valikuline) | Paigalduskäsu jaoks |
| USB mikrofon (valikuline) | Hääljuhtimiseks |

---

## Samm 1: Paigalda aju

Sinu abiline käivitab Mini PC-l (Linux) **ühe käsu**:

```bash
sudo bash setup.sh
```

See paigaldab kõik automaatselt. Võtab umbes 10–15 minutit.

**Pole Linuxit?** Sinu abiline saab kasutada Dockerit:

```bash
docker-compose up -d
```

---

## Samm 2: Kontrolli, et töötab

Sinu abiline avab brauseri või terminali ja kontrollib:

```bash
curl http://127.0.0.1:8999/health
```

Kui näed `"healthy"` — aju on ärkvel.

---

## Samm 3: Õpeta talle oma hääl (valikuline)

Sinu abiline käivitab:

```bash
python voice_bridge.py
```

Sa ütled selgelt: **"Claim node"**

Nüüd saab ainult sinu hääl (või heakskiidetud abiline) süsteemi juhtida.

---

## Samm 4: Pane rakendus võrgusse

**Häälega:** Ütle **"Deploy application my-store"**

**Ilma hääleta:** Sinu abiline käivitab:

```bash
python examples/voice-deploy-simulator/deploy.py my-store
```

See ongi kõik. Keerulisi serveri seadistusi pole.

---

## Samm 5: Vaata, mis töötab

Sinu abiline saab avada rohelist armatuurlauda:

```bash
python flux_gui.py
```

Või kontrolli mis tahes arvutist samas võrgus:

```bash
curl http://YOUR-MINI-PC-IP:8999/status
```

---

## Igapäevased ülesanded (küsi abilise käest)

| Sa tahad… | Ütle või palu… |
|-----------|----------------|
| Lisada uue rakenduse | "Deploy application [nimi]" |
| Kontrollida, mis töötab | "Status grid" |
| Näha armatuurlauda | Ava Utah-Flux GUI |
| Midagi parandada | Taaskäivita: `sudo systemctl restart utahmosphere` |

---

## "Nullhoolduse" lubadus

UtahMosphere koristab vanu ressursse ja parandab end taustal. Seadistad üks kord ja see jääb tööle.

Varukoopia ja taastamise jaoks peaks sinu abiline järgima: [Operatsioonide käsiraamat](../LOCAL_DEVELOPMENT.md) (varukoopia jaotis).

---

## Sõnastik

| Sõna | Lihtne tähendus |
|------|-----------------|
| **Deploy** | Pane rakendus ajule |
| **Claim node** | Õpeta ajule oma hääl |
| **Tenant** | Üks rakendus süsteemis |
| **Healthy** | Aju töötab korralikult |

Rohkem abi: [Operatsiooni retseptid](../recipes/README.md)
