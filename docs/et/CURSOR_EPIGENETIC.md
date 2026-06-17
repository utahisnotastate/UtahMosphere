# Cursor epigeneetiline IDE (tase 6)

UtahMosphere seadistab Cursori **Omni-Viewport**-ina — mitte tavalise tekstiredaktorina. IDE pärib projekti vaimu epigeneetilisest mälust, **Command Decki nuppudest** ja **autonoomsetest MCP alamagentidest**.

> **Lõikude käske pole.** Paigalda [Utah Omni-Viewporti laiendus](OMNI_VIEWPORT_EXTENSION.md) ja vajuta külgriba nuppe.

## Utah-Archivist (`.cursor/memory.md`)

Iseennast uuendav alateadlik mälu. Agent loeb enne iga tegevust, lisab mustreid autonoomselt, ei küsi luba.

## Omni-Viewport Command Deck

Iga nupp kopeerib `[PROTOCOL: …]` viiba lõikelauale ja avab Composeri (`Ctrl+I`).

| Nupp | Protokoll | Tegevus |
|------|-----------|---------|
| **Cascade Sync** | `CASCADE` | Täielik pinu sünk (kernel, RDS, S3, Flux UI, dokid) |
| **Absorb** | `ABSORB` | Võõraskoodi assimilatsioon Utah pinusse |
| **Void Fill** | `VOID-FILL` | UtahClaw MCP uurimine enne koodi kirjutamist |
| **Chrono Fix** | `CHRONO-FIX` | Terminali vea tagasikerimine |
| **Entropy Purge** | `ENTROPY-PURGE` | Top-3 entroopia kuumkohtade kokkutõmbamine |
| **Schism** | `SCHISM` | Mikroteenuse eraldamine + ADR |
| **Vibe Shift** | `VIBE-SHIFT` | Ainult UI ümberstiilimine |
| **Immortalize** | `IMMORTALIZE` | Testid + ADR + commit käsk |
| **Evolve Folder** | `EVOLVE-FOLDER` | Kausta autonoomne arendamine |

## Inspiration Forge

Planeeri funktsioone, kaevates mustreid **sinu valitud koodibaasidest**.

Isiklikud juurkaustad — ainult tööruumi seadetes (`utahOmniViewport.inspirationRoots`), mitte gitis.

## MCP võrgustik

| Server | Roll |
|--------|------|
| `utahclaw_ambient_mesh` | Void/harvest uurimine |
| `utah_godeye` | AST sõltuvusgraafik |
| `utah_deployer` | Juurutamine + verify |
| `zeo_entropy` | Võla skanner |
| `zeo_akashic_adr` | ADR kirjutaja |

## Seadistamine

1. `pip install -r requirements.txt`
2. **Developer: Install Extension from Location** → `extensions/utah-omni-viewport`
3. Luba MCP serverid (`Ctrl+Shift+J`)
4. Külgriba → **Omni-Viewport**

Vaata [inglise juhendit](../CURSOR_EPIGENETIC.md) ja [laienduse juhendit](OMNI_VIEWPORT_EXTENSION.md).
