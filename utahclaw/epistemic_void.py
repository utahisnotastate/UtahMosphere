#!/usr/bin/env python3
"""Epistemic void — emitted when Omni-Compiler lacks capability for an intent."""


class EpistemicVoid(Exception):
    """Raised when the Omni-Mind cannot resolve an intent without external research."""

    def __init__(self, concept: str, *, reason: str = "UNKNOWN_CAPABILITY"):
        self.concept = concept
        self.reason = reason
        super().__init__(f"Epistemic void [{reason}]: {concept}")


# Integration keywords not covered by built-in heuristics → trigger UtahClaw research
_VOID_KEYWORDS = (
    "stripe", "graphql", "twilio", "salesforce", "hubspot", "shopify",
    "kubernetes", "terraform", "jenkins", "datadog", "snowflake",
    "unknown api", "new api", "integrate with",
)


def is_epistemic_void_intent(intent: str) -> bool:
    """Return True when intent likely requires UtahClaw background research."""
    text = intent.lower()
    return any(kw in text for kw in _VOID_KEYWORDS)
