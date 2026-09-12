from dealix.agentic_holding.governance import GovernanceEnvelope, GovernedAgentDispatcher, governance_rejection
from dealix.agentic_holding.runtime import ResourceSnapshot, WorkItem, build_registry


def _registry():
    return build_registry(["technology"], [{"arm_id": "ARM-TEST", "supported_sectors": ["technology"]}])


def _item(agent_id="dealix.group.engineering", **kwargs):
    return WorkItem("W1", agent_id, 80, 10, **kwargs)


def _snapshot():
    return ResourceSnapshot(0.1, 4096, 0.0, 0.0, 1.0, 1.0, 2, cpu_count=4)


def test_trace_is_mandatory():
    try:
        GovernanceEnvelope(_item(), "")
    except ValueError as exc:
        assert "trace_id" in str(exc)
    else:
        raise AssertionError("missing trace must fail closed")


def test_l5_and_destructive_are_blocked_before_dispatch():
    registry = _registry()
    assert governance_rejection(GovernanceEnvelope(_item(), "T1", authority_level="L5"), registry) == "exact_action_authority_required"
    assert governance_rejection(GovernanceEnvelope(_item(), "T2", effect_class="destructive"), registry) == "exact_action_authority_required"


def test_handoff_requires_complete_matching_packet():
    registry = _registry()
    envelope = GovernanceEnvelope(_item(), "T1", coordination_mode="handoff", handoff_packet={})
    assert governance_rejection(envelope, registry) == "handoff_packet_incomplete"


def test_material_output_requires_independent_known_verifier():
    registry = _registry()
    item = _item()
    assert governance_rejection(GovernanceEnvelope(item, "T1", material_output=True), registry) == "independent_verifier_required"
    assert governance_rejection(GovernanceEnvelope(item, "T1", material_output=True, verifier_agent_id=item.agent_id), registry) == "self_verification_forbidden"
    verifier = "dealix.group.qa-verification"
    assert governance_rejection(GovernanceEnvelope(item, "T1", material_output=True, verifier_agent_id=verifier), registry) is None


def test_governed_dispatcher_preserves_canonical_paid_guard():
    registry = _registry()
    paid = _item(requires_paid_model=True)
    plan = GovernedAgentDispatcher().dispatch([GovernanceEnvelope(paid, "T1")], registry=registry, snapshot=_snapshot())
    assert plan.selected == ()
    assert plan.rejected[paid.work_id] == "paid_spill_blocked"


def test_governed_dispatcher_selects_safe_internal_work():
    registry = _registry()
    item = _item()
    plan = GovernedAgentDispatcher().dispatch([GovernanceEnvelope(item, "T1")], registry=registry, snapshot=_snapshot())
    assert [work.work_id for work in plan.selected] == ["W1"]
