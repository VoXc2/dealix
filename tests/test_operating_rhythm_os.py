"""Tests for operating_rhythm_os — CEO cadence contracts."""

from __future__ import annotations

from auto_client_acquisition.operating_finance_os.bad_revenue_filter import BadRevenueSignals
from auto_client_acquisition.operating_finance_os.hiring_triggers import HireFocus
from auto_client_acquisition.operating_rhythm_os.bad_revenue_council import (
    BadRevenueCouncilOutcome,
    BadRevenueCouncilSignals,
    council_recommend_outcome,
)
from auto_client_acquisition.operating_rhythm_os.board_memo import monthly_board_memo_sections_complete
from auto_client_acquisition.operating_rhythm_os.decision_queue import (
    DecisionQueueItem,
    DecisionType,
    decision_has_evidence,
    repeated_evidence_without_decision,
)
from auto_client_acquisition.operating_rhythm_os.governance_review import (
    GovernanceWeeklyChecklist,
    governance_weekly_healthy,
)
from auto_client_acquisition.operating_rhythm_os.hiring_triggers import rhythm_hire_focus
from auto_client_acquisition.operating_rhythm_os.productization_review import (
    ProductizationPath,
    productization_path,
)
from auto_client_acquisition.operating_rhythm_os.proof_review import (
    WeeklyProofDecision,
    weekly_proof_decision,
)
from auto_client_acquisition.operating_rhythm_os.quarterly_review import quarterly_outputs_complete
from auto_client_acquisition.operating_rhythm_os.weekly_scorecard import weekly_scorecard_keys_complete


def test_decision_requires_evidence() -> None:
    empty = DecisionQueueItem(
        decision_id="DEC-1",
        decision_type=DecisionType.BUILD,
        target="X",
        evidence=(),
        owner="Product Owner",
        deadline="this_week",
        decision_status="pending",
    )
    assert not decision_has_evidence(empty)
    ok = DecisionQueueItem(
        decision_id="DEC-2",
        decision_type=DecisionType.BUILD,
        target="X",
        evidence=("clients reported friction",),
        owner="Product Owner",
        deadline="this_week",
        decision_status="pending",
    )
    assert decision_has_evidence(ok)


def test_repeated_evidence_waste_signal() -> None:
    assert repeated_evidence_without_decision(same_theme_count=3, open_decision_exists=False)
    assert not repeated_evidence_without_decision(same_theme_count=3, open_decision_exists=True)


def test_weekly_proof_decision_bands() -> None:
    assert weekly_proof_decision(proof_score=88, adoption_score=50) == WeeklyProofDecision.CASE_SAFE_SUMMARY_CANDIDATE
    assert weekly_proof_decision(proof_score=82, adoption_score=75) == WeeklyProofDecision.RETAINER_RECOMMENDATION
    assert weekly_proof_decision(proof_score=65, adoption_score=90) == WeeklyProofDecision.DELIVERY_IMPROVEMENT_REQUIRED
    assert (
        weekly_proof_decision(proof_score=72, adoption_score=40, repeated_proof_pattern=True)
        == WeeklyProofDecision.BENCHMARK_CANDIDATE
    )


def test_productization_path_steps() -> None:
    assert productization_path(repeat_count=0) == ProductizationPath.OBSERVE
    assert productization_path(repeat_count=2) == ProductizationPath.TEMPLATE
    assert productization_path(repeat_count=3) == ProductizationPath.INTERNAL_TOOL
    assert (
        productization_path(repeat_count=5, client_pull=True) == ProductizationPath.CLIENT_FEATURE
    )
    assert (
        productization_path(repeat_count=3, across_retainers=True) == ProductizationPath.PLATFORM_MODULE
    )


def test_governance_weekly_all_green() -> None:
    check = GovernanceWeeklyChecklist(
        ai_runs_logged=True,
        outputs_have_governance_status=True,
        pii_flags_reviewed=True,
        unsupported_claims_rejected=True,
        forbidden_automation_requests_handled=True,
        agent_permission_escalations_reviewed=True,
        incidents_triaged=True,
    )
    assert governance_weekly_healthy(check)


def test_bad_revenue_council_rejects_scraping() -> None:
    council = BadRevenueCouncilSignals(
        asks_scraping=True,
        asks_cold_whatsapp_automation=False,
        asks_linkedin_automation=False,
        wants_guaranteed_sales=False,
        data_source_unclear=False,
        scope_open_ended=False,
        margin_weak=False,
        no_proof_path=False,
        no_retainer_path=False,
    )
    finance = BadRevenueSignals(
        open_scope=False,
        weak_margin=False,
        high_risk=False,
        governance_refused=False,
        wants_scraping=False,
        wants_guaranteed_sales=False,
        no_proof_path=False,
        no_retainer_path=False,
        no_productization_signal=False,
    )
    outcome, reasons = council_recommend_outcome(council, finance)
    assert outcome == BadRevenueCouncilOutcome.REJECT
    assert "asks_scraping" in reasons


def test_bad_revenue_council_qualified_proceed() -> None:
    council = BadRevenueCouncilSignals(
        asks_scraping=False,
        asks_cold_whatsapp_automation=False,
        asks_linkedin_automation=False,
        wants_guaranteed_sales=False,
        data_source_unclear=False,
        scope_open_ended=False,
        margin_weak=False,
        no_proof_path=False,
        no_retainer_path=False,
    )
    finance = BadRevenueSignals(
        open_scope=False,
        weak_margin=False,
        high_risk=False,
        governance_refused=False,
        wants_scraping=False,
        wants_guaranteed_sales=False,
        no_proof_path=False,
        no_retainer_path=False,
        no_productization_signal=False,
    )
    outcome, reasons = council_recommend_outcome(council, finance)
    assert outcome == BadRevenueCouncilOutcome.QUALIFIED_PROCEED
    assert reasons == ()


def test_rhythm_hire_focus_playbook_gate() -> None:
    assert (
        rhythm_hire_focus(
            stable_checklist_projects=10,
            playbooks_exist=False,
            manual_step_repeat_count=10,
            retainers_with_monthly_cadence=3,
            enterprise_governance_load=True,
            founder_delivery_bottleneck=True,
        )
        == HireFocus.NONE
    )


def test_rhythm_hire_focus_governance_priority() -> None:
    assert (
        rhythm_hire_focus(
            stable_checklist_projects=10,
            playbooks_exist=True,
            manual_step_repeat_count=10,
            retainers_with_monthly_cadence=3,
            enterprise_governance_load=True,
            founder_delivery_bottleneck=True,
        )
        == HireFocus.GOVERNANCE
    )


def test_weekly_scorecard_keys_contract() -> None:
    ok, missing = weekly_scorecard_keys_complete(frozenset({"revenue_pipeline"}))
    assert not ok
    assert "active_delivery" in missing


def test_monthly_board_memo_contract() -> None:
    ok, missing = monthly_board_memo_sections_complete({"executive_summary": "x"})
    assert not ok
    assert "revenue_quality" in missing


def test_quarterly_outputs_contract() -> None:
    ok, missing = quarterly_outputs_complete({"strategic_bet": "expand revenue os"})
    assert not ok
    assert "service_to_scale" in missing
