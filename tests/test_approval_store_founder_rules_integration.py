"""Wave 7.7 §2 — integration tests: founder rules ↔ ApprovalStore.

Asserts the four hard claims:
  1. WhatsApp requests are NEVER auto-approved, even with a matching rule.
  2. Email requests with a matching rule transition pending → approved.
  3. Email requests without a matching rule stay pending.
  4. An audit breadcrumb is written when a rule fires.
"""
from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.founder_rules import (
    FounderRuleEngine,
)
from auto_client_acquisition.approval_center.founder_rules_integration import (
    try_auto_approve_via_founder_rule,
)
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)


@pytest.fixture
def engine(tmp_path: Path):
    rules_p = tmp_path / "active_rules.jsonl"
    audit_p = tmp_path / "rule_match_audit.jsonl"
    with patch.dict(os.environ, {"DEALIX_FOUNDER_RULES_SECRET": "integ-test-secret"}):
        yield FounderRuleEngine(rules_path=rules_p, audit_path=audit_p)


def _email_req(handle: str = "acme") -> ApprovalRequest:
    return ApprovalRequest(
        object_type="lead",
        object_id=f"lead:{handle}-001",
        action_type="faq_reply",
        channel="email",
        risk_level="low",
        proof_impact=f"leadops:{handle}:1",
    )


def _whatsapp_req(handle: str = "acme") -> ApprovalRequest:
    return ApprovalRequest(
        object_type="lead",
        object_id=f"lead:{handle}-001",
        action_type="faq_reply",
        channel="whatsapp",
        risk_level="low",
        proof_impact=f"leadops:{handle}:1",
    )


# ── Hard rule 1: whatsapp can never auto-approve ─────────────────


def test_whatsapp_never_auto_approved_even_with_matching_rule(
    engine: FounderRuleEngine,
) -> None:
    # The CLI / engine refuses to create a whatsapp rule at all.
    with pytest.raises(ValueError, match="permanently blocked"):
        engine.create_rule(
            name="x", channel="whatsapp", customer_handle="acme",
        )

    # Even with an email-shaped rule live, a whatsapp request must
    # stay pending end-to-end through the ApprovalStore helper.
    rule = engine.create_rule(
        name="email FAQ",
        channel="email",
        customer_handle="acme",
        action_type="faq_reply",
        max_risk_level="low",
        min_confidence=0.9,
    )
    engine.append_rule(rule)

    store = ApprovalStore()
    req = _whatsapp_req()
    out = store.create_with_founder_rules(req, confidence=1.0, engine=engine)
    assert ApprovalStatus(out.status) == ApprovalStatus.PENDING


# ── Hard rule 2: email with matching rule transitions to approved ─


def test_email_request_with_matching_rule_auto_approves(
    engine: FounderRuleEngine,
) -> None:
    rule = engine.create_rule(
        name="FAQ replies",
        channel="email",
        customer_handle="acme",
        action_type="faq_reply",
        max_risk_level="low",
        min_confidence=0.85,
    )
    engine.append_rule(rule)

    store = ApprovalStore()
    req = _email_req()
    out = store.create_with_founder_rules(
        req, confidence=0.95, content="any content", engine=engine
    )
    assert ApprovalStatus(out.status) == ApprovalStatus.APPROVED
    assert out.action_mode == "approved_execute"
    # Edit history records the rule_id.
    assert any(
        e.get("rule_id") == rule.rule_id and e.get("action") == "auto_approve"
        for e in out.edit_history
    )


# ── Hard rule 3: email without matching rule stays pending ───────


def test_email_request_without_matching_rule_stays_pending(
    engine: FounderRuleEngine,
) -> None:
    # Register a rule for a *different* customer.
    rule = engine.create_rule(
        name="other only",
        channel="email",
        customer_handle="beta",
        action_type="faq_reply",
        min_confidence=0.0,
    )
    engine.append_rule(rule)

    store = ApprovalStore()
    req = _email_req(handle="acme")
    out = store.create_with_founder_rules(req, confidence=1.0, engine=engine)
    assert ApprovalStatus(out.status) == ApprovalStatus.PENDING
    assert out.action_mode == "approval_required"


# ── Hard rule 4: audit breadcrumb written on match ───────────────


def test_audit_breadcrumb_written_on_match(engine: FounderRuleEngine) -> None:
    rule = engine.create_rule(
        name="FAQ replies",
        channel="email",
        customer_handle="acme",
        action_type="faq_reply",
        min_confidence=0.0,
    )
    engine.append_rule(rule)

    store = ApprovalStore()
    req = _email_req()
    store.create_with_founder_rules(req, confidence=0.95, engine=engine)

    matches = engine.list_recent_matches(limit=5)
    assert len(matches) == 1
    assert matches[0]["rule_id"] == rule.rule_id
    assert matches[0]["approval_id"] == req.approval_id
    assert matches[0]["channel"] == "email"


# ── Bonus: idempotency + helper-level checks ─────────────────────


def test_helper_is_idempotent_on_already_approved(
    engine: FounderRuleEngine,
) -> None:
    rule = engine.create_rule(
        name="r",
        channel="email",
        customer_handle="acme",
        action_type="faq_reply",
        min_confidence=0.0,
    )
    engine.append_rule(rule)

    req = _email_req()
    req.status = ApprovalStatus.APPROVED  # type: ignore[assignment]
    out = try_auto_approve_via_founder_rule(req, engine=engine)
    # Status preserved, no extra edit history entry from the rule.
    assert ApprovalStatus(out.status) == ApprovalStatus.APPROVED
    assert all(e.get("action") != "auto_approve" for e in out.edit_history)


def test_high_risk_email_never_auto_approved(engine: FounderRuleEngine) -> None:
    rule = engine.create_rule(
        name="r",
        channel="email",
        customer_handle="acme",
        action_type="faq_reply",
        max_risk_level="medium",
        min_confidence=0.0,
    )
    engine.append_rule(rule)

    req = _email_req()
    req.risk_level = "high"
    out = try_auto_approve_via_founder_rule(req, engine=engine)
    assert ApprovalStatus(out.status) == ApprovalStatus.PENDING
