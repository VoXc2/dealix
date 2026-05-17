"""Orchestrator policy layer — the central approval-first enforcer.

Deterministic, no LLM. Four checks govern every automated action:
  - requires_approval / can_auto_send — is this action high-risk?
  - claim_has_source                  — does a regulated/outcome claim
                                        carry a source?
  - stage_transition_allowed          — is this pipeline move legal?
"""

from __future__ import annotations

import re

# Actions that ALWAYS require founder approval and never auto-execute.
HIGH_RISK_ACTIONS: frozenset[str] = frozenset(
    {
        "first_outreach",
        "send_message",
        "invoice_send",
        "scope_send",
        "final_diagnostic",
        "case_study_publish",
        "security_claim",
        "discount",
        "support_reply_send",
        "knowledge_publish",
    }
)

# Canonical sales pipeline stage order. A transition may advance by at
# most one stage (each stage carries its own evidence) or drop to a
# terminal loss — no skipping.
STAGE_ORDER: tuple[str, ...] = (
    "new_lead",
    "qualified_a",
    "qualified_b",
    "meeting_booked",
    "meeting_done",
    "scope_requested",
    "scope_sent",
    "invoice_sent",
    "invoice_paid",
    "delivery_started",
    "proof_pack_sent",
    "sprint_candidate",
    "retainer_candidate",
)

_TERMINAL_STAGES: frozenset[str] = frozenset({"closed_lost"})

# Claims touching regulated or outcome topics must cite a source.
_SOURCE_REQUIRED_RE = re.compile(
    r"\b(security|compliance|guarantee|guaranteed|roi|revenue\s+increase|"
    r"legal|privacy|pdpl|certif\w*)\b|"
    r"(أمن|امتثال|نضمن|ضمان|عائد|قانون|خصوص|شهادة)",
    re.IGNORECASE,
)


def requires_approval(action: str) -> bool:
    """Is ``action`` a high-risk action that always needs approval?"""
    return action in HIGH_RISK_ACTIONS


def can_auto_send(action: str, context: dict | None = None) -> tuple[bool, str | None]:
    """Decide whether ``action`` may execute without founder approval.

    Returns ``(allowed, reason)``. High-risk actions are never auto-sent.
    """
    if requires_approval(action):
        return False, f"'{action}' is a high-risk action — approval required"
    return True, None


def claim_has_source(claim: str, source: str | None) -> tuple[bool, str | None]:
    """A claim touching a regulated/outcome topic must carry a source.

    Returns ``(ok, reason)``. ``ok`` is False when a sensitive claim has
    no source string.
    """
    if not claim:
        return True, None
    if _SOURCE_REQUIRED_RE.search(claim) and not (source or "").strip():
        return False, "claim references a regulated/outcome topic and needs a source"
    return True, None


def stage_transition_allowed(
    from_stage: str, to_stage: str
) -> tuple[bool, str | None]:
    """Validate a sales-pipeline stage transition.

    Forward by one stage, a no-op, or a drop to a terminal loss is
    allowed. Skipping stages or moving backwards is not.
    """
    if to_stage in _TERMINAL_STAGES:
        return True, None
    if from_stage not in STAGE_ORDER:
        return False, f"unknown from stage: {from_stage}"
    if to_stage not in STAGE_ORDER:
        return False, f"unknown to stage: {to_stage}"

    fi = STAGE_ORDER.index(from_stage)
    ti = STAGE_ORDER.index(to_stage)
    if ti == fi:
        return True, None
    if ti < fi:
        return False, "backwards stage transition not allowed"
    if ti == fi + 1:
        return True, None
    return False, "cannot skip stages — each transition needs its own evidence"
