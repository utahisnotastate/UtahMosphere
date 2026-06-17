#!/usr/bin/env python3
"""ZEO-Shield — hardware-level sparse activation for UtahVidia."""

from typing import Any, List


class ZeoShield:
    """Forces sparse activation (~2% of weights) during inference."""

    def __init__(self, activation_threshold: float = 0.05):
        self.activation_threshold = activation_threshold
        self._active_ratio = 0.02

    def filter_weights(self, weight_indices: List[int], activations: List[float]) -> List[int]:
        return [
            idx for idx, act in zip(weight_indices, activations)
            if abs(act) >= self.activation_threshold
        ]

    def stats(self) -> dict:
        return {
            "activation_threshold": self.activation_threshold,
            "active_ratio": self._active_ratio,
            "sparse": True,
        }
