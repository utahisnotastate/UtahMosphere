#!/usr/bin/env python3
"""
UtahMosphere Omni-Compiler v2.0 — MCP Context-Aware Build
Model Context Protocol bridge: read filesystem/DB before code generation.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from omni_compiler import SovereignOmniCompiler, _parse_blueprint
from omni_glass import omni_glass
from omni_primitives import (
    PRIMITIVE_TOOLS,
    dispatch_primitive,
    list_directory,
    read_file_from_disk,
)
from utah_omni_mind import UTAH_KERNEL_PRIMITIVES, omni_mind

MCP_ENFORCE = os.environ.get("UTAH_OMNI_MCP_ENFORCE", "1") != "0"


class LocalMCPSession:
    """Fallback MCP server — filesystem tools over UTAH_DATA_DIR."""

    def __init__(self, root: Optional[str] = None):
        self.root = root or os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")

    async def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "read_file",
                "description": "Read a file under the sovereign data root",
                "inputSchema": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            },
            {
                "name": "list_directory",
                "description": "List directory entries under sovereign data root",
                "inputSchema": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                },
            },
        ]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        omni_glass.record("mcp", f"Tool call: {name}", tool=name, payload=arguments)
        if name == "read_file":
            result = read_file_from_disk(arguments.get("path", ""), base_dir=self.root)
            return result.get("content", json.dumps(result))
        if name == "list_directory":
            result = list_directory(arguments.get("path", "."), base_dir=self.root)
            return json.dumps(result)
        mapped = dispatch_primitive(name, arguments)
        return json.dumps(mapped)


class MCPOmniCompiler:
    """Context-aware Omni-Compiler with MCP tool-calling loop."""

    def __init__(self):
        self.system_prompt = (
            UTAH_KERNEL_PRIMITIVES
            + "\nCRITICAL: Before writing code, use MCP tools to inspect files/schemas."
        )

    async def execute_intent(
        self,
        intent: str,
        mcp_server_command: Optional[List[str]] = None,
        kernel_ref: Any = None,
    ) -> Dict[str, Any]:
        if not MCP_ENFORCE:
            return SovereignOmniCompiler.process_developer_intent(intent, kernel_ref)

        omni_glass.record("mcp", "Connecting to local MCP sensory mesh...")
        use_stdio_mcp = mcp_server_command and self._mcp_available()

        if use_stdio_mcp:
            try:
                return await self._execute_with_stdio_mcp(intent, mcp_server_command, kernel_ref)
            except Exception as exc:
                omni_glass.record("error", f"stdio MCP failed: {exc}; falling back to local FS")

        return await self._execute_with_local_mcp(intent, kernel_ref)

    @staticmethod
    def _mcp_available() -> bool:
        try:
            import mcp  # noqa: F401

            return True
        except ImportError:
            return False

    async def _execute_with_local_mcp(self, intent: str, kernel_ref: Any) -> Dict[str, Any]:
        session = LocalMCPSession()
        tools = await session.list_tools()

        # Auto-inspect containers dir when intent mentions database/schema/file
        context_snippets = []
        if any(k in intent.lower() for k in ("database", "schema", "file", "column", "migration", "handler")):
            listing = await session.call_tool("list_directory", {"path": "containers"})
            context_snippets.append(f"containers/: {listing[:2000]}")
            try:
                listing_data = json.loads(listing)
                entries = listing_data.get("entries", []) if listing_data.get("ok") else []
            except json.JSONDecodeError:
                entries = []
            if "handler" in intent.lower() or "utahmosphere" in intent.lower():
                for app in entries[:3]:
                    read = await session.call_tool("read_file", {"path": f"containers/{app}/handler.py"})
                    context_snippets.append(f"--- {app}/handler.py ---\n{read[:4000]}")

        enriched_intent = intent
        if context_snippets:
            enriched_intent += "\n\n[MCP CONTEXT]\n" + "\n".join(context_snippets)

        omni_glass.record("reason", f"MCP-enriched intent ({len(tools)} tools available)")
        return SovereignOmniCompiler.process_developer_intent(enriched_intent, kernel_ref)

    async def _execute_with_stdio_mcp(
        self,
        intent: str,
        mcp_server_command: List[str],
        kernel_ref: Any,
    ) -> Dict[str, Any]:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            return await self._execute_with_local_mcp(intent, kernel_ref)

        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        server_params = StdioServerParameters(
            command=mcp_server_command[0],
            args=mcp_server_command[1:],
            env=None,
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_response = await session.list_tools()
                available_tools = [
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description or "",
                            "parameters": tool.inputSchema,
                        },
                    }
                    for tool in tools_response.tools
                ]

                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": intent},
                ]
                response = client.chat.completions.create(
                    model=os.environ.get("UTAH_OMNI_OPENAI_MODEL", "gpt-4o"),
                    messages=messages,
                    tools=available_tools,
                )

                if response.choices[0].message.tool_calls:
                    for tool_call in response.choices[0].message.tool_calls:
                        omni_glass.record(
                            "mcp",
                            f"Autonomously inspecting: {tool_call.function.name}",
                            tool=tool_call.function.name,
                        )
                        tool_args = json.loads(tool_call.function.arguments)
                        mcp_result = await session.call_tool(tool_call.function.name, arguments=tool_args)
                        content = mcp_result.content[0].text if mcp_result.content else ""
                        messages.append(response.choices[0].message)
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": content,
                            }
                        )

                    final_response = client.chat.completions.create(
                        model=os.environ.get("UTAH_OMNI_OPENAI_MODEL", "gpt-4o"),
                        messages=messages,
                        response_format={"type": "json_object"},
                    )
                    raw = final_response.choices[0].message.content or "{}"
                else:
                    raw = response.choices[0].message.content or "{}"

                blueprint = _parse_blueprint(raw)
                if blueprint:
                    return SovereignOmniCompiler.manifest_blueprint(blueprint, kernel_ref)
                return {"ok": False, "error": "invalid_blueprint", "raw": raw[:500]}

    def execute_intent_sync(
        self,
        intent: str,
        mcp_server_command: Optional[List[str]] = None,
        kernel_ref: Any = None,
    ) -> Dict[str, Any]:
        return asyncio.run(self.execute_intent(intent, mcp_server_command, kernel_ref))


mcp_omni_compiler = MCPOmniCompiler()
