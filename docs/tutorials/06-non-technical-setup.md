# Tutorial: Setup Without Jargon

**Audience:** Non-technical users, small business owners  
**Time:** 20 minutes (with a tech-savvy helper)  
**Goal:** Get UtahMosphere running and deploy your first app

---

## What Is UtahMosphere?

Think of it as a **small computer brain** that runs your website or app **in your office or home** — no monthly cloud bill from Amazon or Google.

You can even **talk to it**: "Deploy application my-store" and it sets things up.

Full plain-language guide: [Non-Technical User Guide](../NON_TECHNICAL_GUIDE.md)

---

## What You Need

| Item | Why |
|------|-----|
| Mini PC or Raspberry Pi | The "brain" hardware |
| Internet (for setup) | Download software once |
| A tech helper (optional) | For the install command |
| USB microphone (optional) | For voice control |

---

## Step 1: Install the Brain

Your helper runs **one command** on the Mini PC (Linux):

```bash
sudo bash setup.sh
```

This installs everything automatically. Takes about 10–15 minutes.

**No Linux?** Your helper can use Docker instead:

```bash
docker-compose up -d
```

---

## Step 2: Check It's Working

Your helper opens a browser or terminal and checks:

```bash
curl http://127.0.0.1:8999/health
```

If you see `"healthy"` — the brain is awake.

---

## Step 3: Teach It Your Voice (Optional)

Your helper runs:

```bash
python voice_bridge.py
```

You say clearly: **"Claim node"**

Now only your voice (or an approved helper) can control the system.

---

## Step 4: Put Your App Online

**With voice:** Say **"Deploy application my-store"**

**Without voice:** Your helper runs:

```bash
python examples/voice-deploy-simulator/deploy.py my-store
```

That's it. No complicated server settings.

---

## Step 5: See What's Running

Your helper can open the green dashboard:

```bash
python flux_gui.py
```

Or check from any computer on the same network:

```bash
curl http://YOUR-MINI-PC-IP:8999/status
```

---

## Everyday Tasks (Ask Your Helper)

| You want to… | Say or ask for… |
|--------------|-----------------|
| Add a new app | "Deploy application [name]" |
| Check what's running | "Status grid" |
| See the dashboard | Open Utah-Flux GUI |
| Fix something | Restart: `sudo systemctl restart utahmosphere` |

---

## The "No Maintenance" Promise

UtahMosphere cleans up old resources and heals itself in the background. You set it up once and it keeps running.

For backup and recovery, your helper should follow: [Operations Runbook](../OPERATIONS_RUNBOOK.md) (backup section).

---

## Glossary

| Word | Simple meaning |
|------|----------------|
| **Deploy** | Put an app on the brain |
| **Claim node** | Teach the brain your voice |
| **Tenant** | One app running on the system |
| **Healthy** | The brain is working fine |

More help: [Ops Recipes](../recipes/ops-recipes.md)
