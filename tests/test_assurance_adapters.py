"""Assurance System — adapter tests.

The doctrine hinge: an unwired source returns Status.UNKNOWN with
value=None — never a fabricated number.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters import (
    ApprovalAdapter,
    ClaimAdapter,
    EvidenceAdapter,
    KpiAdapter,
    PipelineAdapter,
    ScorecardAdapter,
)
from auto_client_acquisition.assurance_os.models import AssuranceInputs, Status


def test_approval_channel_policy_is_real() -> None:
    res = ApprovalAdapter().channel_policy()
    assert res.status is Status.OK
    assert "whatsapp" in res.value


def test_approval_live_stats_real_even_when_empty() -> None:
    res = ApprovalAdapter().live_stats()
    assert res.status is Status.OK
    assert res.value["high_risk_auto_send"] >= 0


def test_claim_adapter_reads_yaml() -> None:
    assert ClaimAdapter().non_negotiables().status is Status.OK
    assert len(ClaimAdapter().non_negotiables().value) == 11
    assert ClaimAdapter().forbidden_claims().value


def test_pipeline_ladder_and_journey() -> None:
    ladder = PipelineAdapter().ladder()
    assert ladder.status is Status.OK
    assert len(ladder.value["ladder"]) == 10
    assert PipelineAdapter().journey_stages().status is Status.OK


def test_unwired_sources_return_unknown_not_fake() -> None:
    empty = AssuranceInputs()
    # pipeline counts, kpi values, evidence completeness, scorecards
    assert PipelineAdapter().counts(empty).status is Status.UNKNOWN
    assert PipelineAdapter().counts(empty).value is None
    assert KpiAdapter().values(empty).status is Status.UNKNOWN
    assert EvidenceAdapter().completeness_pct(empty).status is Status.UNKNOWN
    assert ScorecardAdapter().maturity("sales_autopilot", empty).status is Status.UNKNOWN


def test_kpi_north_star_definitions_are_real() -> None:
    res = KpiAdapter().north_star()
    assert res.status is Status.OK
    assert "primary" in res.value


def test_scorecard_adapter_rejects_out_of_range() -> None:
    bad = AssuranceInputs(machine_maturity={"sales_autopilot": 9})
    assert ScorecardAdapter().maturity("sales_autopilot", bad).status is Status.ERROR
    good = AssuranceInputs(machine_maturity={"sales_autopilot": 4})
    res = ScorecardAdapter().maturity("sales_autopilot", good)
    assert res.status is Status.OK and res.value == 4
