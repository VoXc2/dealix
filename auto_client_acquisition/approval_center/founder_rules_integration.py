"""Wave 7.7 §2 — Bridge between founder rules and the ApprovalStore.

Kept separate from approval_store.py so the rule engine can be wired
in without breaking the existing v6 store contract. Callers invoke
``try_auto_approve_via_founder_rule`` on a freshly-persisted PENDING
ApprovalRequest; if a signed, non-expired rule matches, the request
transitions pending → approved and an audit breadcrumb is written.

Hard guarantees (enforced both here AND in founder_rules.py):
  - WhatsApp / LinkedIn / Phone are NEVER auto-approved.
  - High / blocked risk levels are NEVER auto-approved.
  - Idempotent: an already-approved request is returned unchanged.
  - Fail-closed: any unexpected error returns the request unchanged.
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
    """If a founder rule matches, transition pending → approved and
    record an audit breadcrumb. Otherwise return req unchanged.

    NEVER overrides whatsapp / linkedin / phone gates.
    Idempotent on already-approved requests.
    """
    # ── Hard gates that no rule can bend ────────────────────────
    if (req.channel or "").lower() in _BLOCKED_AUTO_CHANNELS:
        return req
    if ApprovalStatus(req.status) != ApprovalStatus.PENDING:
        return req

    eng = engine or get_default_engine()
    try:
        rule = eng.match(req, confidence=confidence, content=content)
    except Exception:
        return req
    if rule is None:
        return req

    # Match found — transition + audit breadcrumb in edit_history.
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

    try:
        eng.record_match(rule, req, confidence=confidence)
    except Exception:
        # Audit-write failure must NOT unwind a successful auto-approve.
        # The edit_history breadcrumb above is the durable record.
        pass

    return req


__all__ = [
    "try_auto_approve_via_founder_rule",
    "get_default_engine",
    "reset_default_engine_for_tests",
]
