# Utah Omni-Viewport (Cursor / VS Code Extension)

Button-based **Command Deck** and **Inspiration Forge** — no slash commands required.

## Install (Cursor)

1. Open **Extensions** (`Ctrl+Shift+X`)
2. Click **...** → **Install from VSIX...** OR **Load Extension**
3. Choose folder: `extensions/utah-omni-viewport`

For development:

```bash
# From repo root — symlink or open folder in Cursor
code --extensionDevelopmentPath=extensions/utah-omni-viewport
```

Or in Cursor: **Developer: Install Extension from Location** → select `extensions/utah-omni-viewport`.

## UI

Activity bar → **Omni-Viewport** icon:

| Panel | Purpose |
|-------|---------|
| **Command Deck** | Buttons: Cascade, Absorb, Void Fill, Chrono Fix, Entropy Purge, Schism, Vibe Shift, Immortalize, Evolve Folder |
| **Inspiration Forge** | Multi-folder codebase scan + feature planning |

Buttons copy structured prompts to clipboard and open Composer (`Ctrl+I`).

## Settings (workspace — personal paths stay local)

`utahOmniViewport.inspirationRoots` — save in **Workspace** settings, not committed.

| Setting | Default |
|---------|---------|
| `utahOmniViewport.kernelBase` | `http://127.0.0.1:8999` |
| `utahOmniViewport.pythonPath` | `py` |

## Related

- [Cursor Epigenetic IDE](../../docs/CURSOR_EPIGENETIC.md)
- [Omni-Viewport Extension Guide](../../docs/OMNI_VIEWPORT_EXTENSION.md)
- `scripts/inspiration_scanner.py`
