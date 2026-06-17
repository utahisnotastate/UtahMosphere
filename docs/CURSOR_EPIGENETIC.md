# Cursor Epigenetic IDE (Level 6)

UtahMosphere configures Cursor as an **Omni-Viewport** — not a typewriter. The IDE inherits the project's vibe via epigenetic memory, **Command Deck buttons**, and **autonomic MCP subagents**.

> **No slash commands.** Install the [Utah Omni-Viewport extension](OMNI_VIEWPORT_EXTENSION.md) and press buttons in the activity bar.

## Utah-Archivist (`.cursor/memory.md`)

Self-rewriting subconscious memory. The Agent reads before every action, appends patterns autonomously, never asks permission.

## Omni-Viewport Command Deck

Each button copies a `[PROTOCOL: …]` prompt to the clipboard and opens Composer (`Ctrl+I`).

| Button | Protocol | Action |
|--------|----------|--------|
| **Cascade Sync** | `CASCADE` | Holographic sync across kernel, RDS, S3, Flux UI, docs, verify |
| **Absorb** | `ABSORB` | Assimilate foreign code into UtahMosphere native stack |
| **Void Fill** | `VOID-FILL` | UtahClaw MCP research only — synthesize before codegen |
| **Chrono Fix** | `CHRONO-FIX` | Time-reversal debugging from last terminal error |
| **Entropy Purge** | `ENTROPY-PURGE` | Collapse top-3 entropy hotspots via ZEO-Entropy |
| **Schism** | `SCHISM` | Extract microservice + God-Eye blast radius + ADR |
| **Vibe Shift** | `VIBE-SHIFT` | Restyle UI without mutating state logic |
| **Immortalize** | `IMMORTALIZE` | Edge-case tests + ADR + semantic commit command |
| **Evolve Folder** | `EVOLVE-FOLDER` | Autonomously evolve folder: debt, docs, locales, verify |

Secondary actions: **Kernel Health** (live `GET /health`), **Entropy Scan** (local debt report).

## Inspiration Forge

Plan features by mining patterns across **your selected codebases**:

1. Enter one folder path per line (old repos, forks, experiments).
2. Optional **feature hint** (e.g. real-time chat WebSocket).
3. **Scan & Plan** — runs `scripts/inspiration_scanner.py`.
4. **Send Plan to Composer** — dispatches `[PROTOCOL: INSPIRATION-PLAN]`.
5. **Evolve Project Folder** — autonomous folder evolution protocol.

Save personal roots in **workspace** settings (`utahOmniViewport.inspirationRoots`) — never commit.

## MCP sensory mesh (Golden Master subagents)

| Server | Script | Role |
|--------|--------|------|
| `utahclaw_ambient_mesh` | `utahclaw_mcp_bridge.py` | Epistemic void research, harvest |
| `utah_godeye` | `mcp_godeye.py` | AST dependency graph |
| `utah_deployer` | `mcp_deployer.py` | Live container deploy + verify |
| `zeo_entropy` | `mcp_zeo_entropy.py` | Autonomic debt pruner |
| `zeo_akashic_adr` | `mcp_akashic_adr.py` | Immutable ADR writer |

### ZEO-Entropy

Scans cyclomatic/cognitive complexity. Flags functions above threshold (default: 4).

```
zeo_entropy.scan_project_entropy
zeo_entropy.suggest_collapse_targets
```

### Akashic ADR

Writes immutable records to `.cursor/adr/`. Auto-updates `INDEX.md` and `.cursor/memory.md`.

```
zeo_akashic_adr.log_architectural_decision
zeo_akashic_adr.log_schism_decision
```

## Example workflow (Schism)

1. Open **Command Deck** → click **Schism** → enter `tycoon_settlement`.
2. God-Eye maps blast radius via MCP.
3. Agent extracts UtahContainerEngine microservice.
4. Rewrites kernel imports to RPC/REST.
5. Akashic-ADR documents the schism.
6. Click **Immortalize** → tests + commit command (commit only if you ask).

## Configuration

| File | Scope | Commit? |
|------|-------|---------|
| `.cursor/mcp.json` | Project MCP servers | Yes |
| `~/.cursor/mcp.json` | Global MCP (personal) | **No** — stays on your machine |
| `.cursorrules` | L6 Omni-Compiler directive | Yes |
| `.cursor/memory.md` | Epigenetic memory | Yes |
| `.cursor/user.json` | Personal overrides | **No** — gitignored |
| `.vscode/settings.json` | Personal editor prefs | **No** — use `settings.json.example` |

## Setup

1. `pip install -r requirements.txt` (includes `mcp`)
2. Install extension: `.\scripts\install-omni-viewport.ps1` (Windows) or **Developer: Install Extension from Location** → `extensions/utah-omni-viewport`
3. `Ctrl+Shift+J` → enable all `utah_*` and `zeo_*` MCP servers
4. **Developer: Reload Window**
5. Activity bar → **Omni-Viewport** → Command Deck

## Related

- [Omni-Viewport Extension](OMNI_VIEWPORT_EXTENSION.md)
- [Omni-Desk](OMNI_DESK.md)
- [MCP Omni-Bridge](MCP_OMNI_BRIDGE.md)
- [Local Development](LOCAL_DEVELOPMENT.md)
