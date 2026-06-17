#!/usr/bin/env python3
"""
UtahMosphere Omni-Compiler v3.0 (Sovereign Edition)
Agentic intent engine — translates developer intent into live hardware reality.
"""

import json
import os
import re
from typing import Any, Dict, Optional

from omni_glass import omni_glass
from utah_omni_mind import UTAH_KERNEL_PRIMITIVES, omni_mind

try:
    from utahclaw.epistemic_void import EpistemicVoid, is_epistemic_void_intent
    from utahclaw.ambient_runner import ambient_runner
    from chrono_state import chrono_state
except ImportError:
    EpistemicVoid = None  # type: ignore
    is_epistemic_void_intent = lambda _i: False  # type: ignore
    ambient_runner = None  # type: ignore
    chrono_state = None  # type: ignore

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
CONTAINER_ROOT = os.path.join(UTAH_DATA_DIR, "containers")
OMNI_EXEC_ENFORCE = os.environ.get("UTAH_OMNI_EXEC_ENFORCE", "1") != "0"


def _parse_blueprint(raw: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
    return None


def _safe_exec_post_script(script: str, kernel_ref: Any, app_name: str):
    """Execute LLM post-deploy script in a restricted namespace."""
    if not script or not script.strip():
        return
    if not OMNI_EXEC_ENFORCE:
        omni_glass.record("exec", "post_deploy_script skipped (UTAH_OMNI_EXEC_ENFORCE=0)")
        return
    namespace = {
        "kernel": kernel_ref,
        "app_name": app_name,
        "os": os,
        "__builtins__": {"print": print, "len": len, "str": str, "int": int},
    }
    try:
        if chrono_state and kernel_ref:
            import types

            mod = types.ModuleType(f"omni_post_{app_name}")
            mod.__dict__["handler"] = lambda e, c: {"status": "pre-mutation"}
            chrono_state.execute_with_rewind(mod, script, {"app": app_name})
        else:
            exec(script, namespace, namespace)  # noqa: S102
        omni_glass.log_thought_vector("Omni-Compiler", f"post_deploy for {app_name}", "exec")
    except Exception as exc:
        omni_glass.record("error", f"post_deploy_script failed: {exc}")


class SovereignOmniCompiler:
    """Manifests LLM blueprints directly onto sovereign hardware."""

    @staticmethod
    def manifest_blueprint(blueprint: Dict[str, Any], kernel_ref: Any = None) -> Dict[str, Any]:
        app_name = blueprint.get("app_name", "omni-app")
        app_dir = os.path.join(CONTAINER_ROOT, app_name)
        os.makedirs(app_dir, exist_ok=True)
        omni_glass.record("synthesize", f"Synthesizing {app_name} from intent blueprint...")

        written = []
        for file_spec in blueprint.get("files_to_write", []):
            rel = file_spec.get("path", "handler.py")
            file_path = os.path.join(app_dir, rel)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            content = file_spec.get("content", "")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            written.append(rel)
            omni_glass.record("write", f"Wrote {rel}", tool="write_file_to_disk", payload={"path": rel})

        if kernel_ref and hasattr(kernel_ref, "manifest_utah_container"):
            msg = kernel_ref.manifest_utah_container(app_name)
            omni_glass.record("deploy", msg, payload={"app_name": app_name})
        else:
            msg = f"Files written to {app_dir}"

        _safe_exec_post_script(blueprint.get("post_deploy_script", ""), kernel_ref, app_name)
        omni_glass.record("complete", f"Intent manifested: {app_name}")
        return {"ok": True, "app_name": app_name, "files": written, "message": msg}

    @staticmethod
    def process_developer_intent(intent_transcript: str, kernel_ref: Any = None) -> Dict[str, Any]:
        omni_glass.log_thought_vector("Omni-Compiler", f"Analyzing: {intent_transcript[:100]}", "generate_blueprint")

        if is_epistemic_void_intent(intent_transcript) and ambient_runner:
            omni_glass.log_thought_vector("Omni-Compiler", "Epistemic void — waking UtahClaw", "claw_void")
            return ambient_runner.dispatch_void(intent_transcript, kernel_ref)

        raw = omni_mind.generate_intent_blueprint(UTAH_KERNEL_PRIMITIVES, intent_transcript)
        blueprint = _parse_blueprint(raw)
        if not blueprint:
            omni_glass.record("error", "Omni-Mind output was not valid JSON")
            return {"ok": False, "error": "invalid_blueprint", "raw": raw[:500]}

        if blueprint.get("error") == "UNKNOWN_CAPABILITY" and ambient_runner:
            return ambient_runner.dispatch_void(intent_transcript, kernel_ref)

        return SovereignOmniCompiler.manifest_blueprint(blueprint, kernel_ref)


class OmniCompiler(SovereignOmniCompiler):
    """Alias for SovereignOmniCompiler (v1/v3 unified API)."""

    pass


omni_compiler = SovereignOmniCompiler()
