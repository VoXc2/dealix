from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from dealix.agentic_holding.runtime import (
    AgentDispatcher,
    AgentHierarchyRegistry,
    DispatchPlan,
    ResourceSnapshot,
    WorkItem,
)

EFFECT_CLASSES = frozenset({"read_only", "reversible_internal", "material_external", "destructive"})
COORDINATION_MODES = frozenset({"manager", "handoff"})
HANDOFF_REQUIRED_FIELDS = frozenset({
    "trace_id", "source_agent", "target_agent", "reason", "scope", "facts", "inferences",
    "evidence_refs", "authority_scope", "relationship_state", "consent_state", "context_filter",
    "expected_output", "acceptance_criteria", "next_state_sought",
})


@dataclass(frozen=True, slots=True)
class GovernanceEnvelope:
    work_item: WorkItem
    trace_id: str
    authority_level: str = "L3"
    effect_class: str = "reversible_internal"
    coordination_mode: str = "manager"
    source_agent_id: str | None = None
    handoff_packet: Mapping[str, Any] | None = None
    evidence_refs: tuple[str, ...] = ()
    acceptance_criteria: str = "acceptance evidence required"
    material_output: bool = False
    verifier_agent_id: str | None = None

    def __post_init__(self) -> None:
        if not self.trace_id.strip():
            raise ValueError("trace_id is required")
        if self.authority_level not in {"L0", "L1", "L2", "L3", "L4", "L5"}:
            raise ValueError("authority_level must be L0-L5")
        if self.effect_class not in EFFECT_CLASSES:
            raise ValueError("invalid effect_class")
        if self.coordination_mode not in COORDINATION_MODES:
            raise ValueError("invalid coordination_mode")


def governance_rejection(envelope: GovernanceEnvelope, registry: AgentHierarchyRegistry) -> str | None:
    item = envelope.work_item
    if envelope.authority_level == "L5" or item.material_external_effect or envelope.effect_class in {
        "material_external", "destructive"
    }:
        return "exact_action_authority_required"

    if envelope.coordination_mode == "handoff":
        packet = dict(envelope.handoff_packet or {})
        if not HANDOFF_REQUIRED_FIELDS <= set(packet):
            return "handoff_packet_incomplete"
        if packet.get("trace_id") != envelope.trace_id:
            return "handoff_trace_mismatch"
        if packet.get("target_agent") != item.agent_id:
            return "handoff_target_mismatch"

        # A handoff is an explicit agent-to-agent authority transfer. The source
        # identity must therefore be present, registry-backed, distinct from the
        # target, and identical to the packet identity. Omitting source_agent_id
        # must never turn an arbitrary packet string into trusted provenance.
        source = (envelope.source_agent_id or "").strip()
        if not source:
            return "handoff_source_required"
        if source not in registry.agents:
            return "unknown_source_agent"
        if source == item.agent_id:
            return "self_handoff_forbidden"
        if packet.get("source_agent") != source:
            return "handoff_source_mismatch"

    if envelope.material_output:
        verifier = envelope.verifier_agent_id
        if not verifier:
            return "independent_verifier_required"
        if verifier == item.agent_id:
            return "self_verification_forbidden"
        if verifier not in registry.agents:
            return "unknown_verifier_agent"
    return None


class GovernedAgentDispatcher:
    """Governance gate layered over the merged ResourceGovernor/AgentDispatcher.

    It deliberately delegates resource, paid-approval, model-capacity and worktree decisions
    to the canonical dispatcher rather than duplicating them.
    """

    def __init__(self, dispatcher: AgentDispatcher | None = None) -> None:
        self.dispatcher = dispatcher or AgentDispatcher()

    def dispatch(
        self,
        envelopes: Sequence[GovernanceEnvelope],
        *,
        registry: AgentHierarchyRegistry,
        snapshot: ResourceSnapshot,
    ) -> DispatchPlan:
        rejected: dict[str, str] = {}
        eligible: list[WorkItem] = []

        # work_id is the durable identity in DispatchPlan receipts. Duplicates
        # make a receipt ambiguous (the same id can otherwise appear selected
        # and rejected at once), so every occurrence of a duplicate fails closed.
        work_id_counts = Counter(envelope.work_item.work_id for envelope in envelopes)
        duplicate_ids = {work_id for work_id, count in work_id_counts.items() if count > 1}

        for envelope in envelopes:
            work_id = envelope.work_item.work_id
            if work_id in duplicate_ids:
                rejected[work_id] = "duplicate_work_id"
                continue
            reason = governance_rejection(envelope, registry)
            if reason:
                rejected[work_id] = reason
            else:
                eligible.append(envelope.work_item)

        base_plan = self.dispatcher.dispatch(eligible, registry=registry, snapshot=snapshot)
        return DispatchPlan(
            selected=base_plan.selected,
            rejected={**rejected, **base_plan.rejected},
            budget=base_plan.budget,
        )


def governance_context_refs(envelope: GovernanceEnvelope) -> tuple[str, ...]:
    refs = [
        f"trace_id:{envelope.trace_id}",
        f"authority_level:{envelope.authority_level}",
        f"effect_class:{envelope.effect_class}",
        f"coordination_mode:{envelope.coordination_mode}",
    ]
    if envelope.source_agent_id:
        refs.append(f"source_agent:{envelope.source_agent_id}")
    if envelope.verifier_agent_id:
        refs.append(f"verifier_agent:{envelope.verifier_agent_id}")
    refs.extend(f"evidence:{ref}" for ref in envelope.evidence_refs)
    return tuple(refs)
