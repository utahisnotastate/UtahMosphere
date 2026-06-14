# Tutorial: Your First Robot Butler

**Audience:** Kids and families  
**Time:** 15 minutes  
**You'll need:** A computer with UtahMosphere installed, optional microphone

---

## What You'll Build

A tiny "Robot Butler" on your computer that listens to you and deploys apps when you ask.

---

## Step 1: Meet the Butler

UtahMosphere is like having a robot butler in a small box (Mini PC or Raspberry Pi). Instead of paying a big company to host your stuff, the butler lives in **your** room.

Start the butler's brain:

```bash
python utahmosphere_os.py
```

Ask a grown-up to help set `UTAH_DATA_DIR` to a folder on your computer if you're not on Linux.

---

## Step 2: Say Hello to the Butler

Open a second window and run:

```bash
python voice_bridge.py
```

When it says **"Listening..."**, try saying:

> **"Claim node"**

This teaches the butler your voice. It's like giving the butler a key that only your voice can use.

---

## Step 3: Build a Lemonade Stand

Say:

> **"Deploy application lemonade"**

The butler creates a tiny "lemonade stand" app on the computer. Check that it worked:

```bash
curl http://127.0.0.1:8999/status
```

Look for `"lemonade"` in the tenants list.

---

## Step 4: No Microphone? No Problem!

Ask a grown-up to run this instead:

```bash
python examples/voice-deploy-simulator/deploy.py lemonade
```

Same result — the butler still builds your stand.

---

## Step 5: Watch the Control Screen

If you have a screen, run:

```bash
python flux_gui.py
```

You'll see green text showing what the butler is doing — like a spaceship dashboard!

---

## What You Learned

- **Claim node** = teach the butler your voice
- **Deploy application** = build something new
- The butler keeps a list of everything it built

---

## Fun Challenges

1. Deploy three apps: `toys`, `games`, and `art`
2. Say **"status grid"** and read what the butler reports
3. Draw a picture of your Robot Butler and label: Voice, Brain, Apps

More activities: [Kids Recipes](../recipes/kids-activities.md)

Parent guide: [ELI5 For Kids](../ELI5_FOR_KIDS.md)
