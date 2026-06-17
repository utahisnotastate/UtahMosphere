#!/usr/bin/env python3
"""
UtahClaw MCP bridge for Cursor Level 6.
Delegates epistemic void research and codebase harvest to UtahClaw (port 9090).
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

CLAW_BASE = os.environ.get("UTAH_CLAW_BASE", "http://127.0.0.1:9090").rstrip("/")


def _http_json(method: str, path: str, body: dict | None = None) -> dict:
    data = None
    headers = {"Content-Type": "application/json", "User-Agent": "utahclaw-mcp-bridge/1.0"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{CLAW_BASE}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {"ok": True}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            return json.loads(detail)
        except json.JSONDecodeError:
            return {"ok": False, "error": detail or str(exc), "status": exc.code}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def research_void(concept: str) -> str:
    result = _http_json("POST", "/void", {"concept": concept})
    return json.dumps(result, indent=2)


def harvest_codebase(path: str) -> str:
    result = _http_json("POST", "/harvest", {"path": path})
    return json.dumps(result, indent=2)


def claw_status() -> str:
    result = _http_json("GET", "/status")
    return json.dumps(result, indent=2)


def fetch_documentation(query: str) -> str:
    """Dispatch void research for unknown API/library surface."""
    void = _http_json("POST", "/void", {"concept": f"Documentation research: {query}"})
    status = _http_json("GET", "/status")
    return json.dumps({"void_dispatch": void, "claw_status": status}, indent=2)


async def _run_mcp_server():
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp import types

    server = Server("utahclaw_ambient_mesh")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="research_void",
                description="Dispatch UtahClaw to research an unknown API, library, or integration. Use when confidence < 100%.",
                inputSchema={
                    "type": "object",
                    "properties": {"concept": {"type": "string", "description": "Capability or API to research"}},
                    "required": ["concept"],
                },
            ),
            types.Tool(
                name="fetch_documentation",
                description="Fetch current documentation via UtahClaw epistemic void protocol.",
                inputSchema={
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="harvest_codebase",
                description="Harvest reusable features from a repo into MCP tools (horizontal gene transfer).",
                inputSchema={
                    "type": "object",
                    "properties": {"path": {"type": "string", "description": "Absolute or relative repo path"}},
                    "required": ["path"],
                },
            ),
            types.Tool(
                name="claw_status",
                description="UtahClaw ambient runner status, pending research, forged tools.",
                inputSchema={"type": "object", "properties": {}},
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        args = arguments or {}
        if name == "research_void":
            text = research_void(args.get("concept", ""))
        elif name == "fetch_documentation":
            text = fetch_documentation(args.get("query", ""))
        elif name == "harvest_codebase":
            text = harvest_codebase(args.get("path", ""))
        elif name == "claw_status":
            text = claw_status()
        else:
            text = json.dumps({"ok": False, "error": f"unknown_tool: {name}"})
        return [types.TextContent(type="text", text=text)]

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    try:
        import mcp  # noqa: F401
    except ImportError:
        print(
            "Install MCP SDK: pip install mcp",
            file=sys.stderr,
        )
        sys.exit(1)

    import asyncio

    asyncio.run(_run_mcp_server())


if __name__ == "__main__":
    main()
