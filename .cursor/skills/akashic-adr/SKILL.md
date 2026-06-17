---
name: akashic-adr
description: Write immutable Architecture Decision Records to .cursor/adr/ on every structural pivot, schism, or Immortalize protocol.
---

# Akashic-ADR

On structural changes (new module, library, schism, major refactor):

1. Call `zeo_akashic_adr.log_architectural_decision` with Context, Decision, Consequences.
2. For **Schism** protocol, use `log_schism_decision` instead.
3. ADRs auto-update `.cursor/adr/INDEX.md` and `.cursor/memory.md`.

Never leave architecture undocumented. Never use stale external wikis.
