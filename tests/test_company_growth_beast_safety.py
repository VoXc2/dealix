"""Safety policy unit checks."""

from __future__ import annotations

from auto_client_acquisition.company_growth_beast.safety_policy import assess_text_safety, redact_free_text, sector_requires_escalation


def test_blocked_phrase_auto_send() -> None:
    assert assess_text_safety("we do auto_send for leads")["safe"] is False


def test_redact_email() -> None:
    t = redact_free_text("reach me at user@corp.com please")
    assert "[redacted_email]" in t
    assert "user@corp.com" not in t


def test_sensitive_sector() -> None:
    assert sector_requires_escalation("Medical devices") is True
    assert sector_requires_escalation("وكالة تسويق") is False
