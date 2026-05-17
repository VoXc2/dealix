"""Assurance System — orchestrator, acceptance tests, funnel, review,
improvement and the scale / no-scale verdict."""
from __future__ import annotations

import json

import pytest

from auto_client_acquisition.assurance_os.acceptance_tests import (
    ACCEPTANCE_TESTS,
    run_acceptance_tests,
)
from auto_client_acquisition.assurance_os.assurance_system import (
    LAYERS,
    report_to_dict,
    run_assurance,
)
from auto_client_acquisition.assurance_os.funnel import build_funnel, detect_bottleneck
from auto_client_acquisition.assurance_os.gates import GATE_SPECS
from auto_client_acquisition.assurance_os.improvement import select_experiments
from auto_client_acquisition.assurance_os.models import AssuranceInputs

_FULL_MATURITY = {
    "sales_autopilot": 5, "marketing_factory": 5, "support_autopilot": 5,
    "delivery_factory": 5, "partner_machine": 5, "affiliate_machine": 5,
    "approval_center": 5, "evidence_ledger": 5, "no_build_engine": 5,
    "reporting": 5,
}


def _all_gate_answers() -> dict[str, bool]:
    return {cid: True for _, _, _, crits in GATE_SPECS for cid, _, _ in crits}


def test_report_runs_seven_layers() -> None:
    report = run_assurance(AssuranceInputs())
    assert report.layers == LAYERS
    assert len(report.layers) == 7


def test_empty_inputs_verdict_no_scale() -> None:
    report = run_assurance(AssuranceInputs())
    assert report.verdict == "no_scale"
    assert report.verdict_reasons  # honest blocking reasons listed


def test_report_is_json_serializable() -> None:
    json.dumps(report_to_dict(run_assurance(AssuranceInputs())))


def test_full_inputs_verdict_scale() -> None:
    inputs = AssuranceInputs(
        gate_answers=_all_gate_answers(),
        machine_maturity=_FULL_MATURITY,
        evidence_completeness_pct=95,
        lead_scoring_coverage_pct=100,
        support_high_risk_escalation_pct=100,
        affiliate_payout_before_payment_count=0,
        approval_compliance_pct=100,
    )
    report = run_assurance(inputs)
    assert report.verdict == "scale"
    assert report.verdict_reasons == []


def test_one_unmet_condition_blocks_scale() -> None:
    inputs = AssuranceInputs(
        gate_answers=_all_gate_answers(),
        machine_maturity=_FULL_MATURITY,
        evidence_completeness_pct=50,  # below 90
        lead_scoring_coverage_pct=100,
        support_high_risk_escalation_pct=100,
        affiliate_payout_before_payment_count=0,
        approval_compliance_pct=100,
    )
    report = run_assurance(inputs)
    assert report.verdict == "no_scale"
    assert any("evidence_completeness" in r for r in report.verdict_reasons)


def test_25_acceptance_tests() -> None:
    assert len(ACCEPTANCE_TESTS) == 25
    results = run_acceptance_tests(AssuranceInputs())
    assert all(r.result == "unknown" for r in results)


def test_acceptance_results_recorded() -> None:
    results = run_acceptance_tests(
        AssuranceInputs(acceptance_results={"at_sales_1": "pass", "at_gov_3": "fail"})
    )
    by_id = {r.id: r.result for r in results}
    assert by_id["at_sales_1"] == "pass"
    assert by_id["at_gov_3"] == "fail"
    assert by_id["at_sales_2"] == "unknown"


def test_funnel_ten_rungs_and_conversion() -> None:
    funnel = build_funnel(AssuranceInputs(
        funnel_counts={"attention": 100, "lead": 40, "qualified": 10}
    ))
    assert len(funnel.rungs) == 10
    assert funnel.conversion["attention->lead"] == 0.4
    # rungs with no count -> conversion is None, never fabricated
    assert funnel.conversion["paid->delivered"] is None


def test_detect_bottleneck() -> None:
    funnel = build_funnel(AssuranceInputs(
        funnel_counts={"attention": 100, "lead": 90, "qualified": 9}
    ))
    assert detect_bottleneck(funnel) == "lead->qualified"


def test_weekly_review_has_twelve_questions() -> None:
    report = run_assurance(AssuranceInputs())
    assert len(report.review.answered_questions) == 12
    assert len(report.review.decisions) == 5


def test_experiment_cap_enforced() -> None:
    too_many = AssuranceInputs(experiments=[{"id": f"e{i}"} for i in range(4)])
    with pytest.raises(ValueError, match="max 3 experiments"):
        select_experiments(too_many)


def test_default_experiments_when_none_supplied() -> None:
    experiments = select_experiments(AssuranceInputs())
    assert 1 <= len(experiments) <= 3
    assert all(e.decision == "pending" for e in experiments)


def test_improvement_items_default_to_proposed() -> None:
    report = run_assurance(AssuranceInputs(
        improvement_items=[{"title": "fix CTA", "recommended_action": "add UTM"}]
    ))
    assert report.improvement[0].status == "proposed"
