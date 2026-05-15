"""Proof sovereignty — standard sections and claim gates."""

from __future__ import annotations

PROOF_SOVEREIGNTY_SECTIONS: tuple[str, ...] = (
    "problem",
    "inputs",
    "work_completed",
    "metrics",
    "before_after",
    "ai_outputs",
    "governance_events",
    "business_value",
    "risks",
    "limitations",
    "recommended_next_step",
)


def proof_sections_complete(present: frozenset[str]) -> bool:
    return all(s in present for s in PROOF_SOVEREIGNTY_SECTIONS)


def can_make_retainer_push(*, proof_score: int, governance_confidence: int) -> bool:
    return proof_score >= 80 and governance_confidence >= 70


def can_publish_case_public(*, client_authorized: bool, proof_score: int) -> bool:
    return client_authorized and proof_score >= 85
