"""System 35 — the Self-Evolving Enterprise Fabric.

Meta-learning, meta-orchestration and continuous optimization: the fabric
mines control-plane history for patterns and proposes improvements to
workflows, governance and orchestration.

It is strictly **propose-don't-execute**. `propose_improvement` only ever
creates a proposal plus an approval-gate ticket — status is always `proposed`.
`apply_proposal` raises `ProposalNotApprovedError` unless the proposal's ticket
has been granted. There is no auto-apply path, which is what keeps
`no_unaudited_changes` and approval-first intact.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.control_plane_os.approval_gate import (
    ControlApprovalGate,
    get_approval_gate,
)
from auto_client_acquisition.control_plane_os.ledger import (
    ControlEventType,
    ControlLedger,
    emit,
    get_control_ledger,
)
from auto_client_acquisition.self_evolving_os.schemas import (
    ImprovementProposal,
    ImprovementTarget,
    MetaLearningInsight,
    ProposalStatus,
)
from auto_client_acquisition.value_engine_os.core import get_value_engine

_MODULE = "self_evolving_os"


class ProposalNotApprovedError(RuntimeError):
    """Raised when `apply_proposal` runs without a granted approval ticket."""


class SelfEvolvingError(ValueError):
    """Raised on an invalid self-evolving operation — never swallowed."""


class SelfEvolvingFabric:
    """Mines patterns and proposes improvements — applies none without approval."""

    def __init__(
        self,
        *,
        gate: ControlApprovalGate | None = None,
        ledger: ControlLedger | None = None,
    ) -> None:
        self._proposals: dict[str, ImprovementProposal] = {}
        self._gate = gate or get_approval_gate()
        self._ledger = ledger or get_control_ledger()

    def analyze(self) -> list[MetaLearningInsight]:
        """Mine control-plane history + value ROI for improvement patterns."""
        insights: list[MetaLearningInsight] = []
        events = self._ledger.list_events(limit=1000)

        counts: dict[str, list[str]] = {}
        for event in events:
            counts.setdefault(str(event.event_type), []).append(event.id)

        failed = counts.get(ControlEventType.CONTRACT_FAILED.value, [])
        if len(failed) >= 3:
            insights.append(
                MetaLearningInsight(
                    pattern="recurring assurance-contract failures — tighten preconditions",
                    evidence_refs=failed[:20],
                    confidence=min(0.95, 0.5 + 0.05 * len(failed)),
                )
            )

        circuits = counts.get(ControlEventType.CIRCUIT_OPENED.value, [])
        if circuits:
            insights.append(
                MetaLearningInsight(
                    pattern="circuit breakers opening — review failing targets",
                    evidence_refs=circuits[:20],
                    confidence=min(0.9, 0.6 + 0.1 * len(circuits)),
                )
            )

        for workflow_id in get_value_engine().optimization_candidates():
            insights.append(
                MetaLearningInsight(
                    pattern=f"workflow '{workflow_id}' has low efficiency gain",
                    evidence_refs=[],
                    confidence=0.7,
                )
            )
        return insights

    def propose_improvement(
        self,
        *,
        target: ImprovementTarget | str,
        target_id: str,
        current_state: dict[str, Any] | None = None,
        proposed_change: dict[str, Any] | None = None,
        rationale: str = "",
        expected_gain: dict[str, Any] | None = None,
    ) -> ImprovementProposal:
        """Create an improvement proposal. Always `proposed` — never applied here."""
        proposal = ImprovementProposal(
            target=ImprovementTarget(target),
            target_id=target_id,
            current_state=current_state or {},
            proposed_change=proposed_change or {},
            rationale=rationale,
            expected_gain=expected_gain or {},
            status=ProposalStatus.PROPOSED,
        )
        ticket = self._gate.submit(
            action_type="apply_improvement",
            description=f"Apply improvement to {proposal.target}:{target_id}",
            requested_by=_MODULE,
            source_module=_MODULE,
            subject_type="improvement_proposal",
            subject_id=proposal.proposal_id,
        )
        proposal.approval_ticket_id = ticket.ticket_id
        self._proposals[proposal.proposal_id] = proposal
        emit(
            event_type=ControlEventType.IMPROVEMENT_PROPOSED,
            source_module=_MODULE,
            subject_type="improvement_proposal",
            subject_id=proposal.proposal_id,
            decision="escalate",
            payload={
                "target": str(proposal.target),
                "target_id": target_id,
                "ticket_id": ticket.ticket_id,
            },
        )
        return proposal

    def apply_proposal(
        self, proposal_id: str, *, actor: str = "system"
    ) -> ImprovementProposal:
        """Apply a proposal — only if its approval ticket has been granted."""
        proposal = self._proposals.get(proposal_id)
        if proposal is None:
            raise SelfEvolvingError(f"proposal not found: {proposal_id}")
        if proposal.status == ProposalStatus.APPLIED:
            raise SelfEvolvingError(f"proposal {proposal_id} already applied")
        ticket_id = proposal.approval_ticket_id
        if not ticket_id or not self._gate.is_granted(ticket_id):
            raise ProposalNotApprovedError(
                f"proposal {proposal_id} has no granted approval ticket — "
                "cannot apply (propose-don't-execute)"
            )
        proposal.status = ProposalStatus.APPLIED
        emit(
            event_type=ControlEventType.IMPROVEMENT_APPLIED,
            source_module=_MODULE,
            actor=actor,
            subject_type="improvement_proposal",
            subject_id=proposal_id,
            decision="allow",
            payload={
                "target": str(proposal.target),
                "target_id": proposal.target_id,
                "ticket_id": ticket_id,
                "proposed_change": proposal.proposed_change,
            },
        )
        return proposal

    def get_proposal(self, proposal_id: str) -> ImprovementProposal | None:
        return self._proposals.get(proposal_id)

    def list_proposals(
        self, *, status: str | None = None
    ) -> list[ImprovementProposal]:
        proposals = list(self._proposals.values())
        if status:
            proposals = [p for p in proposals if str(p.status) == status]
        return proposals


_FABRIC: SelfEvolvingFabric | None = None


def get_self_evolving_fabric() -> SelfEvolvingFabric:
    """Return the process-scoped self-evolving fabric singleton."""
    global _FABRIC
    if _FABRIC is None:
        _FABRIC = SelfEvolvingFabric()
    return _FABRIC


def reset_self_evolving_fabric() -> None:
    """Test helper: drop the cached fabric."""
    global _FABRIC
    _FABRIC = None


__all__ = [
    "ProposalNotApprovedError",
    "SelfEvolvingError",
    "SelfEvolvingFabric",
    "get_self_evolving_fabric",
    "reset_self_evolving_fabric",
]
