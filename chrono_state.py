#!/usr/bin/env python3
"""
Chrono-State Engine — speculative AI mutation with timeline rewind.
Obsoletes CI/CD staging: test on live requests, rewind on failure.
"""

import copy
import os
import types
from typing import Any, Callable, Dict, Optional

CHRONO_ENFORCE = os.environ.get("UTAH_CHRONO_ENFORCE", "1") != "0"

try:
    from omni_glass import omni_glass
except ImportError:
    omni_glass = None  # type: ignore

try:
    from utahclaw.epistemic_void import EpistemicVoid
    from utahclaw.ambient_runner import ambient_runner
except ImportError:
    EpistemicVoid = None  # type: ignore
    ambient_runner = None  # type: ignore


class ChronoStateEngine:
    """Execute generated code with memory snapshot + rewind on paradox."""

    @staticmethod
    def execute_with_rewind(
        target_module: types.ModuleType,
        generated_code: str,
        request_context: dict,
        *,
        handler_name: str = "handler",
        on_void: Optional[Callable[[str, Exception], None]] = None,
    ) -> Any:
        if not CHRONO_ENFORCE or not generated_code or not generated_code.strip():
            handler = getattr(target_module, handler_name, None)
            return handler(request_context, {}) if callable(handler) else None

        safe_state = copy.deepcopy(target_module.__dict__)
        if omni_glass:
            omni_glass.log_lazarus_mutation("Chrono-State", "speculative inject")

        try:
            exec(generated_code, target_module.__dict__)  # noqa: S102
            handler = getattr(target_module, handler_name, None)
            if not callable(handler):
                raise AttributeError(f"{handler_name} not callable after mutation")
            result = handler(request_context, {})
            if omni_glass:
                omni_glass.log_lazarus_mutation("Chrono-State", "mutation committed")
            return result
        except Exception as exc:
            if omni_glass:
                omni_glass.log_lazarus_mutation("Chrono-State", f"rewind: {exc}")
            target_module.__dict__.clear()
            target_module.__dict__.update(safe_state)
            if on_void and ambient_runner:
                on_void(generated_code, exc)
            elif ambient_runner:
                ambient_runner.dispatch_void(
                    f"Fix exception {exc} in generated code",
                )
            handler = getattr(target_module, handler_name, None)
            if callable(handler):
                return handler(request_context, {})
            raise

    @staticmethod
    def snapshot_namespace(namespace: Dict[str, Any]) -> Dict[str, Any]:
        return copy.deepcopy(namespace)

    @staticmethod
    def rewind_namespace(namespace: Dict[str, Any], snapshot: Dict[str, Any]):
        namespace.clear()
        namespace.update(snapshot)

    @staticmethod
    def status() -> dict:
        return {"enforce": CHRONO_ENFORCE, "rewinds": "memory_isolation"}


chrono_state = ChronoStateEngine()
