# Executive Recipes

Worksheets and checklists for business leaders evaluating UtahMosphere.

---

## Recipe: 90-Day Pilot Charter

```markdown
## UtahMosphere Pilot Charter

**Sponsor:** _______________
**CTO lead:** _______________
**Start date:** _______________

### Success metrics
- [ ] Node uptime > 99% (measured via /health)
- [ ] ≥ 2 workloads migrated from cloud
- [ ] Documented OpEx comparison vs. current cloud bill
- [ ] Security sign-off on access control model

### Scope (in)
- Edge APIs, internal tools, high-egress data paths

### Scope (out)
- Mission-critical DB until RDS ledger API ships
- PCI/HIPAA workloads until compliance review

### Exit criteria
- Go / no-go decision by day 90
```

---

## Recipe: OpEx Comparison Spreadsheet

| Category | Current monthly ($) | UtahMosphere pilot ($) | Notes |
|----------|--------------------|-----------------------|-------|
| Compute VMs | | $0 (owned HW) | |
| Kubernetes mgmt | | $0 | UtahNetes gossip |
| S3 storage | | Local disk | |
| S3 egress | | $0 | |
| RDS | | TBD | Ledger API roadmap |
| DevOps FTE hours | | Reduced | Voice deploy |
| Hardware CapEx | | $100–300 one-time | |
| **Total** | | | |

---

## Recipe: Hybrid Migration Decision Tree

```
Is workload latency-sensitive to users on LAN?
├─ Yes → Candidate for UtahMosphere edge
└─ No → Keep on cloud OR evaluate cost only

Does workload move >100GB/month egress?
├─ Yes → High priority for mesh storage (when S3 API ships)
└─ No → Lower priority

Is workload stateless HTTP/API?
├─ Yes → Migrate now via /command deploy
└─ No → Hybrid: UtahMosphere compute + cloud DB
```

---

## Recipe: Board-Ready One-Pager

**Problem:** Cloud OpEx growing 20%+ YoY; egress and idle compute dominate.

**Solution:** UtahMosphere sovereign nodes on $100 Mini PCs — MIT licensed, voice-operable.

**Proof:** 30-minute executive tutorial deploys live pilot with payment-gate demo.

**Ask:** Approve 90-day pilot budget ($500 hardware + 40 eng hours).

Tutorial: [Executive Quickstart](../tutorials/02-executive-quickstart.md)

---

## Recipe: Risk Register (Starter)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| API parity gaps | Medium | Medium | Use capability matrix; hybrid architecture |
| Single voice owner | Low | High | Document claim/recovery runbook |
| Hardware failure | Medium | Medium | Multi-node gossip sync |
| Skill gap | Medium | Low | Developer tutorial + templates |
