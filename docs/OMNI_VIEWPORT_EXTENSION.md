# Utah Omni-Viewport Extension

The **Utah Omni-Viewport** is a Cursor / VS Code extension that replaces slash commands with **clickable GUI panels** for Level-6 UtahMosphere workflows.

Source: `extensions/utah-omni-viewport/`

## Install

### Windows (recommended)

```powershell
.\scripts\install-omni-viewport.ps1
```

Reload Cursor, then open the **Omni-Viewport** icon in the activity bar.

### Cursor / VS Code

1. Open the repo in Cursor.
2. `Ctrl+Shift+P` → **Developer: Install Extension from Location**
3. Select `extensions/utah-omni-viewport`
4. Reload the window.

Verify: `cursor --list-extensions` should show `utahmosphere.utah-omni-viewport`.

## Activity bar panels

| Panel | Purpose |
|-------|---------|
| **Command Deck** | One-click Level-6 protocols (Cascade, Absorb, Void Fill, …) |
| **Inspiration Forge** | Cross-codebase scan + feature planning |

Open via the **Omni-Viewport** icon in the activity bar, or:

- `Ctrl+Shift+P` → **Utah: Open Command Deck**
- `Ctrl+Shift+P` → **Utah: Open Inspiration Forge**

## Command Deck

Optional text field: module name, feature intent, aesthetic, or foreign code path.

| Button | What it does |
|--------|----------------|
| Cascade Sync | Full-stack holographic change trace |
| Absorb | Assimilate external code into Utah stack |
| Void Fill | UtahClaw research before writing code |
| Chrono Fix | Debug from last terminal failure |
| Entropy Purge | Rewrite top complexity hotspots |
| Schism | Microservice extraction + ADR |
| Vibe Shift | UI-only restyle |
| Immortalize | Tests + ADR + commit command |
| Evolve Folder | Autonomous folder evolution |
| Kernel Health | `GET {kernelBase}/health` |
| Entropy Scan | Local `zeo_entropy` report |

Each protocol button builds a `[PROTOCOL: NAME]` block, copies it to the clipboard, and attempts to open Composer.

## Inspiration Forge

Mine inspiration from **multiple local codebases** you choose:

```
C:\code\OldChatApp
C:\code\LegacyPayments
D:\experiments\websocket-poc
```

1. **+ Workspace** — append current repo root.
2. Enter a **feature hint** (optional).
3. **Scan & Plan** — `scripts/inspiration_scanner.py` tags auth, mesh, UI, deploy, AI patterns.
4. Review the markdown plan in the panel.
5. **Send Plan to Composer** — `[PROTOCOL: INSPIRATION-PLAN]` with your scan results.
6. **Evolve Project Folder** — kick off autonomous evolution on the workspace.

### Scanner CLI

```bash
py scripts/inspiration_scanner.py C:\code\RepoA C:\code\RepoB --feature "real-time chat" --json
```

## Settings

Copy `.vscode/settings.json.example` to your **user or workspace** settings (do not commit personal `settings.json`).

| Setting | Default | Notes |
|---------|---------|-------|
| `utahOmniViewport.kernelBase` | `http://127.0.0.1:8999` | Kernel health probes |
| `utahOmniViewport.pythonPath` | `py` | Windows: use `py`, not `python` |
| `utahOmniViewport.inspirationRoots` | `[]` | **Workspace only** — personal paths |

## Privacy

| Keep local (never commit) | Safe in repo |
|---------------------------|--------------|
| `~/.cursor/mcp.json` | `.cursor/mcp.json` |
| `~/.cursor/User/settings.json` | `.vscode/settings.json.example` |
| `.cursor/user.json` | `.cursorrules`, `.cursor/memory.md` |
| Workspace `inspirationRoots` with your disk paths | Extension source + docs |

## Related

- [Cursor Epigenetic IDE](CURSOR_EPIGENETIC.md)
- [UtahClaw](UTAH_CLAW.md)
- Extension README: `extensions/utah-omni-viewport/README.md`
