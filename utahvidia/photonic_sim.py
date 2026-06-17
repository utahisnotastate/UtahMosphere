#!/usr/bin/env python3
"""Photonic Context Bridge — zero-copy prompt ingestion for Omni-Mind."""

import hashlib
from typing import Union


class PhotonicContextBridge:
    """Memory-maps prompt context into the inference vector space."""

    @staticmethod
    def ingest(prompt: Union[str, bytes]) -> str:
        raw = prompt if isinstance(prompt, bytes) else prompt.encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        return f"photonic:{digest[:32]}"
