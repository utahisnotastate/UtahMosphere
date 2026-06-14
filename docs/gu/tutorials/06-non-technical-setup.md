# Leksion: Setup Sin Jargon

**Para håyi:** Usuarios ti teknikal, small business owners  
**Tiempo:** 20 minutos (yan teknikal assistant)  
**Meta:** Get UtahMosphere running yan deploy first app

---

## Håfa i UtahMosphere?

Think of it komo **dikike' kompiuter brains** na run i website pat apps-mu **gi office pat gima'** — ti monthly cloud bill gi Amazon pat Google.

Puede **sångan**: "Deploy application my-store" ya ma handle i install.

Full plain-language guide: [Guia Ti Teknikal](../NON_TECHNICAL_GUIDE.md)

---

## Håfa necessita

| Item | Para håfa |
|------|-----------|
| Mini PC pat Raspberry Pi | Hardware para "brains" |
| Internet (para install) | Download software un biahi |
| Teknikal assistant (ti necesario) | Para install command |
| USB mikrofonu (ti necesario) | Para voice control |

---

## Paso 1: Install i brains

I assistant run **un command** gi Mini PC (Linux):

```bash
sudo bash setup.sh
```

Ma install everything automaticamente. ~10–15 minutos.

**Ti Linux?** I assistant puede usa Docker:

```bash
docker-compose up -d
```

---

## Paso 2: Chek mumuña

I assistant open browser pat terminal ya check:

```bash
curl http://127.0.0.1:8999/health
```

Yanggen un li'e `"healthy"` — i brains awake.

---

## Paso 3: Teach i bos-mu (ti necesario)

I assistant run:

```bash
python voice_bridge.py
```

Sångan clearly: **"Claim node"**

På'go solo i bos-mu (pat approved assistant) puede control i sistema — biometric claim.

---

## Paso 4: Put i app-mu online

**Voice:** Sångan **"Deploy application my-store"**

**Sin voice:** I assistant run:

```bash
python examples/voice-deploy-simulator/deploy.py my-store
```

Listo. Ti complicated server config.

---

## Paso 5: Li'e håfa running

I assistant open green dashboard:

```bash
python flux_gui.py
```

Pat check from any kompiuter gi same network:

```bash
curl http://YOUR-MINI-PC-IP:8999/status
```

---

## Daily Tasks (ask assistant)

| Malago'… | Sångan pat ask… |
|----------|-----------------|
| Add new app | "Deploy application [name]" |
| Check running | "Status grid" |
| Li'e dashboard | Open Utah-Flux GUI |
| Fix something | Restart: `sudo systemctl restart utahmosphere` |

---

## "Zero-Maintenance" Promise

UtahMosphere clean old resources yan self-heal gi background. Install un biahi ya sigi running.

Para backup yan restore, i assistant usa steps gi [Guia Desarrollu Lokal](../LOCAL_DEVELOPMENT.md).

---

## Vocabulary

| På'ot | Simple meaning |
|-------|----------------|
| **Deploy** | Put app gi brains |
| **Claim node** | Teach brains i bos-mu |
| **Tenant** | Un app gi sistema |
| **Healthy** | Brains working fine |

Mas ayuda: [Referensia API](../API_REFERENCE.md) · [Indeks Recepta](../recipes/README.md)
