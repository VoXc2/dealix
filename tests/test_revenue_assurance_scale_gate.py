"""Scale Gate — all 7 thresholds must hold; missing signal blocks scaling."""

from __future__ import annotations

from auto_client_acquisition.revenue_assurance_os.scale_gate import can_scale

_ALL_PASS = {
    "assurance_score": 80,
    "approval_compliance": 1.0,
    "high_risk_auto_send": 0,
    "lead_scoring_coverage": 1.0,
    "evidence_completeness": 0.95,
    "support_high_risk_escalation": 1.0,
    "affiliate_payout_before_payment": 0,
}


def test_all_thresholds_pass_allows_scaling() -> None:
    assert can_scale(_ALL_PASS).can_scale is True


def test_no_signal_blocks_scaling() -> None:
    result = can_scale()
    assert result.can_scale is False
    assert len(result.blocking_reasons) == 7


def test_single_failed_threshold_blocks() -> None:
    bad = dict(_ALL_PASS, high_risk_auto_send=1)
    result = can_scale(bad)
    assert result.can_scale is False
    assert "high_risk_auto_send" in result.blocking_reasons


def test_partial_approval_compliance_blocks() -> None:
    bad = dict(_ALL_PASS, approval_compliance=0.99)
    assert can_scale(bad).can_scale is False
