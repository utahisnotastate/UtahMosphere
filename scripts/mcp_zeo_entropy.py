#!/usr/bin/env python3
"""
ZEO-Entropy MCP — autonomous technical debt scanner for Cursor Level 6.
Calculates cyclomatic/cognitive complexity and flags entropy hotspots.
"""

from __future__ import annotations

import ast
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

from mcp.server.fastmcp import FastMCP

ROOT = Path(os.environ.get("UTAH_REPO_ROOT", Path(__file__).resolve().parents[1]))
ENTROPY_THRESHOLD = int(os.environ.get("ZEO_ENTROPY_THRESHOLD", "4"))
SKIP_DIRS = {".git", ".utah-data", "__pycache__", "node_modules", ".venv", "venv"}

mcp = FastMCP("ZEO-Entropy")


@dataclass
class FunctionEntropy:
    file: str
    name: str
    complexity: int
    lineno: int
    lines: int


@dataclass
class EntropyReport:
    scanned_files: int = 0
    skipped_files: int = 0
    hotspots: List[FunctionEntropy] = field(default_factory=list)

    def top(self, n: int = 10) -> List[FunctionEntropy]:
        return sorted(self.hotspots, key=lambda h: (-h.complexity, -h.lines))[:n]


def _cognitive_complexity(node: ast.AST) -> int:
    """Branch/loop/except/nested boolean complexity for a function body."""
    score = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)):
            score += 1
        elif isinstance(child, ast.BoolOp):
            score += max(1, len(child.values) - 1)
        elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            score += 1
    return score


def _analyze_file(path: Path) -> Tuple[List[FunctionEntropy], bool]:
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(path))
    except (OSError, SyntaxError):
        return [], False

    rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    source_lines = source.splitlines()
    found: List[FunctionEntropy] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        complexity = _cognitive_complexity(node)
        end = getattr(node, "end_lineno", node.lineno) or node.lineno
        span = max(1, end - node.lineno + 1)
        if complexity >= ENTROPY_THRESHOLD or span >= 80:
            found.append(FunctionEntropy(rel, node.name, complexity, node.lineno, span))

    return found, True


def _iter_python_files(directory: str) -> List[Path]:
    base = ROOT / directory if not Path(directory).is_absolute() else Path(directory)
    if base.is_file() and base.suffix == ".py":
        return [base.resolve()]
    files: List[Path] = []
    for path in base.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def _build_report(directory: str = ".") -> EntropyReport:
    report = EntropyReport()
    for path in _iter_python_files(directory):
        hotspots, ok = _analyze_file(path)
        if ok:
            report.scanned_files += 1
            report.hotspots.extend(hotspots)
        else:
            report.skipped_files += 1
    return report


def _format_report(report: EntropyReport, top_n: int = 10) -> str:
    top = report.top(top_n)
    if not top:
        return "[ZEO-Entropy] Codebase is crystalline. Zero debt detected above threshold."

    lines = [
        f"[ZEO-Entropy] Scanned {report.scanned_files} files (skipped {report.skipped_files}).",
        f"Threshold: complexity>={ENTROPY_THRESHOLD} or span>=80 lines.",
        "High structural debt:",
    ]
    for h in top:
        lines.append(
            f"  - {h.file}:{h.lineno} `{h.name}` complexity={h.complexity} lines={h.lines}"
        )
    lines.append("Suggest: Command Deck Entropy Purge or collapse worst offenders.")
    return "\n".join(lines)


@mcp.tool()
def scan_project_entropy(directory: str = ".") -> str:
    """Subagent: Scan directory for structural entropy (high cyclomatic complexity). Returns refactor targets."""
    report = _build_report(directory)
    return _format_report(report, top_n=15)


@mcp.tool()
def scan_file_entropy(target_file: str) -> str:
    """Scan a single Python file for entropy hotspots."""
    path = ROOT / target_file if not Path(target_file).is_absolute() else Path(target_file)
    hotspots, ok = _analyze_file(path.resolve())
    if not ok:
        return json.dumps({"ok": False, "error": f"cannot_parse: {target_file}"})
    return json.dumps({
        "ok": True,
        "file": target_file,
        "hotspots": [h.__dict__ for h in sorted(hotspots, key=lambda x: -x.complexity)],
    }, indent=2)


@mcp.tool()
def suggest_collapse_targets(directory: str = ".", limit: int = 3) -> str:
    """Return top N functions to collapse via ENTROPY-PURGE protocol (JSON for Agent consumption)."""
    report = _build_report(directory)
    top = report.top(limit)
    return json.dumps({
        "threshold": ENTROPY_THRESHOLD,
        "targets": [h.__dict__ for h in top],
        "protocol": "[PROTOCOL: ENTROPY-PURGE] — rewrite using functional dispatch, early returns, extract helpers",
        "crystalline": len(top) == 0,
    }, indent=2)


@mcp.tool()
def entropy_summary_json(directory: str = ".") -> str:
    """Machine-readable entropy report for autonomic subagents."""
    report = _build_report(directory)
    return json.dumps({
        "scanned_files": report.scanned_files,
        "skipped_files": report.skipped_files,
        "hotspot_count": len(report.hotspots),
        "top_hotspots": [h.__dict__ for h in report.top(20)],
    }, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
