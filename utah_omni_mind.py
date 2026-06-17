#!/usr/bin/env python3
"""
UtahMosphere Omni-Mind Engine v1.0
Sovereign replacement for OpenAI/Anthropic APIs — powered by UtahVidia.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional

from omni_intent_heuristics import heuristic_blueprint
from omni_glass import omni_glass

OMNI_PROVIDER = os.environ.get("UTAH_OMNI_PROVIDER", "sovereign").lower()
OMNI_ENFORCE = os.environ.get("UTAH_OMNI_ENFORCE", "1") != "0"
LOCAL_MODEL_PATH = os.environ.get(
    "UTAH_OMNI_MODEL_PATH",
    os.path.join(os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere"), "models", "utah-frontier-v1.safetensors"),
)

UTAH_KERNEL_PRIMITIVES = """
You are the UtahMosphere Omni-Compiler. You replace GCP and AWS.
Your job is to translate user intent into executable Python code.
You have access to hardware primitives via utahmosphere_master.py:
- UtahKernel.manifest_utah_container(app_name)
- LazarusEngine.mutate(app_name, patch_code)
- omni_primitives.write_file_to_disk(path, content)

Do not return conversational text. Return ONLY a valid JSON object:
{
    "app_name": "string",
    "files_to_write": [{"path": "string", "content": "string"}],
    "post_deploy_script": "string (valid python code to execute)"
}
"""

try:
    import utahvidia.core as uv_core
    from utahvidia.zeo_shield import ZeoShield
    from utahvidia.osmotic import UtahOsmoticRouter
    from utahvidia.photonic_sim import PhotonicContextBridge
except ImportError:
    uv_core = None  # type: ignore
    ZeoShield = None  # type: ignore
    UtahOsmoticRouter = None  # type: ignore
    PhotonicContextBridge = None  # type: ignore


class UtahOmniMind:
    """Local inference engine — UtahVidia when available, heuristics otherwise."""

    def __init__(self):
        self._engine = None
        self.zeo_shield = ZeoShield(activation_threshold=0.05) if ZeoShield else None
        self.osmotic_mesh = UtahOsmoticRouter() if UtahOsmoticRouter else None
        if uv_core:
            self._engine = uv_core.load_engine(LOCAL_MODEL_PATH)
            omni_glass.record("boot", "[Omni-Mind] UtahVidia execution core online.")
        else:
            omni_glass.record("boot", "[Omni-Mind] Heuristic sovereign mode (no UtahVidia).")

    def generate_intent_blueprint(self, system_prompt: str, user_intent: str) -> str:
        """Replacement for client.chat.completions.create — returns JSON blueprint text."""
        if not OMNI_ENFORCE:
            blueprint = heuristic_blueprint(user_intent)
            return json.dumps(blueprint)

        if OMNI_PROVIDER == "openai":
            return self._openai_blueprint(system_prompt, user_intent)

        prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{user_intent}\n<|assistant|>\n"
        if PhotonicContextBridge:
            ctx = PhotonicContextBridge.ingest(prompt)
            omni_glass.record("reason", f"[Omni-Mind] Photonic ingest {ctx[:24]}...")
        else:
            ctx = prompt

        omni_glass.record("reason", "[Omni-Mind] Collapsing intent waveform into executable reality...")

        if self._engine:
            tokens: List[str] = []
            for token in self._engine.stream_generate(prompt, temperature=0.0):
                tokens.append(token)
            raw = "".join(tokens)
            if self._valid_json_blueprint(raw):
                return raw

        blueprint = heuristic_blueprint(user_intent)
        return json.dumps(blueprint)

    @staticmethod
    def _valid_json_blueprint(text: str) -> bool:
        try:
            data = json.loads(text)
            return isinstance(data, dict) and "app_name" in data
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", text)
            if not match:
                return False
            try:
                data = json.loads(match.group(0))
                return isinstance(data, dict) and "app_name" in data
            except json.JSONDecodeError:
                return False

    @staticmethod
    def _openai_blueprint(system_prompt: str, user_intent: str) -> str:
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            return json.dumps(heuristic_blueprint(user_intent))
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.environ.get("UTAH_OMNI_OPENAI_MODEL", "gpt-4o"),
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"The user says: {user_intent}"},
                ],
            )
            return response.choices[0].message.content or json.dumps(heuristic_blueprint(user_intent))
        except Exception as exc:
            omni_glass.record("error", f"[Omni-Mind] OpenAI fallback: {exc}")
            return json.dumps(heuristic_blueprint(user_intent))

    def status(self) -> Dict[str, Any]:
        return {
            "provider": OMNI_PROVIDER,
            "enforce": OMNI_ENFORCE,
            "model_path": LOCAL_MODEL_PATH,
            "weights_loaded": os.path.isfile(LOCAL_MODEL_PATH),
            "zeo_shield": self.zeo_shield.stats() if self.zeo_shield else None,
            "osmotic": self.osmotic_mesh.stats() if self.osmotic_mesh else None,
            "engine": "utahvidia" if self._engine else "heuristic",
        }


omni_mind = UtahOmniMind()
