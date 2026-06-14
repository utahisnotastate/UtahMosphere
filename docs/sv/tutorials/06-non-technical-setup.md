# Guide: Installation utan jargong

**Målgrupp:** Icke-tekniska användare, småföretagare  
**Tid:** 20 minuter (med en teknikintresserad hjälpare)  
**Mål:** Få UtahMosphere igång och driftsätt din första app

---

## Vad är UtahMosphere?

Tänk på det som en **liten datorhjärna** som kör din webbplats eller app **på ditt kontor eller hem** — ingen månatlig molnräkning från Amazon eller Google.

Du kan till och med **prata med den**: "Deploy application my-store" och den sätter upp allt.

Fullständig guide på enkelt språk: [Icke-teknisk användarguide](../NON_TECHNICAL_GUIDE.md)

---

## Vad du behöver

| Objekt | Varför |
|--------|--------|
| Mini PC eller Raspberry Pi | "Hjärnans" hårdvara |
| Internet (för installation) | Ladda ner programvaran en gång |
| En teknikhjälpare (valfritt) | För installationskommandot |
| USB-mikrofon (valfritt) | För röststyrning |

---

## Steg 1: Installera hjärnan

Din hjälpare kör **ett kommando** på Mini PC:n (Linux):

```bash
sudo bash setup.sh
```

Detta installerar allt automatiskt. Tar cirka 10–15 minuter.

**Ingen Linux?** Din hjälpare kan använda Docker istället:

```bash
docker-compose up -d
```

---

## Steg 2: Kontrollera att det fungerar

Din hjälpare öppnar en webbläsare eller terminal och kontrollerar:

```bash
curl http://127.0.0.1:8999/health
```

Om du ser `"healthy"` — hjärnan är vaken.

---

## Steg 3: Lär den din röst (valfritt)

Din hjälpare kör:

```bash
python voice_bridge.py
```

Du säger tydligt: **"Claim node"**

Nu kan bara din röst (eller en godkänd hjälpare) styra systemet.

---

## Steg 4: Sätt din app online

**Med röst:** Säg **"Deploy application my-store"**

**Utan röst:** Din hjälpare kör:

```bash
python examples/voice-deploy-simulator/deploy.py my-store
```

Det var allt. Inga komplicerade serverinställningar.

---

## Steg 5: Se vad som körs

Din hjälpare kan öppna den gröna panelen:

```bash
python flux_gui.py
```

Eller kontrollera från vilken dator som helst i samma nätverk:

```bash
curl http://YOUR-MINI-PC-IP:8999/status
```

---

## Vardagsuppgifter (be din hjälpare)

| Du vill… | Säg eller be om… |
|----------|------------------|
| Lägga till en ny app | "Deploy application [name]" |
| Kontrollera vad som körs | "Status grid" |
| Se panelen | Öppna Utah-Flux GUI |
| Fixa något | Starta om: `sudo systemctl restart utahmosphere` |

---

## Löftet om "nollunderhåll"

UtahMosphere städar gamla resurser och läker sig själv i bakgrunden. Du sätter upp det en gång och det fortsätter köra.

För säkerhetskopiering och återställning bör din hjälpare följa: [Driftshandbok](../LOCAL_DEVELOPMENT.md) (säkerhetskopieringssektion).

---

## Ordlista

| Ord | Enkel betydelse |
|-----|-----------------|
| **Deploy** | Lägg en app på hjärnan |
| **Claim node** | Lär hjärnan din röst |
| **Tenant** | En app som körs på systemet |
| **Healthy** | Hjärnan fungerar bra |

Mer hjälp: [Ops-recept](../recipes/README.md)
