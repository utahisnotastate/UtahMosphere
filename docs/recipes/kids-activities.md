# Kids Activities

Fun experiments with your UtahMosphere Robot Butler.

---

## Activity 1: Name Three Apps

Deploy three apps with silly names:

```bash
python examples/voice-deploy-simulator/deploy.py dinosaur-park
python examples/voice-deploy-simulator/deploy.py pizza-robot
python examples/voice-deploy-simulator/deploy.py space-cat
```

Check the list:

```bash
curl http://127.0.0.1:8999/status
```

How many apps are running? (`active_workloads`)

---

## Activity 2: Butler Memory Game

1. Deploy `secret-base`
2. Say or send **"status grid"**
3. Find `secret-base` in the response

Ask a friend to deploy a different app on another computer (if you have two butlers on the same network).

---

## Activity 3: Draw the Stack

Draw four boxes and label them:

1. **Your voice** → Voice Bridge
2. **Butler brain** → Kernel (port 8999)
3. **Apps** → Containers folder
4. **Dashboard** → Utah-Flux green screen

---

## Activity 4: Health Check Detective

Run:

```bash
python examples/check-node-health/health_check.py
```

If it says `healthy`, the butler is happy. If not, ask a grown-up to start `utahmosphere_os.py`.

---

## Activity 5: Payment Treasure Hunt

```bash
python examples/paid-app-access/access_app.py treasure
```

First you get a "payment required" message. Wait one minute and try again — treasure unlocked!

This is how apps can charge tiny amounts (like arcade tokens) on UtahMosphere.

---

## Word Search

Find these words in the docs:

- Sovereign
- Butler
- Tenant
- Mesh
- Vibe

Parent guide: [ELI5 For Kids](../ELI5_FOR_KIDS.md)  
Tutorial: [Your First Robot Butler](../tutorials/01-kids-first-robot-butler.md)
