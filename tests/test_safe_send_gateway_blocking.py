"""Wave 7.5 §24.2 Fix 4 — safe_send_gateway BLOCKS, not just checks."""
from __future__ import annotations

import pytest

from auto_client_acquisition.safe_send_gateway import (
    SendBlocked,
    enforce_consent_or_block,
    summarize_gates,
)


def test_invalid_channel_raises() -> None:
    with pytest.raises(SendBlocked) as exc_info:
        enforce_consent_or_block(
            channel="telegram",
            destination="@user",
            approval_status="approved",
        )
    assert exc_info.value.reason_code == "invalid_channel"
    assert exc_info.value.gate == "channel_validation"


def test_not_approved_raises() -> None:
    with pytest.raises(SendBlocked) as exc_info:
        enforce_consent_or_block(
            channel="whatsapp",
            destination="+966512345678",
            approval_status="pending",
            consent_record_id="con_123",
        )
    assert exc_info.value.reason_code == "not_approved"
    assert "founder approval" in exc_info.value.reasons_en.lower()


def test_opted_out_raises_permanent_block() -> None:
    with pytest.raises(SendBlocked) as exc_info:
        enforce_consent_or_block(
            channel="whatsapp",
            destination="+966512345678",
            approval_status="approved",
            is_opted_out=True,
            consent_record_id="con_123",
        )
    assert exc_info.value.reason_code == "opted_out"
    assert "PDPL" in exc_info.value.reasons_en or "PDPL" in exc_info.value.reasons_ar


def test_whatsapp_without_consent_record_raises() -> None:
    with pytest.raises(SendBlocked) as exc_info:
        enforce_consent_or_block(
            channel="whatsapp",
            destination="+966512345678",
            approval_status="approved",
            is_opted_out=False,
            consent_record_id="",  # No consent record
        )
    assert exc_info.value.reason_code == "no_consent_record"


def test_email_without_consent_record_passes_for_now() -> None:
    # Email path doesn't hard-require consent_record_id at gateway level
    # (caller's compliance check still runs separately via email_send.py)
    decision = enforce_consent_or_block(
        channel="email",
        destination="ceo@acme.sa",
        approval_status="approved",
        is_opted_out=False,
    )
    assert decision.is_safe_to_send is True


def test_quiet_hours_raises() -> None:
    with pytest.raises(SendBlocked) as exc_info:
        enforce_consent_or_block(
            channel="whatsapp",
            destination="+966512345678",
            approval_status="approved",
            consent_record_id="con_123",
            quiet_hours_active=True,
        )
    assert exc_info.value.reason_code == "quiet_hours"
    assert "21:00" in exc_info.value.reasons_en or "21:00" in exc_info.value.reasons_ar


def test_happy_path_returns_decision() -> None:
    decision = enforce_consent_or_block(
        channel="whatsapp",
        destination="+966512345678",
        approval_status="approved",
        is_opted_out=False,
        consent_record_id="con_123",
        approval_action_id="apr_456",
        quiet_hours_active=False,
    )
    assert decision.is_safe_to_send is True
    assert decision.channel == "whatsapp"
    assert decision.audit_breadcrumb["all_gates_passed"] is True


def test_summarize_gates_returns_documentation() -> None:
    summary = summarize_gates()
    assert "approval_gate" in summary
    assert "opt_out_gate" in summary
    assert "consent_record_gate" in summary
    assert "quiet_hours_gate" in summary
    # All gate descriptions are non-empty strings
    for gate, desc in summary.items():
        assert isinstance(desc, str) and len(desc) > 0
