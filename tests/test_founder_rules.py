"""Wave 7.7 §1 — founder rules tests."""
from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from auto_client_acquisition.approval_center.founder_rules import (
    DEFAULT_RULE_TTL_DAYS,
    FounderRule,
    FounderRuleEngine,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest


@pytest.fixture
def tmp_engine(tmp_path: Path):
    rules_p = tmp_path / "active_rules.jsonl"
    audit_p = tmp_path / "rule_match_audit.jsonl"
    with patch.dict(os.environ, {"DEALIX_FOUNDER_RULES_SECRET": "test-secret-12345"}):
        yield FounderRuleEngine(rules_path=rules_p, audit_path=audit_p)


def test_create_rule_signs_with_hmac(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(
        name="FAQ replies for acme",
        channel="email",
        customer_handle="acme-real-estate",
        action_type="faq_reply",
        max_risk_level="low",
        min_confidence=0.9,
    )
    assert rule.rule_id.startswith("rule_")
    assert rule.founder_signature  # HMAC was computed
    assert tmp_engine.verify_signature(rule)


def test_create_rule_refuses_whatsapp(tmp_engine: FounderRuleEngine) -> None:
    with pytest.raises(ValueError, match="permanently blocked"):
        tmp_engine.create_rule(
            name="auto WA",
            channel="whatsapp",
        )


def test_create_rule_refuses_linkedin(tmp_engine: FounderRuleEngine) -> None:
    with pytest.raises(ValueError, match="permanently blocked"):
        tmp_engine.create_rule(name="x", channel="linkedin")


def test_create_rule_refuses_phone(tmp_engine: FounderRuleEngine) -> None:
    with pytest.raises(ValueError, match="permanently blocked"):
        tmp_engine.create_rule(name="x", channel="phone")


def test_create_rule_refuses_high_risk(tmp_engine: FounderRuleEngine) -> None:
    with pytest.raises(ValueError, match="risk_level"):
        tmp_engine.create_rule(name="x", channel="email", max_risk_level="high")


def test_create_rule_refuses_blocked_risk(tmp_engine: FounderRuleEngine) -> None:
    with pytest.raises(ValueError, match="risk_level"):
        tmp_engine.create_rule(name="x", channel="email", max_risk_level="blocked")


def test_create_rule_refuses_invalid_confidence(tmp_engine: FounderRuleEngine) -> None:
    with pytest.raises(ValueError, match="min_confidence"):
        tmp_engine.create_rule(name="x", channel="email", min_confidence=1.5)


def test_create_rule_refuses_invalid_regex(tmp_engine: FounderRuleEngine) -> None:
    with pytest.raises(ValueError, match="invalid content_pattern_regex"):
        tmp_engine.create_rule(name="x", channel="email", content_pattern_regex="[unbalanced")


def test_signature_invalid_when_secret_missing(tmp_path: Path) -> None:
    eng = FounderRuleEngine(
        rules_path=tmp_path / "r.jsonl",
        audit_path=tmp_path / "a.jsonl",
    )
    # Without secret env, signing returns "" → verification fails
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("DEALIX_FOUNDER_RULES_SECRET", None)
        rule = FounderRule(
            rule_id="r1", name="x", channel="email",
            created_at="2026-05-01T00:00:00+00:00",
            expires_at="2099-01-01T00:00:00+00:00",
            founder_signature="abc123",
        )
        assert eng.verify_signature(rule) is False


def test_persistence_roundtrip(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(
        name="r1", channel="email", customer_handle="acme",
    )
    tmp_engine.append_rule(rule)
    loaded = tmp_engine.list_rules()
    assert len(loaded) == 1
    assert loaded[0].rule_id == rule.rule_id
    assert tmp_engine.verify_signature(loaded[0])


def test_disable_rule(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(name="r1", channel="email")
    tmp_engine.append_rule(rule)
    assert tmp_engine.disable_rule(rule.rule_id) is True
    rules = tmp_engine.list_rules()
    assert rules[0].enabled is False
    # Disabled → not in active list
    assert tmp_engine.list_active_rules() == []


def test_match_email_low_risk_high_confidence(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(
        name="email FAQ",
        channel="email",
        customer_handle="acme",
        action_type="faq_reply",
        max_risk_level="low",
        min_confidence=0.85,
    )
    tmp_engine.append_rule(rule)

    req = ApprovalRequest(
        object_type="lead", object_id="lead:acme-001",
        action_type="faq_reply", channel="email", risk_level="low",
    )
    matched = tmp_engine.match(req, confidence=0.9, content="How do I reset my password?")
    assert matched is not None
    assert matched.rule_id == rule.rule_id


def test_match_refuses_whatsapp_even_with_rule_table(tmp_engine: FounderRuleEngine) -> None:
    # Even if someone manually wrote a whatsapp rule into the file
    # (bypassing create_rule), match() must refuse
    bad_rule_data = {
        "rule_id": "evil",
        "name": "evil",
        "channel": "whatsapp",
        "customer_handle": "*",
        "action_type": "*",
        "max_risk_level": "low",
        "min_confidence": 0.0,
        "content_pattern_regex": "",
        "created_at": "2026-05-07T00:00:00+00:00",
        "expires_at": "2099-01-01T00:00:00+00:00",
        "founder_signature": "",
        "enabled": True,
        "notes": "",
    }
    tmp_engine.rules_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_engine.rules_path.write_text(
        json.dumps(bad_rule_data) + "\n", encoding="utf-8"
    )
    req = ApprovalRequest(
        object_type="msg", object_id="m:1",
        action_type="reply", channel="whatsapp", risk_level="low",
    )
    assert tmp_engine.match(req, confidence=1.0) is None


def test_match_refuses_high_risk(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(
        name="r", channel="email", max_risk_level="medium", min_confidence=0.0,
    )
    tmp_engine.append_rule(rule)
    req = ApprovalRequest(
        object_type="x", object_id="x:1", action_type="reply",
        channel="email", risk_level="high",
    )
    assert tmp_engine.match(req, confidence=1.0) is None


def test_match_refuses_low_confidence(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(
        name="r", channel="email", min_confidence=0.9,
    )
    tmp_engine.append_rule(rule)
    req = ApprovalRequest(
        object_type="x", object_id="x:1", action_type="reply",
        channel="email", risk_level="low",
    )
    assert tmp_engine.match(req, confidence=0.5) is None
    assert tmp_engine.match(req, confidence=0.95) is not None


def test_match_customer_handle_filter(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(
        name="acme only", channel="email", customer_handle="acme",
        min_confidence=0.0,
    )
    tmp_engine.append_rule(rule)
    # Match acme
    req_a = ApprovalRequest(
        object_type="lead", object_id="lead:acme-1",
        action_type="reply", channel="email", risk_level="low",
    )
    assert tmp_engine.match(req_a, confidence=1.0) is not None
    # Don't match other customer
    req_b = ApprovalRequest(
        object_type="lead", object_id="lead:beta-1",
        action_type="reply", channel="email", risk_level="low",
    )
    assert tmp_engine.match(req_b, confidence=1.0) is None


def test_match_content_regex(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(
        name="password FAQ", channel="email",
        content_pattern_regex=r"\bpassword\b",
        min_confidence=0.0,
    )
    tmp_engine.append_rule(rule)
    req = ApprovalRequest(
        object_type="x", object_id="x:1", action_type="reply",
        channel="email", risk_level="low",
    )
    assert tmp_engine.match(req, confidence=1.0, content="how to reset password") is not None
    assert tmp_engine.match(req, confidence=1.0, content="how do I login") is None


def test_expired_rule_ignored(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(name="r", channel="email", min_confidence=0.0, ttl_days=-1)
    tmp_engine.append_rule(rule)
    assert tmp_engine.list_active_rules() == []
    req = ApprovalRequest(
        object_type="x", object_id="x:1", action_type="reply",
        channel="email", risk_level="low",
    )
    assert tmp_engine.match(req, confidence=1.0) is None


def test_record_match_writes_audit(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(name="r", channel="email", min_confidence=0.0)
    tmp_engine.append_rule(rule)
    req = ApprovalRequest(
        object_type="x", object_id="x:1", action_type="reply",
        channel="email", risk_level="low",
    )
    tmp_engine.record_match(rule, req, confidence=0.95)
    matches = tmp_engine.list_recent_matches()
    assert len(matches) == 1
    assert matches[0]["rule_id"] == rule.rule_id
    assert matches[0]["approval_id"] == req.approval_id
    assert matches[0]["confidence"] == 0.95


def test_default_ttl_is_30_days(tmp_engine: FounderRuleEngine) -> None:
    rule = tmp_engine.create_rule(name="r", channel="email", min_confidence=0.0)
    # Verify expiry is roughly 30 days out
    assert DEFAULT_RULE_TTL_DAYS == 30
    from datetime import datetime, timezone
    exp = datetime.fromisoformat(rule.expires_at)
    created = datetime.fromisoformat(rule.created_at)
    delta_days = (exp - created).days
    assert 29 <= delta_days <= 30


def test_unsigned_rule_not_active(tmp_engine: FounderRuleEngine) -> None:
    # Manually inject a rule with bogus signature
    bad = {
        "rule_id": "evil", "name": "evil", "channel": "email",
        "customer_handle": "*", "action_type": "*", "max_risk_level": "low",
        "min_confidence": 0.0, "content_pattern_regex": "",
        "created_at": "2026-05-07T00:00:00+00:00",
        "expires_at": "2099-01-01T00:00:00+00:00",
        "founder_signature": "FAKE_SIGNATURE",
        "enabled": True, "notes": "",
    }
    tmp_engine.rules_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_engine.rules_path.write_text(
        json.dumps(bad) + "\n", encoding="utf-8"
    )
    # list_rules returns it but list_active_rules filters it out
    assert len(tmp_engine.list_rules()) == 1
    assert tmp_engine.list_active_rules() == []
