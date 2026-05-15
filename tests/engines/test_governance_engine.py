"""Governance Engine (Engine 4) — production-depth behaviour."""

from __future__ import annotations

import pytest

from dealix.classifications import ApprovalClass, ReversibilityClass, SensitivityClass
from dealix.contracts.decision import DecisionOutput, Evidence, NextAction
from dealix.engines.base import EngineStatus, PlannedCapabilityError
from dealix.engines.governance import GovernanceEngine
from dealix.trust.approval import ApprovalCenter
from dealix.trust.audit import InMemoryAuditSink
from dealix.trust.policy import PolicyDecision, PolicyEvaluator


def _decision(action: NextAction, *, evidence: bool = False) -> DecisionOutput:
    return DecisionOutput(
        entity_id="lead_1",
        objective="qualify_lead",
        agent_name="test_agent",
        recommendation={"verdict": "qualified"},
        confidence=0.9,
        rationale="test rationale",
        approval_class=ApprovalClass.A0,
        reversibility_class=ReversibilityClass.R0,
        sensitivity_class=SensitivityClass.S1,
        evidence=[Evidence(source="hubspot.contact", excerpt="x")] if evidence else [],
        next_actions=[action],
    )


def _action(action_type: str, a: ApprovalClass, r: ReversibilityClass, s: SensitivityClass) -> NextAction:
    return NextAction(
        action_type=action_type,
        description=f"do {action_type}",
        approval_class=a,
        reversibility_class=r,
        sensitivity_class=s,
    )


def test_engine_binds_governance_spec_at_production_status() -> None:
    engine = GovernanceEngine()
    assert engine.spec.engine_id == "governance"
    assert engine.spec.status == EngineStatus.PRODUCTION


def test_routine_action_is_allowed() -> None:
    engine = GovernanceEngine()
    action = _action("icp_match", ApprovalClass.A0, ReversibilityClass.R0, SensitivityClass.S1)
    result = engine.evaluate_decision(_decision(action))
    assert len(result.evaluations) == 1
    assert result.evaluations[0].verdict == PolicyDecision.ALLOW


def test_never_auto_execute_action_escalates() -> None:
    engine = GovernanceEngine()
    action = _action(
        "pricing_offer_commit", ApprovalClass.A3, ReversibilityClass.R3, SensitivityClass.S3
    )
    result = engine.evaluate_decision(_decision(action, evidence=True))
    ev = result.evaluations[0]
    assert ev.verdict == PolicyDecision.ESCALATE
    assert ev.rule_fired == "never_auto_execute"
    assert ev.required_approvers == 2


def test_evaluation_emits_audit_entries() -> None:
    engine = GovernanceEngine()
    action = _action("icp_match", ApprovalClass.A0, ReversibilityClass.R0, SensitivityClass.S1)
    before = len(engine.recent_audit(limit=10_000))
    result = engine.evaluate_decision(_decision(action))
    after = len(engine.recent_audit(limit=10_000))
    assert after > before
    assert result.audit_ids


def test_submit_approvals_raises_approval_request() -> None:
    engine = GovernanceEngine()
    action = _action(
        "contract_change", ApprovalClass.A3, ReversibilityClass.R3, SensitivityClass.S3
    )
    result = engine.evaluate_decision(_decision(action, evidence=True), submit_approvals=True)
    assert result.evaluations[0].approval_request_id is not None
    assert engine.capabilities.approval.list_pending()


def test_explain_decision_replays_audit_chain() -> None:
    engine = GovernanceEngine()
    action = _action("icp_match", ApprovalClass.A0, ReversibilityClass.R0, SensitivityClass.S1)
    decision = _decision(action)
    engine.evaluate_decision(decision)
    explanations = engine.explain_decision(decision.decision_id)
    assert len(explanations) == 1
    assert explanations[0].decision_id == decision.decision_id


def test_explanation_is_bilingual() -> None:
    engine = GovernanceEngine()
    action = _action(
        "nda_send", ApprovalClass.A3, ReversibilityClass.R3, SensitivityClass.S3
    )
    result = engine.evaluate_decision(_decision(action, evidence=True))
    expl = result.evaluations[0].explanation
    assert expl.human_readable_en
    assert expl.human_readable_ar
    assert expl.human_readable_en != expl.human_readable_ar


def test_decision_without_actions_is_noted_not_faked() -> None:
    engine = GovernanceEngine()
    decision = DecisionOutput(
        entity_id="lead_2",
        objective="qualify_lead",
        agent_name="test_agent",
        recommendation={"x": 1},
        confidence=0.9,
        rationale="r",
        approval_class=ApprovalClass.A0,
        reversibility_class=ReversibilityClass.R0,
        sensitivity_class=SensitivityClass.S1,
        next_actions=[],
    )
    result = engine.evaluate_decision(decision)
    assert result.evaluations == []
    assert result.note is not None


def test_risk_snapshot_is_composed() -> None:
    engine = GovernanceEngine()
    snapshot = engine.risk_snapshot()
    # NEVER_AUTO_EXECUTE is always available — a non-empty signal proves composition.
    assert snapshot.never_auto_execute_actions


def test_capability_catalog_has_six_entries() -> None:
    engine = GovernanceEngine()
    catalog = engine.capabilities.catalog()
    names = {c["name"] for c in catalog}
    assert names == {"policy", "approval", "audit", "compliance", "risk", "explainability"}


def test_engine_reuses_trust_plane_components_not_reimplements() -> None:
    """The engine composes existing Trust Plane classes — it does not reinvent them."""
    evaluator = PolicyEvaluator()
    center = ApprovalCenter()
    sink = InMemoryAuditSink()
    engine = GovernanceEngine(
        policy_evaluator=evaluator, approval_center=center, audit_sink=sink
    )
    assert engine.capabilities.policy._evaluator is evaluator
    assert engine.capabilities.approval._center is center
    assert engine.capabilities.audit._sink is sink


def test_planned_capability_fails_loudly() -> None:
    """no_silent_failures — an unbuilt capability raises, never fakes a result."""
    from dealix.engines.agent_runtime import AgentRuntimeEngine

    with pytest.raises(PlannedCapabilityError):
        AgentRuntimeEngine().plan()
