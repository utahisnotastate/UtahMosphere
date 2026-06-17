#!/usr/bin/env python3
"""
UtahMosphere Kernel Primitives — MCP / tool-calling surface for the Omni-Compiler.
"""

import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
CONTAINER_ROOT = os.path.join(UTAH_DATA_DIR, "containers")
UTAHX_ROOT = os.path.join(UTAH_DATA_DIR, "utahx_mesh")


def allocate_memory_silo(app_name: str, size_mb: int = 64) -> Dict[str, Any]:
    """Reserve a container namespace directory (memory silo)."""
    silo = os.path.join(CONTAINER_ROOT, app_name)
    os.makedirs(silo, exist_ok=True)
    return {"app_name": app_name, "silo_path": silo, "size_mb": size_mb, "status": "allocated"}


def write_file_to_disk(path: str, content: str, *, base_dir: Optional[str] = None) -> Dict[str, Any]:
    """Write content under UTAH_DATA_DIR (path traversal blocked)."""
    root = Path(base_dir or UTAH_DATA_DIR).resolve()
    target = (root / path).resolve()
    if not str(target).startswith(str(root)):
        return {"ok": False, "error": "path outside sovereign data root"}
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {"ok": True, "path": str(target), "bytes": len(content.encode("utf-8"))}


def read_file_from_disk(path: str, *, base_dir: Optional[str] = None) -> Dict[str, Any]:
    root = Path(base_dir or UTAH_DATA_DIR).resolve()
    target = (root / path).resolve()
    if not str(target).startswith(str(root)) or not target.is_file():
        return {"ok": False, "error": "file not found or outside root"}
    text = target.read_text(encoding="utf-8", errors="replace")
    return {"ok": True, "path": str(target), "content": text[:65536]}


def list_directory(path: str = ".", *, base_dir: Optional[str] = None) -> Dict[str, Any]:
    root = Path(base_dir or UTAH_DATA_DIR).resolve()
    target = (root / path).resolve()
    if not str(target).startswith(str(root)) or not target.is_dir():
        return {"ok": False, "error": "directory not found"}
    entries = sorted(p.name for p in target.iterdir())[:500]
    return {"ok": True, "path": str(target), "entries": entries}


def update_utahx_routing(domain: str, port: int, kernel_ref: Any = None) -> Dict[str, Any]:
    """Register UtahX ingress route for a manifested app."""
    manifest = {
        "ingress_host": domain if "." in domain else f"{domain}.utahmosphere.internal",
        "fluid_proxy_target": f"http://127.0.0.1:{port}",
        "tollbooth_cache": "omni-compiler",
        "buffer_optimization": "high-throughput-ram",
    }
    dest = os.path.join(UTAHX_ROOT, f"{domain.split('.')[0]}.utahx.json")
    os.makedirs(UTAHX_ROOT, exist_ok=True)
    import json

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    if kernel_ref and hasattr(kernel_ref, "cluster_registry"):
        kernel_ref.cluster_registry.setdefault("utahx_routes", {})[domain.split(".")[0]] = manifest
        if hasattr(kernel_ref, "_save_registry_unlocked"):
            kernel_ref._save_registry_unlocked()
    return {"ok": True, "domain": domain, "port": port, "manifest": manifest}


def execute_subprocess(command: str, timeout: float = 30.0) -> Dict[str, Any]:
    """Run a shell command (disabled when UTAH_OMNI_SUBPROCESS_ENFORCE=0)."""
    if os.environ.get("UTAH_OMNI_SUBPROCESS_ENFORCE", "1") == "0":
        return {"ok": False, "error": "subprocess disabled in dev mode"}
    try:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-4096:],
            "stderr": proc.stderr[-4096:],
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


PRIMITIVE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "allocate_memory_silo",
            "description": "Reserve a container memory silo for an app",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string"},
                    "size_mb": {"type": "integer"},
                },
                "required": ["app_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file_to_disk",
            "description": "Write a file under UTAH_DATA_DIR",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file_from_disk",
            "description": "Read a file from UTAH_DATA_DIR",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List a directory under UTAH_DATA_DIR",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_utahx_routing",
            "description": "Update UtahX ingress routing for an app",
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string"},
                    "port": {"type": "integer"},
                },
                "required": ["domain", "port"],
            },
        },
    },
]


def dispatch_primitive(name: str, arguments: Dict[str, Any], kernel_ref: Any = None) -> Dict[str, Any]:
    if name == "allocate_memory_silo":
        return allocate_memory_silo(**arguments)
    if name == "write_file_to_disk":
        return write_file_to_disk(**arguments)
    if name == "read_file_from_disk":
        return read_file_from_disk(**arguments)
    if name == "list_directory":
        return list_directory(**arguments)
    if name == "update_utahx_routing":
        return update_utahx_routing(**arguments, kernel_ref=kernel_ref)
    if name == "execute_subprocess":
        return execute_subprocess(**arguments)
    return {"ok": False, "error": f"unknown primitive: {name}"}
