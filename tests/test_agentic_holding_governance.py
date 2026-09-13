from dealix.agentic_holding.governance import GovernanceEnvelope, GovernedAgentDispatcher, governance_rejection
from dealix.agentic_holding.runtime import ResourceSnapshot, WorkItem, build_registry


def _registry():
    return build_registry(["technology"], [{"arm_id": "ARM-TEST", "supported_sectors": ["technology"]}])


def _item(agent_id="dealix.group.engineering", *, work_id="W1", **kwargs):
    return WorkItem(work_id, agent_id, 80, 10, **kwargs)


def _snapshot():
    return ResourceSnapshot(0.1, 4096, 0.0, 0.0, 1.0, 1.0, 2, cpu_count=4)


def _handoff_packet(*, source="dealix.group.research-intelligence", target="dealix.group.engineering", trace="T1"):
    return {
        "trace_id": trace,
        "source_agent": source,
        "target_agent": target,
        "reason": "bounded ownership transfer",
        "scope": "research finding to engineering acceptance",
        "facts": ["source evidence attached"],
        "inferences": [],
        "evidence_refs": ["proof:test"],
        "authority_scope": "L0-L4",
        "relationship_state": "INTERNAL_ONLY",
        "consent_state": "NOT_APPLICABLE",
        "context_filter": "minimum necessary",
        "expected_output": "accepted bounded artifact",
        "acceptance_criteria": "independent evidence required",
        "next_state_sought": "VERIFYING",
    }


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


def test_handoff_requires_registry_backed_source_identity():
    registry = _registry()
    packet = _handoff_packet()
    missing_source = GovernanceEnvelope(
        _item(), "T1", coordination_mode="handoff", handoff_packet=packet
    )
    assert governance_rejection(missing_source, registry) == "handoff_source_required"

    unknown_source = GovernanceEnvelope(
        _item(),
        "T1",
        coordination_mode="handoff",
        source_agent_id="dealix.group.not-a-real-agent",
        handoff_packet={**packet, "source_agent": "dealix.group.not-a-real-agent"},
    )
    assert governance_rejection(unknown_source, registry) == "unknown_source_agent"


def test_handoff_forbids_self_transfer_and_requires_packet_identity_match():
    registry = _registry()
    target = "dealix.group.engineering"
    self_packet = _handoff_packet(source=target, target=target)
    self_handoff = GovernanceEnvelope(
        _item(target),
        "T1",
        coordination_mode="handoff",
        source_agent_id=target,
        handoff_packet=self_packet,
    )
    assert governance_rejection(self_handoff, registry) == "self_handoff_forbidden"

    source = "dealix.group.research-intelligence"
    mismatch = GovernanceEnvelope(
        _item(target),
        "T1",
        coordination_mode="handoff",
        source_agent_id=source,
        handoff_packet=_handoff_packet(source="dealix.group.qa-verification", target=target),
    )
    assert governance_rejection(mismatch, registry) == "handoff_source_mismatch"


def test_valid_handoff_is_accepted():
    registry = _registry()
    source = "dealix.group.research-intelligence"
    target = "dealix.group.engineering"
    envelope = GovernanceEnvelope(
        _item(target),
        "T1",
        coordination_mode="handoff",
        source_agent_id=source,
        handoff_packet=_handoff_packet(source=source, target=target),
    )
    assert governance_rejection(envelope, registry) is None


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


def test_governed_dispatcher_fails_closed_on_duplicate_work_id():
    registry = _registry()
    first = _item(work_id="W-DUP")
    second = _item(agent_id="dealix.group.qa-verification", work_id="W-DUP")
    plan = GovernedAgentDispatcher().dispatch(
        [GovernanceEnvelope(first, "T1"), GovernanceEnvelope(second, "T2")],
        registry=registry,
        snapshot=_snapshot(),
    )
    assert plan.selected == ()
    assert plan.rejected == {"W-DUP": "duplicate_work_id"}
