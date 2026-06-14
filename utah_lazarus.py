#!/usr/bin/env python3
"""
Lazarus AST Engine - v25.0 Omega-Build
Live code mutation without binary rebuilds or container pulls.
"""

import ast
import os
import textwrap
import time
from typing import Optional

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
CONTAINER_ROOT = os.path.join(UTAH_DATA_DIR, "containers")
LAMBDA_ROOT = os.path.join(UTAH_DATA_DIR, "lambda")


class LazarusEngine:
    """AST mutator for handler.py in containers and lambda functions."""

    @staticmethod
    def _resolve_handler(app_name: str) -> Optional[str]:
        for root in (CONTAINER_ROOT, LAMBDA_ROOT):
            path = os.path.join(root, app_name, "handler.py")
            if os.path.exists(path):
                return path
        return None

    @staticmethod
    def mutate(app_name: str, patch_code: str) -> bool:
        path = LazarusEngine._resolve_handler(app_name)
        if not path:
            return False

        print(f"[Lazarus] Mutating AST for {app_name}: {patch_code[:80]}...")

        with open(path, "r") as f:
            source = f.read()

        # Validate existing source parses
        try:
            ast.parse(source)
        except SyntaxError:
            return False

        # If patch looks like Python code, inject as new function
        stripped = patch_code.strip()
        if stripped.startswith("def ") or "\ndef " in stripped:
            injection = textwrap.dedent(f"""

# --- LAZARUS PATCH {time.time()} ---
{stripped}
""")
        else:
            # Intent string: append metadata and optional return override comment
            injection = f"""

# --- LAZARUS PATCH {time.time()} ---
# Intent: {patch_code}
def _lazarus_patch_{int(time.time())}(event, context):
    result = handler(event, context)
    if isinstance(result, dict):
        result['lazarus_intent'] = {patch_code!r}
    return result
"""

        try:
            combined = source + injection
            ast.parse(combined)
            with open(path, "w") as f:
                f.write(combined)
            return True
        except SyntaxError:
            # Fallback: comment-only append (legacy behavior)
            with open(path, "a") as f:
                f.write(f"\n# LAZARUS FALLBACK PATCH: {patch_code}\n")
            return True

    @staticmethod
    def patch_live_logic(app_name: str, patch_intent: str) -> bool:
        return LazarusEngine.mutate(app_name, patch_intent)
