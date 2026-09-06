"""Wave 7.7 §2 — Bridge between founder rules and the ApprovalStore.

Kept separate from approval_store.py so the rule engine can be wired
in without breaking the existing v6 store contract. Callers invoke
``try_auto_approve_via_founder_rule`` while a PENDING ApprovalRequest is
being created; if a signed, non-expired rule matches *and its usage audit
is recorded successfully*, the request transitions pending -> approved and
a durable approval breadcrumb is written.

Hard guarantees (enforced both here AND in founder_rules.py):
  - WhatsApp / LinkedIn / Phone are NEVER auto-approved.
  - High / blocked risk levels are NEVER auto-approved.
  - Idempotent: an already-approved request is returned unchanged.
  - Fail-closed: match or rule-usage audit failures leave the request pending.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.approval_center.founder_rules import (
    _BLOCKED_AUTO_CHANNELS,
    FounderRuleEngine,
)
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)

_DEFAULT_ENGINE: FounderRuleEngine | None = None


def get_default_engine() -> FounderRuleEngine:
    """Process-scoped singleton. Tests pass their own engine instead."""
    global _DEFAULT_ENGINE
    if _DEFAULT_ENGINE is None:
        _DEFAULT_ENGINE = FounderRuleEngine()
    return _DEFAULT_ENGINE


def reset_default_engine_for_tests() -> None:
    """Test helper. Production code never calls this."""
    global _DEFAULT_ENGINE
    _DEFAULT_ENGINE = None


def try_auto_approve_via_founder_rule(
    req: ApprovalRequest,
    *,
    confidence: float = 1.0,
    content: str = "",
    engine: FounderRuleEngine | None = None,
) -> ApprovalRequest:
    """Auto-approve only when both rule matching and rule-use audit succeed.

    The approval record itself receives the durable breadcrumb, while the rule
    engine records use of the founder rule. A rule-engine audit failure is a
    trust failure, so the request remains PENDING instead of gaining execution
    authority with incomplete evidence.

    NEVER overrides whatsapp / linkedin / phone gates.
    Idempotent on already-approved requests.
    """
    # Hard gates that no rule can bend.
    if (req.channel or "").lower() in _BLOCKED_AUTO_CHANNELS:
        return req
    if ApprovalStatus(req.status) != ApprovalStatus.PENDING:
        return req
    # Reject if the request was already hard-blocked by safety policy
    # (e.g. ``evaluate_safety()`` set action_mode="blocked"). Founder
    # rules never override a blocked action.
    if (req.action_mode or "").lower() == "blocked":
        return req
    # Only auto-approve requests that are awaiting human approval.
    # A ``draft_only`` request must NOT be escalated into an executable
    # send — that would silently turn a non-send draft into a send.
    if (req.action_mode or "").lower() != "approval_required":
        return req

    eng = engine or get_default_engine()
    try:
        rule = eng.match(req, confidence=confidence, content=content)
    except Exception:
        return req
    if rule is None:
        return req

    # Record founder-rule use before granting execution authority. If the
    # rule-use audit cannot be written, fail closed and persist the request as
    # PENDING. This prevents a multi-worker/restart-safe Approval Center from
    # containing an APPROVED transition whose authorizing rule use is missing.
    try:
        eng.record_match(rule, req, confidence=confidence)
    except Exception:
        return req

    req.status = ApprovalStatus.APPROVED
    req.action_mode = "approved_execute"
    entry: dict[str, Any] = {
        "at": datetime.now(UTC).isoformat(),
        "who": "founder_rule",
        "action": "auto_approve",
        "rule_id": rule.rule_id,
        "rule_name": rule.name,
        "confidence": confidence,
    }
    req.edit_history.append(entry)
    req.updated_at = datetime.now(UTC)
    return req


__all__ = [
    "get_default_engine",
    "reset_default_engine_for_tests",
    "try_auto_approve_via_founder_rule",
]
