"""Deterministic support risk gate.

Maps a ticket category to a risk level and decides whether a ticket is
eligible for an auto-drafted answer. High-risk categories always escalate
and are NEVER auto-answerable — payment, refunds, privacy and angry
customers must reach a human.
"""

from __future__ import annotations

# Categories that always escalate and can never be auto-answered.
HIGH_RISK_CATEGORIES: frozenset[str] = frozenset(
    {"payment", "refund", "privacy_pdpl", "angry_customer", "security"}
)

_MEDIUM_RISK_CATEGORIES: frozenset[str] = frozenset(
    {"billing", "technical_issue", "connector_setup"}
)


def risk_level_for_category(category: str) -> str:
    """Return ``high`` / ``medium`` / ``low`` for a ticket category."""
    if category in HIGH_RISK_CATEGORIES:
        return "high"
    if category in _MEDIUM_RISK_CATEGORIES:
        return "medium"
    return "low"


def is_auto_answerable(
    *, category: str, escalation_needed: bool, kb_confidence: float
) -> bool:
    """A ticket may carry an auto-drafted answer only when it is low-risk,
    not flagged for escalation, and the KB matched with real confidence.

    Note: "auto-answerable" only means a draft may be attached — the reply
    is still never sent without approval.
    """
    if escalation_needed:
        return False
    if risk_level_for_category(category) != "low":
        return False
    return kb_confidence >= 0.34
