"""Tests for institutional_control_os."""

from __future__ import annotations

from auto_client_acquisition.endgame_os.agent_control import AgentControlCard
from auto_client_acquisition.institutional_control_os import (
    AuditEvent,
    ControlMetricsSnapshot,
    GovernanceRuntimeSignals,
    ProofGovernanceDimensions,
    agent_control_plane_mvp_valid,
    audit_event_complete,
    enterprise_control_blockers,
    evaluate_output_governance,
    governance_runtime_checklist_passes,
    incident_control_closure_ok,
    institutional_source_ai_allowed,
    proof_case_band,
    proof_governance_score,
    proof_pack_section_coverage,
)
from auto_client_acquisition.institutional_control_os.governance_runtime import (
    RUNTIME_CHECKLIST_KEYS,
)
from auto_client_acquisition.institutional_control_os.incident_response import (
    INCIDENT_RESPONSE_STEPS,
)
from auto_client_acquisition.institutional_control_os.source_passport import SourcePassport


def test_source_passport_institutional_gate() -> None:
    ok_passport = SourcePassport(
        source_id="SRC-1",
        source_type="client_upload",
        owner="client",
        allowed_use=frozenset({"internal_analysis"}),
        contains_pii=True,
        sensitivity="medium",
        retention_policy="project_duration",
        ai_access_allowed=True,
        external_use_allowed=False,
    )
    ok, errs = institutional_source_ai_allowed(ok_passport)
    assert ok and not errs
    bad = SourcePassport(
        "",
        "x",
        "x",
        frozenset(),
        False,
        "low",
        "x",
        True,
        False,
    )
    ok2, _errs = institutional_source_ai_allowed(bad)
    assert not ok2


def test_runtime_checklist() -> None:
    full = dict.fromkeys(RUNTIME_CHECKLIST_KEYS, True)
    assert governance_runtime_checklist_passes(full) == (True, ())
    partial = dict(full)
    partial["audit_event_recorded"] = False
    ok, missing = governance_runtime_checklist_passes(partial)
    assert not ok and missing == ("audit_event_recorded",)


def test_agent_mvp_ceiling() -> None:
    card_ok = AgentControlCard(
        agent_id="A1",
        name="x",
        owner="Dealix",
        purpose="score",
        autonomy_level=3,
        audit_required=True,
    )
    assert agent_control_plane_mvp_valid(card_ok) == (True, ())
    card_high = AgentControlCard("A1", "x", "Dealix", "x", 4, True)
    ok, errs = agent_control_plane_mvp_valid(card_high)
    assert not ok and errs == ("mvp_autonomy_ceiling_exceeded",)


def test_audit_complete() -> None:
    ev = AuditEvent(
        audit_event_id="AUD-1",
        actor_type="agent",
        actor_id="AG-1",
        human_owner="o",
        action="score",
        dataset_id="DS-1",
        source_id="SRC-1",
        policy_decision="ALLOW_WITH_REVIEW",
        approval_required=False,
        timestamp="2026-05-14T10:00:00Z",
    )
    assert audit_event_complete(ev)
    assert not audit_event_complete(
        AuditEvent("AUD-1", "agent", "AG-1", "o", "score", "", "SRC-1", "ALLOW", False, "2026-01-01"),
    )


def test_proof_score_bands() -> None:
    hi = ProofGovernanceDimensions(90, 90, 90, 90, 90, 90)
    assert proof_governance_score(hi) == 90
    assert proof_case_band(90) == "case_candidate"
    assert proof_case_band(75) == "sales_support"
    assert proof_case_band(50) == "internal_learning_only"


def test_control_blockers() -> None:
    perfect = ControlMetricsSnapshot(
        pct_sources_with_passport=100.0,
        pct_ai_runs_logged=100.0,
        pct_outputs_with_governance_status=100.0,
        client_facing_qa_avg=90.0,
        pct_external_actions_with_approval=100.0,
        proof_pack_completion_rate=100.0,
        capital_assets_per_project_min=1.0,
    )
    assert enterprise_control_blockers(perfect) == ()
    bad = ControlMetricsSnapshot(
        99.0,
        100.0,
        100.0,
        90.0,
        100.0,
        100.0,
        1.0,
    )
    assert "source_passport_coverage_incomplete" in enterprise_control_blockers(bad)


def test_incident_closure() -> None:
    assert incident_control_closure_ok(rule_updated=True, test_added=False, playbook_updated=False)[0]
    assert not incident_control_closure_ok(rule_updated=False, test_added=False, playbook_updated=False)[0]


def test_incident_response_flow_defined() -> None:
    assert "detect" in INCIDENT_RESPONSE_STEPS and "update_playbook" in INCIDENT_RESPONSE_STEPS


def test_evaluate_output_governance_draft_only_pii_external() -> None:
    sig = GovernanceRuntimeSignals(
        source_passport_valid=True,
        contains_personal_contact_data=True,
        external_action_requested=True,
        human_approved_external=False,
    )
    out = evaluate_output_governance(sig, audit_event_id="AUD-001")
    assert out["decision"] == "DRAFT_ONLY"
    assert out["risk_level"] == "medium"
    assert "external_action_requires_approval" in out["matched_rules"]
    assert out["next_action"] == "human_review"


def test_evaluate_output_governance_blocks_without_passport() -> None:
    sig = GovernanceRuntimeSignals(
        source_passport_valid=False,
        contains_personal_contact_data=False,
        external_action_requested=False,
        human_approved_external=False,
    )
    out = evaluate_output_governance(sig, audit_event_id="AUD-002")
    assert out["decision"] == "BLOCK"
    assert "no_source_passport_no_ai_use" in out["matched_rules"]


def test_proof_pack_section_coverage() -> None:
    filled, total = proof_pack_section_coverage(frozenset({"problem", "inputs"}))
    assert total >= 10
    assert filled == 2
