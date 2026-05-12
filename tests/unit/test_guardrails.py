"""Unit tests for core/llm/guardrails.py (T3b)."""

from __future__ import annotations

from core.llm.guardrails import (
    guard_proposal_output,
    redact_pii,
    validate_proposal_json,
)


def test_redact_pii_strips_nid() -> None:
    text = "العميل رقم 1234567890 يرغب بعرض."
    out = redact_pii(text)
    assert "1234567890" not in out.redacted_text
    assert "[nid]" in out.redacted_text
    assert "nid" in out.violations
    assert out.ok is False


def test_redact_pii_strips_iban_and_vat() -> None:
    text = "حسابي SA0380000000608010167519 ورقم الضريبي 300000000000003"
    out = redact_pii(text)
    assert "[iban]" in out.redacted_text
    assert "[vat]" in out.redacted_text


def test_redact_pii_allows_allowed_email() -> None:
    text = "يرجى الرد على decision@acme.sa أو dpo@other.sa"
    out = redact_pii(text, allowed_emails=["decision@acme.sa"])
    assert "decision@acme.sa" in out.redacted_text
    assert "dpo@other.sa" not in out.redacted_text
    assert "email_leak" in out.violations


def test_validate_proposal_json_shape_missing() -> None:
    out = validate_proposal_json('{"subject":"x"}')
    assert out.ok is False
    assert "missing_fields" in out.violations


def test_validate_proposal_json_invalid_json() -> None:
    out = validate_proposal_json("not-json")
    assert out.ok is False
    assert "invalid_json" in out.violations


def test_guard_proposal_output_happy_path() -> None:
    raw = '{"subject":"عرض جديد","body_ar":"شكراً","next_steps":["call"]}'
    out = guard_proposal_output(raw, allowed_emails=[])
    assert out.ok is True
