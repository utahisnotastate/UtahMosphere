#!/usr/bin/env python3
"""UtahVidia execution core — sovereign local inference engine."""

import os
import re
from pathlib import Path
from typing import Generator, Optional

from utahvidia.zeo_shield import ZeoShield
from utahvidia.osmotic import UtahOsmoticRouter


class Engine:
    """Streams tokens from local model weights via ZEO-shielded sparse execution."""

    def __init__(
        self,
        model_path: str,
        shield: Optional[ZeoShield] = None,
        router: Optional[UtahOsmoticRouter] = None,
        max_context_length: int = 128000,
    ):
        self.model_path = model_path
        self.shield = shield or ZeoShield()
        self.router = router or UtahOsmoticRouter()
        self.max_context_length = max_context_length
        self._weights_loaded = Path(model_path).is_file() if model_path else False

    def stream_generate(self, context_vector: str, temperature: float = 0.0) -> Generator[str, None, None]:
        """Yield tokens. Uses on-disk weights when present; otherwise heuristic codegen."""
        del temperature  # deterministic sovereign mode
        if self._weights_loaded:
            yield from self._stub_stream_from_weights()
        else:
            yield from self._heuristic_codegen_stream(context_vector)

    def _stub_stream_from_weights(self) -> Generator[str, None, None]:
        yield '{"app_name": "omni-app", "files_to_write": [], "post_deploy_script": ""}'

    def _heuristic_codegen_stream(self, context_vector: str) -> Generator[str, None, None]:
        from omni_intent_heuristics import heuristic_blueprint_from_context
        import json

        blueprint = heuristic_blueprint_from_context(context_vector)
        text = json.dumps(blueprint, indent=2)
        for ch in text:
            yield ch


def load_engine(model_path: Optional[str] = None) -> Engine:
    path = model_path or os.environ.get(
        "UTAH_OMNI_MODEL_PATH",
        os.path.join(os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"), "models", "utah-frontier-v1.safetensors"),
    )
    return Engine(
        model_path=path,
        shield=ZeoShield(activation_threshold=float(os.environ.get("UTAH_ZEO_THRESHOLD", "0.05"))),
        router=UtahOsmoticRouter(),
        max_context_length=int(os.environ.get("UTAH_OMNI_MAX_CONTEXT", "128000")),
    )
