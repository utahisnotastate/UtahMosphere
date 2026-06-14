# Tutorial: Executive Quickstart

**Audience:** CEOs, CTOs, business leaders  
**Time:** 30 minutes  
**Goal:** Evaluate UtahMosphere for hybrid cloud migration and cost reduction

---

## Executive Summary

UtahMosphere OS v25.0 is a sovereign edge platform that runs on low-cost hardware (Mini PC, Raspberry Pi) instead of hyperscaler VMs. This tutorial walks through a **proof-of-concept deployment** you can complete in one meeting.

---

## Step 1: Understand the Value Proposition

| Traditional Cloud Pain | UtahMosphere Answer |
|------------------------|---------------------|
| Data egress fees | Local P2P mesh — data stays on your hardware |
| Idle VM costs | Pay once for hardware; no per-hour billing |
| Ops overhead | ASEN self-healing, automated janitor, voice ops |
| Vendor lock-in | You own the node; MIT-licensed stack |

Read the full business case: [Executive Summary](../EXECUTIVE_SUMMARY.md)

---

## Step 2: Deploy a Pilot Node

**Option A — Linux production path:**

```bash
sudo bash setup.sh
```

**Option B — Docker evaluation (any OS):**

```bash
docker-compose up -d
curl http://127.0.0.1:8999/health
```

**Success criteria:** Health endpoint returns `"status": "healthy"`.

---

## Step 3: Run the 5-Minute Demo

1. **Deploy a sample workload** (no voice needed):

   ```bash
   python examples/voice-deploy-simulator/deploy.py pilot-app
   ```

2. **Show payment gate (monetization demo):**

   ```bash
   python examples/paid-app-access/access_app.py pilot-app
   ```

   First call returns HTTP 402 (payment required). After ~60 seconds, access unlocks.

3. **Show status dashboard:**

   ```bash
   curl http://127.0.0.1:8999/status
   ```

---

## Step 4: Hybrid Migration Assessment

Use the [Capability Matrix](../CAPABILITY_MATRIX.md) with your CTO to score:

- [ ] Which AWS/GCP services map to implemented APIs today?
- [ ] Which workloads are edge-suitable (low latency, high egress)?
- [ ] What stays on hyperscaler during phase 1?

Recommended hybrid pattern:

1. Keep public web frontends on CDN/hyperscaler
2. Move data-heavy backends to UtahMosphere mesh
3. Use voice/API deploy for internal tools first

---

## Step 5: ROI Worksheet

| Line item | Monthly AWS (example) | UtahMosphere pilot |
|-----------|----------------------|-------------------|
| Compute (2 VMs) | $400 | $0 (owned hardware) |
| S3 egress | $150 | $0 (local mesh) |
| RDS | $200 | Roadmap (ledger API) |
| **Total** | **$750** | **~$15 electricity** |

Hardware CapEx: ~$100–300 one-time per node.

Full recipes: [Executive Recipes](../recipes/executive-recipes.md)

---

## Decision Checklist

- [ ] Pilot node health verified
- [ ] CTO reviewed capability matrix
- [ ] Security team reviewed [Access Control](../ACCESS_CONTROL.md)
- [ ] Hybrid migration scope defined
- [ ] 90-day evaluation metrics set (uptime, cost, deploy velocity)

---

## Next Steps

- Architect deep-dive: [Tutorial: Architect Deployment](03-architect-deployment.md)
- Migration path: [Tutorial: Cloud Migration Walkthrough](04-cloud-migration-walkthrough.md)
