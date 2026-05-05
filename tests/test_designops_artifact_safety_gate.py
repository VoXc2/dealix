"""Safety gate tests — regex-only artifact safety check.

Uses Acme-Saudi-Pilot-EXAMPLE placeholders only. No real customer data.
"""
from __future__ import annotations

from auto_client_acquisition.designops.safety_gate import (
    SafetyGateResult,
    check_artifact,
)


def test_clean_bilingual_markdown_passes() -> None:
    text = (
        "# Acme-Saudi-Pilot-EXAMPLE — تقرير التسليم\n\n"
        "هذا تقرير تجريبي لـ Acme-Saudi-Pilot-EXAMPLE. لا يوجد ادعاءات."
    )
    result = check_artifact(text)
    assert isinstance(result, SafetyGateResult)
    assert result.passed is True
    assert result.blocked_reasons == []
    assert result.risk_level == "low"
    assert result.safe_to_publish is True
    # safe_to_send is ALWAYS False by default — manual review required
    assert result.safe_to_send is False


def test_blocks_arabic_guarantee_token() -> None:
    text = "نضمن لكم 50% زيادة في المبيعات"
    result = check_artifact(text)
    assert result.passed is False
    assert "نضمن" in result.forbidden_tokens_found
    assert any("forbidden_tokens" in r for r in result.blocked_reasons)
    assert result.risk_level == "blocked"
    assert result.safe_to_publish is False


def test_blocks_english_guaranteed_revenue_claim() -> None:
    text = "Our service guaranteed 10x revenue for every customer."
    result = check_artifact(text)
    assert result.passed is False
    assert "guaranteed" in result.forbidden_tokens_found
    # Both "guaranteed" AND ROI-claim should fire
    assert "unsupported_roi_claim" in result.blocked_reasons
    assert result.risk_level == "blocked"


def test_blocks_raw_saudi_phone_number() -> None:
    text = "Contact us at +966501234567 to learn more."
    result = check_artifact(text)
    assert result.passed is False
    assert "raw_pii_detected" in result.blocked_reasons
    assert result.risk_level == "blocked"


def test_blocks_raw_email() -> None:
    text = "Reach out: customer@example.sa for the demo."
    result = check_artifact(text)
    assert result.passed is False
    assert "raw_pii_detected" in result.blocked_reasons


def test_blocks_live_send_marker() -> None:
    text = "config: { action: send_email_live }"
    result = check_artifact(text)
    assert result.passed is False
    assert any("live_send_marker" in r for r in result.blocked_reasons)
    assert "send_email_live" in result.forbidden_tokens_found


def test_safe_to_send_always_false_by_default() -> None:
    """Even on a passing artifact, safe_to_send stays False —
    manual review is non-negotiable."""
    result = check_artifact("Hello world. مرحبا.")
    assert result.passed is True
    assert result.safe_to_send is False


def test_risk_level_blocked_when_any_forbidden_token_hit() -> None:
    text = "We will blast our list with promo emails."
    result = check_artifact(text)
    assert result.risk_level == "blocked"
    assert "blast" in result.forbidden_tokens_found


def test_dict_manifest_is_scanned_recursively() -> None:
    manifest = {
        "title": "ok",
        "body": {"copy": "we نضمن results"},
        "tags": ["clean", "blast"],
    }
    result = check_artifact(manifest)
    assert result.passed is False
    # Both "نضمن" and "blast" should be detected
    assert "نضمن" in result.forbidden_tokens_found
    assert "blast" in result.forbidden_tokens_found


def test_fake_customer_pattern_blocked() -> None:
    text = "Big Saudi Bank chose us last quarter."
    result = check_artifact(text)
    assert result.passed is False
    assert "fake_customer_name_pattern" in result.blocked_reasons
