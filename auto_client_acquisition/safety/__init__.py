"""Dealix safety primitives — intent classification + safe-channel routing."""

from auto_client_acquisition.safety.intent_classifier import (
    ActionMode,
    IntentDecision,
    Language,
    classify_intent,
)

__all__ = ["ActionMode", "IntentDecision", "Language", "classify_intent"]
