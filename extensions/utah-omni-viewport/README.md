# Utah Omni-Viewport (Cursor / VS Code Extension)

Button-based **Command Deck** and **Inspiration Forge** — no slash commands required.

## Install (Cursor)

### One command (Windows)

From the repo root:

```powershell
.\scripts\install-omni-viewport.ps1
```

Then **Developer: Reload Window** (`Ctrl+Shift+P`). Activity bar → **Omni-Viewport**.

### Manual

`Ctrl+Shift+P` → **Developer: Install Extension from Location** → select `extensions/utah-omni-viewport`

### VSIX (optional)

```powershell
cd extensions\utah-omni-viewport
npx -y @vscode/vsce package --allow-missing-repository
cursor --install-extension .\utah-omni-viewport-1.0.0.vsix
```

## UI

| Panel | Purpose |
|-------|---------|
| **Command Deck** | Cascade, Absorb, Void Fill, Chrono Fix, Entropy Purge, Schism, Vibe Shift, Immortalize, Evolve Folder |
| **Inspiration Forge** | Multi-folder codebase scan + feature planning |

Buttons copy `[PROTOCOL: …]` prompts to the clipboard and open Composer (`Ctrl+I`).

## Settings (workspace — personal paths stay local)

| Setting | Default |
|---------|---------|
| `utahOmniViewport.kernelBase` | `http://127.0.0.1:8999` |
| `utahOmniViewport.pythonPath` | `py` |
| `utahOmniViewport.inspirationRoots` | `[]` (workspace only — do not commit) |

Copy `.vscode/settings.json.example` to your workspace settings if needed.

## Related

- [Cursor Epigenetic IDE](../../docs/CURSOR_EPIGENETIC.md)
- [Omni-Viewport Extension Guide](../../docs/OMNI_VIEWPORT_EXTENSION.md)
- `scripts/inspiration_scanner.py`
