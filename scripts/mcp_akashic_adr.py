#!/usr/bin/env python3
"""
Akashic ADR MCP — immutable Architecture Decision Records for Cursor Level 6.
Documentation is a byproduct of execution, not a separate Jira sprint.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

ROOT = Path(os.environ.get("UTAH_REPO_ROOT", Path(__file__).resolve().parents[1]))
ADR_DIR = ROOT / ".cursor" / "adr"
INDEX_FILE = ADR_DIR / "INDEX.md"
MEMORY_FILE = ROOT / ".cursor" / "memory.md"

mcp = FastMCP("Akashic-ADR")


def _slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", title.strip().lower()).strip("_")
    return slug[:64] or "decision"


def _next_adr_id() -> int:
    if not ADR_DIR.is_dir():
        return 1
    existing = [f for f in ADR_DIR.glob("adr_*.md") if f.is_file()]
    return len(existing) + 1


def _append_memory_note(adr_id: int, title: str, file_path: Path):
    if not MEMORY_FILE.is_file():
        return
    stamp = dt.datetime.now().strftime("%Y-%m-%d")
    line = f"- **{stamp}** ADR-{adr_id:03d}: {title} → `{file_path.relative_to(ROOT).as_posix()}`"
    text = MEMORY_FILE.read_text(encoding="utf-8")
    marker = "## Recent epigenetic mutations"
    if marker not in text:
        return
    head, tail = text.split(marker, 1)
    insertion = f"\n{line}"
    if insertion.strip() not in tail:
        MEMORY_FILE.write_text(head + marker + insertion + tail, encoding="utf-8")


def _rebuild_index():
    ADR_DIR.mkdir(parents=True, exist_ok=True)
    entries: List[str] = ["# Akashic ADR Index\n", "| ID | Date | Title | File |", "|----|------|-------|------|"]
    for path in sorted(ADR_DIR.glob("adr_*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        title_match = re.search(r"^# ADR (\d+): (.+)$", text, re.M)
        date_match = re.search(r"\*\*Date:\*\* (.+)$", text, re.M)
        if title_match:
            entries.append(
                f"| {title_match.group(1)} | {date_match.group(1) if date_match else '-'} "
                f"| {title_match.group(2)} | `{path.name}` |"
            )
    INDEX_FILE.write_text("\n".join(entries) + "\n", encoding="utf-8")


@mcp.tool()
def log_architectural_decision(
    title: str,
    context: str,
    decision: str,
    consequences: str,
) -> str:
    """Write an Architecture Decision Record whenever structure, libraries, or architecture pivot."""
    ADR_DIR.mkdir(parents=True, exist_ok=True)
    adr_id = _next_adr_id()
    slug = _slugify(title)
    file_path = ADR_DIR / f"adr_{adr_id:03d}_{slug}.md"

    adr_content = f"""# ADR {adr_id}: {title}
**Date:** {dt.datetime.now().strftime("%Y-%m-%d")}
**Status:** Accepted

## Context
{context.strip()}

## Decision
{decision.strip()}

## Consequences
{consequences.strip()}
"""
    file_path.write_text(adr_content, encoding="utf-8")
    _rebuild_index()
    _append_memory_note(adr_id, title, file_path)

    return (
        f"[Akashic-ADR] Architectural state preserved in {file_path.relative_to(ROOT).as_posix()}. "
        "Genetic memory updated."
    )


@mcp.tool()
def list_architectural_decisions() -> str:
    """List all ADRs in the Akashic record."""
    if not ADR_DIR.is_dir():
        return json.dumps({"adrs": [], "count": 0})
    adrs = []
    for path in sorted(ADR_DIR.glob("adr_*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^# ADR (\d+): (.+)$", text, re.M)
        if m:
            adrs.append({"id": int(m.group(1)), "title": m.group(2), "file": path.name})
    return json.dumps({"adrs": adrs, "count": len(adrs), "index": "INDEX.md"}, indent=2)


@mcp.tool()
def read_architectural_decision(adr_id: int) -> str:
    """Read a specific ADR by numeric id."""
    matches = list(ADR_DIR.glob(f"adr_{adr_id:03d}_*.md"))
    if not matches:
        return json.dumps({"ok": False, "error": f"adr_not_found: {adr_id}"})
    return matches[0].read_text(encoding="utf-8")


@mcp.tool()
def log_schism_decision(
    module_name: str,
    service_name: str,
    rpc_style: str,
    affected_files: str,
) -> str:
    """Convenience ADR template for Schism monolith decoupling."""
    return log_architectural_decision(
        title=f"Schism: extract {module_name} to {service_name}",
        context=f"Module `{module_name}` decoupled from monolith. Blast radius files: {affected_files}",
        decision=f"Extract `{module_name}` into standalone UtahContainerEngine service `{service_name}` using {rpc_style}.",
        consequences="Original imports rewritten to RPC/REST client. Kernel routes proxy to new container port.",
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
