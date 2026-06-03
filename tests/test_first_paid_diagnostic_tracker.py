"""First paid Diagnostic pipeline tracker."""

from __future__ import annotations

from scripts.verify_first_paid_diagnostic_tracker import analyze


def test_analyze_returns_expected_keys():
    blob = analyze()
    assert "payment_received_real" in blob
    assert "first_close_ready" in blob
    assert "verdict" in blob
    assert blob["total_events"] >= 0
