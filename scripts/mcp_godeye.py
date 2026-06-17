#!/usr/bin/env python3
"""
Utah-GodEye MCP — real-time AST dependency graph for Cursor Level 6.
"""

from __future__ import annotations

import ast
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Set

from mcp.server.fastmcp import FastMCP

ROOT = Path(os.environ.get("UTAH_REPO_ROOT", Path(__file__).resolve().parents[1]))
KERNEL_FILE = ROOT / "utahmosphere_os.py"

mcp = FastMCP("Utah-GodEye")


def _resolve_path(target_file: str) -> Path:
    p = Path(target_file)
    if not p.is_absolute():
        p = ROOT / p
    return p.resolve()


def _parse_python_file(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {"ok": False, "error": f"not_found: {path}"}
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return {"ok": False, "error": f"syntax_error: {exc}", "file": str(path)}

    imports: List[str] = []
    functions: List[str] = []
    classes: List[str] = []
    calls: Set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                imports.append(f"{mod}.{alias.name}" if mod else alias.name)
        elif isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_"):
                functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)

    return {
        "ok": True,
        "file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "imports": sorted(set(imports)),
        "functions": functions,
        "classes": classes,
        "call_symbols": sorted(calls),
        "line_count": source.count("\n") + 1,
    }


def _scan_routes_in_kernel() -> List[str]:
    routes: List[str] = []
    if not KERNEL_FILE.is_file():
        return routes
    text = KERNEL_FILE.read_text(encoding="utf-8", errors="replace")
    for match in re.finditer(r'path\s*==\s*["\']([^"\']+)["\']', text):
        routes.append(match.group(1))
    for match in re.finditer(r'path\.startswith\(["\']([^"\']+)["\']\)', text):
        routes.append(match.group(1) + "*")
    return sorted(set(routes))


def _find_refs(symbol: str, limit: int = 40) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    pattern = re.compile(re.escape(symbol))
    for py_file in ROOT.rglob("*.py"):
        if ".utah-data" in py_file.parts or "__pycache__" in py_file.parts:
            continue
        try:
            lines = py_file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                hits.append({
                    "file": str(py_file.relative_to(ROOT)),
                    "line": i,
                    "text": line.strip()[:120],
                })
                if len(hits) >= limit:
                    return hits
    return hits


@mcp.tool()
def map_ast_dependencies(target_file: str) -> str:
    """Subagent: AST scan of target file — imports, functions, classes, call symbols. Use before refactoring."""
    path = _resolve_path(target_file)
    analysis = _parse_python_file(path)
    if not analysis.get("ok"):
        return json.dumps(analysis, indent=2)

    module_stem = path.stem
    refs = _find_refs(module_stem, limit=15)
    routes = [r for r in _scan_routes_in_kernel() if module_stem.replace("_", "") in r.replace("/", "").replace("_", "")]

    graph = {
        **analysis,
        "module_stem": module_stem,
        "kernel_routes_related": routes,
        "workspace_references": refs,
        "mcp_hint": "Call find_symbol_references for each function before renaming.",
    }
    return json.dumps(graph, indent=2)


@mcp.tool()
def scan_kernel_routes() -> str:
    """Return all HTTP route paths registered in utahmosphere_os.py SovereignIngressMultiplexer."""
    return json.dumps({
        "kernel": str(KERNEL_FILE.relative_to(ROOT)),
        "routes": _scan_routes_in_kernel(),
        "ingress_port": 8999,
    }, indent=2)


@mcp.tool()
def find_symbol_references(symbol: str, limit: int = 30) -> str:
    """Find workspace references to a function, class, or variable name."""
    return json.dumps({
        "symbol": symbol,
        "references": _find_refs(symbol, limit=limit),
        "count": len(_find_refs(symbol, limit=limit)),
    }, indent=2)


@mcp.tool()
def map_import_graph(target_file: str, depth: int = 1) -> str:
    """Recursive local import graph (project-relative Python modules only)."""
    path = _resolve_path(target_file)
    visited: Set[str] = set()
    graph: Dict[str, Any] = {}

    def walk(p: Path, d: int):
        key = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
        if key in visited or d < 0:
            return
        visited.add(key)
        info = _parse_python_file(p)
        graph[key] = info
        if d == 0:
            return
        for imp in info.get("imports", []):
            candidate = ROOT / f"{imp.replace('.', '/')}.py"
            if candidate.is_file():
                walk(candidate, d - 1)

    walk(path, depth)
    return json.dumps({"root": str(path), "depth": depth, "graph": graph}, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
