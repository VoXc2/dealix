"""Full Ops 2.0 — the `critical` approval tier (between high and blocked)."""
from __future__ import annotations

from auto_client_acquisition.approval_center.approval_policy import (
    CRITICAL_ACTION_TYPES,
    _RISK_ORDER,
    can_auto_approve,
    evaluate_safety,
    is_critical_action,
)
from auto_client_acquisition.approval_center.founder_rules import FounderRuleEngine
from auto_client_acquisition.approval_center.schemas import ApprovalRequest


def _req(**overrides) -> ApprovalRequest:
    base = {
        "object_type": "draft_message",
        "object_id": "obj_001",
        "action_type": "draft_email",
        "action_mode": "approval_required",
        "channel": "email",
        "risk_level": "low",
    }
    base.update(overrides)
    return ApprovalRequest.model_validate(base)


# ── risk ordering ────────────────────────────────────────────────


def test_critical_sits_between_high_and_blocked() -> None:
    assert _RISK_ORDER["high"] < _RISK_ORDER["critical"] < _RISK_ORDER["blocked"]


def test_critical_action_types_cover_required_set() -> None:
    for action in (
        "invoice_send",
        "refund",
        "affiliate_payout",
        "client_data_export",
        "security_compliance_claim",
        "case_study_publish",
        "external_autonomous_action",
    ):
        assert action in CRITICAL_ACTION_TYPES
        assert is_critical_action(action) is True


def test_non_critical_action_is_not_critical() -> None:
    assert is_critical_action("draft_email") is False


# ── evaluate_safety ──────────────────────────────────────────────


def test_evaluate_safety_upgrades_critical_action_risk() -> None:
    req = _req(action_type="refund", risk_level="low")
    evaluate_safety(req)
    assert req.risk_level == "critical"


def test_evaluate_safety_critical_cannot_be_pre_approved() -> None:
    req = _req(action_type="affiliate_payout", action_mode="approved_execute")
    evaluate_safety(req)
    assert req.action_mode == "approval_required"


def test_evaluate_safety_leaves_blocked_above_critical() -> None:
    # A blocked action stays blocked even when also a critical action.
    req = _req(action_type="invoice_send", risk_level="blocked")
    evaluate_safety(req)
    assert req.risk_level == "blocked"


# ── auto-approve gate ────────────────────────────────────────────


def test_critical_risk_never_auto_approves() -> None:
    req = _req(action_type="invoice_send", risk_level="critical", channel="email")
    assert can_auto_approve(req) is False


# ── founder rules recognise critical ─────────────────────────────


def test_founder_rule_does_not_match_critical(tmp_path) -> None:
    engine = FounderRuleEngine(
        rules_path=tmp_path / "rules.jsonl",
        audit_path=tmp_path / "audit.jsonl",
    )
    req = _req(action_type="client_data_export", risk_level="critical", channel="email")
    # critical is a recognized tier — no fail-closed crash, just no match.
    assert engine.match(req, confidence=1.0) is None
