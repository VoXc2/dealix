"""RevOps revenue truth + finance brief."""
from __future__ import annotations

from auto_client_acquisition.revops.finance_brief import build_finance_brief
from auto_client_acquisition.revops.revenue_truth import build_revops_truth_snapshot


def test_revops_truth_labels_draft_not_revenue() -> None:
    snap = build_revops_truth_snapshot(
        {"total_leads": 0, "commitments": 0, "paid": 0, "total_revenue_sar": 0},
    )
    assert snap["draft_invoice_is_revenue"] is False
    assert snap["payment_evidence_is_revenue"] is False


def test_finance_brief_has_margin_and_next_actions() -> None:
    brief = build_finance_brief()
    assert "gross_margin_estimate" in brief
    assert brief["next_action_ar"]
    assert brief["next_action_en"]
