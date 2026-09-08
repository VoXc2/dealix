import pytest

import app.outbound.policy_gate as policy_gate
from app.outbound.consent import consent_backend_status
from app.outbound.suppression import suppression_backend_status


@pytest.fixture(autouse=True)
def _memory_backends_default(monkeypatch):
    """Keep unit tests deterministic even on a production-like host."""

    monkeypatch.delenv("DEALIX_SUPPRESSION_BACKEND", raising=False)
    monkeypatch.delenv("DEALIX_CONSENT_BACKEND", raising=False)
    monkeypatch.delenv("DEALIX_CONSENT_DEFAULT_TENANT", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)


def _email_contact() -> dict[str, object]:
    return {
        "email": "test@example.com",
        "source_url": "https://example.com",
        "verification_status": "approved_to_send",
        "email_opt_out": False,
    }


def _approved_email() -> dict[str, str]:
    return {
        "status": "approved",
        "body": "Hello from Dealix. You can unsubscribe anytime.",
        "consent_purpose": "direct_marketing",
    }


def test_email_blocked_by_default():
    env = {
        "EXTERNAL_SEND_ENABLED": "false",
        "EMAIL_SEND_ENABLED": "false",
        "OUTBOUND_MODE": "draft_only",
    }
    result = policy_gate.can_send_email(_email_contact(), _approved_email(), env)
    assert not result.allowed


def test_current_suppression_backend_is_not_live_eligible():
    assert suppression_backend_status() == {
        "backend": "memory",
        "persistent": False,
        "live_send_eligible": False,
        "reason": "in_memory_suppression_is_not_durable",
    }


def test_current_consent_backend_is_not_live_eligible():
    assert consent_backend_status() == {
        "backend": "memory",
        "persistent": False,
        "live_send_eligible": False,
        "reason": "in_memory_consent_is_not_durable",
    }


def test_controlled_live_is_blocked_until_suppression_persistence_is_proven():
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    result = policy_gate.can_send_email(_email_contact(), _approved_email(), env)
    assert not result.allowed
    assert "persistent suppression backend is not verified" in result.reasons


def test_controlled_live_is_blocked_until_consent_persistence_is_proven(monkeypatch):
    monkeypatch.setattr(policy_gate, "persistent_suppression_ready", lambda: True)
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    result = policy_gate.can_send_email(_email_contact(), _approved_email(), env)
    assert not result.allowed
    assert "persistent consent backend is not verified" in result.reasons


def test_email_allowed_only_when_both_durability_gates_are_proven(monkeypatch):
    monkeypatch.setattr(policy_gate, "persistent_suppression_ready", lambda: True)
    monkeypatch.setattr(policy_gate, "persistent_consent_ready", lambda: True)
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    result = policy_gate.can_send_email(_email_contact(), _approved_email(), env)
    assert result.allowed, result.reasons


def test_controlled_live_requires_explicit_consent_purpose(monkeypatch):
    monkeypatch.setattr(policy_gate, "persistent_suppression_ready", lambda: True)
    monkeypatch.setattr(policy_gate, "persistent_consent_ready", lambda: True)
    monkeypatch.setattr(policy_gate, "has_consent", lambda *args, **kwargs: True)
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    message = {
        "status": "approved",
        "body": "Hello from Dealix. You can unsubscribe anytime.",
    }
    result = policy_gate.can_send_email(_email_contact(), message, env)
    assert not result.allowed
    assert "consent purpose is required for controlled live" in result.reasons


def test_policy_gate_forwards_exact_consent_purpose(monkeypatch):
    monkeypatch.setattr(policy_gate, "persistent_suppression_ready", lambda: True)
    monkeypatch.setattr(policy_gate, "persistent_consent_ready", lambda: True)
    observed: list[str | None] = []

    def _has_consent(channel, contact, purpose=None):
        observed.append(purpose)
        return True

    monkeypatch.setattr(policy_gate, "has_consent", _has_consent)
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    message = _approved_email()
    message["consent_purpose"] = "partner_discovery"
    result = policy_gate.can_send_email(_email_contact(), message, env)
    assert result.allowed, result.reasons
    assert observed == ["partner_discovery"]


def test_email_requires_unsubscribe():
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    message = {
        "status": "approved",
        "body": "Hello from Dealix.",
        "consent_purpose": "direct_marketing",
    }
    result = policy_gate.can_send_email(_email_contact(), message, env)
    assert not result.allowed
    assert any("unsubscribe" in reason for reason in result.reasons)


def test_whatsapp_requires_opt_in_and_template():
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "WHATSAPP_SEND_ENABLED": "true",
        "WHATSAPP_ALLOW_LIVE_SEND": "true",
        "OUTBOUND_MODE": "controlled_live",
        "WHATSAPP_SEND_MODE": "template_only",
    }
    contact = {
        "whatsapp": "+966500000000",
        "whatsapp_opt_in": False,
        "whatsapp_opt_out": False,
        "source_url": "https://example.com",
        "verification_status": "approved_to_send",
    }
    message = {
        "status": "approved",
        "template_name": "dealix_intro_ar",
        "body": "السلام عليكم",
        "consent_purpose": "direct_marketing",
    }
    result = policy_gate.can_send_whatsapp(contact, message, env)
    assert not result.allowed
    assert any("opt-in" in reason for reason in result.reasons)


def test_whatsapp_allowed_only_when_policy_and_both_durability_gates_pass(monkeypatch):
    monkeypatch.setattr(policy_gate, "persistent_suppression_ready", lambda: True)
    monkeypatch.setattr(policy_gate, "persistent_consent_ready", lambda: True)
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "WHATSAPP_SEND_ENABLED": "true",
        "WHATSAPP_ALLOW_LIVE_SEND": "true",
        "OUTBOUND_MODE": "controlled_live",
        "WHATSAPP_SEND_MODE": "template_only",
    }
    contact = {
        "whatsapp": "+966500000000",
        "whatsapp_opt_in": True,
        "whatsapp_opt_out": False,
        "source_url": "https://example.com",
        "verification_status": "approved_to_send",
    }
    message = {
        "status": "approved",
        "template_name": "dealix_intro_ar",
        "body": "السلام عليكم",
        "consent_purpose": "direct_marketing",
    }
    result = policy_gate.can_send_whatsapp(contact, message, env)
    assert result.allowed, result.reasons


def test_blocks_fake_guarantees():
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    message = {
        "status": "approved",
        "body": "نضمن لك 100% نتائج. unsubscribe anytime.",
        "consent_purpose": "direct_marketing",
    }
    result = policy_gate.can_send_email(_email_contact(), message, env)
    assert not result.allowed
    assert any("blocked claim" in reason for reason in result.reasons)
