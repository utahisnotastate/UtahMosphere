#!/usr/bin/env python3
"""
Inspiration Scanner — cross-codebase pattern mining for Omni-Viewport extension.
Scans user-selected folders and returns structured inspiration for feature planning.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Set

SKIP_DIRS = {
    ".git", ".utah-data", "__pycache__", "node_modules", ".venv", "venv",
    "dist", "build", ".cursor", "terminals",
}

PATTERN_TAGS = {
    "auth": re.compile(r"\b(jwt|oauth|hmac|auth|nonce|signature|bearer)\b", re.I),
    "payments": re.compile(r"\b(stripe|bitcoin|mempool|checkout|tycoon|settlement)\b", re.I),
    "mesh": re.compile(r"\b(swarm|gossip|dht|quorum|witness|mesh)\b", re.I),
    "deploy": re.compile(r"\b(deploy|manifest|container|handler\.py)\b", re.I),
    "ai": re.compile(r"\b(omni|compiler|llm|mcp|claw|inference)\b", re.I),
    "ui": re.compile(r"\b(flux|gui|webview|tkinter|css|manifest)\b", re.I),
}


def _iter_source_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in (".py", ".md", ".ts", ".tsx", ".js", ".json"):
            if path.stat().st_size > 500_000:
                continue
            files.append(path)
    return files


def _extract_python_symbols(path: Path) -> List[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (SyntaxError, OSError):
        return []
    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    ][:40]


def _tag_content(text: str) -> Set[str]:
    tags: Set[str] = set()
    for name, regex in PATTERN_TAGS.items():
        if regex.search(text):
            tags.add(name)
    return tags


def scan_directories(directories: List[str], feature_hint: str = "") -> Dict[str, Any]:
    corpus: List[Dict[str, Any]] = []
    tag_index: Dict[str, List[str]] = {k: [] for k in PATTERN_TAGS}

    for raw in directories:
        root = Path(raw).expanduser().resolve()
        if not root.exists():
            continue
        for path in _iter_source_files(root)[:400]:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            tags = _tag_content(text)
            if not tags and path.suffix != ".py":
                continue
            rel = str(path)
            entry = {
                "path": rel,
                "tags": sorted(tags),
                "symbols": _extract_python_symbols(path) if path.suffix == ".py" else [],
                "preview": text[:400].replace("\n", " "),
            }
            corpus.append(entry)
            for tag in tags:
                tag_index[tag].append(rel)

    plan_sections = []
    if feature_hint:
        hint_lower = feature_hint.lower()
        relevant = [
            c for c in corpus
            if any(t in hint_lower for t in c["tags"]) or feature_hint.lower() in c["preview"].lower()
        ][:25]
        if not relevant:
            relevant = corpus[:15]
        plan_sections.append(f"# Feature plan seed: {feature_hint}\n")
        plan_sections.append("## Inspiration from selected codebases\n")
        for item in relevant:
            plan_sections.append(f"- `{item['path']}` tags={item['tags']} symbols={item['symbols'][:5]}")

    return {
        "ok": True,
        "directories": directories,
        "files_scanned": len(corpus),
        "tag_index": {k: v[:20] for k, v in tag_index.items() if v},
        "corpus_sample": corpus[:60],
        "feature_plan_markdown": "\n".join(plan_sections) if plan_sections else "",
    }


def main():
    parser = argparse.ArgumentParser(description="UtahMosphere inspiration scanner")
    parser.add_argument("directories", nargs="*", help="Codebase roots to scan")
    parser.add_argument("--feature", default="", help="Feature description for planning")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    dirs = args.directories or ["."]
    result = scan_directories(dirs, args.feature)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result.get("feature_plan_markdown") or json.dumps(result["tag_index"], indent=2))


if __name__ == "__main__":
    main()
