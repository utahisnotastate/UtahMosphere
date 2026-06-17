---
name: zeo-entropy
description: Autonomic debt pruner — scan cyclomatic complexity and suggest collapse targets via zeo_entropy MCP.
---

# ZEO-Entropy

When code accrues structural debt:

1. Call `zeo_entropy.suggest_collapse_targets` (limit 3).
2. For each target, rewrite with functional dispatch, early returns, or extracted helpers.
3. Append refactor note to `.cursor/memory.md`.
4. If systemic, call `zeo_akashic_adr.log_architectural_decision`.

Trigger: user clicks **Entropy Purge** on the Omni-Viewport Command Deck, or sends `[PROTOCOL: ENTROPY-PURGE]`.
