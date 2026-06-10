"""CEO Master Plan status script."""

from __future__ import annotations

from scripts.run_ceo_master_plan_status import analyze_ceo_master_plan


def test_analyze_ceo_master_plan_keys():
    blob = analyze_ceo_master_plan()
    assert "overall_verdict" in blob
    assert blob["p0_revenue_close"]["verdict"] in {"PASS", "OPEN", "IN_PROGRESS"}
    assert blob["p0_ceo_decision"]["decision"]["one_decision_filled"] is True
    assert blob["p0_gtm_blitz"]["icp"]["eligible"] >= 75
    assert blob["p0_gtm_blitz"]["proposal_templates"] >= 5
    assert blob["p2_repeatability"]["artifacts_present"] >= 4
