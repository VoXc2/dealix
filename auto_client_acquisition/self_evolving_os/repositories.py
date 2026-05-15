"""Self-evolving proposal storage with strict approval gate."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.control_plane_os.tenant_context import resolve_tenant_id


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ProposalApprovalRequiredError(RuntimeError):
    status_code = 409


@dataclass(slots=True)
class ImprovementProposal:
    proposal_id: str
    tenant_id: str
    title: str
    change_summary: str
    proposed_by: str
    state: str = "pending_approval"
    metadata: dict[str, Any] = field(default_factory=dict)
    approved_by: str | None = None
    applied_by: str | None = None
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)


class InMemorySelfEvolvingRepository:
    def __init__(self) -> None:
        self._proposals: dict[str, dict[str, ImprovementProposal]] = {}

    def submit_proposal(self, proposal: ImprovementProposal) -> ImprovementProposal:
        tid = resolve_tenant_id(proposal.tenant_id)
        stored = replace(proposal, tenant_id=tid, updated_at=_now())
        self._proposals.setdefault(tid, {})[proposal.proposal_id] = stored
        return stored

    def get_proposal(self, *, tenant_id: str | None, proposal_id: str) -> ImprovementProposal:
        tid = resolve_tenant_id(tenant_id)
        return self._proposals[tid][proposal_id]

    def approve_proposal(
        self,
        *,
        tenant_id: str | None,
        proposal_id: str,
        approved_by: str,
    ) -> ImprovementProposal:
        tid = resolve_tenant_id(tenant_id)
        proposal = self.get_proposal(tenant_id=tid, proposal_id=proposal_id)
        approved = replace(
            proposal,
            state="approved",
            approved_by=approved_by,
            updated_at=_now(),
        )
        self._proposals[tid][proposal_id] = approved
        return approved

    def apply_proposal(
        self,
        *,
        tenant_id: str | None,
        proposal_id: str,
        applied_by: str,
    ) -> ImprovementProposal:
        tid = resolve_tenant_id(tenant_id)
        proposal = self.get_proposal(tenant_id=tid, proposal_id=proposal_id)
        if proposal.state != "approved":
            raise ProposalApprovalRequiredError("proposal cannot apply without approval")
        applied = replace(
            proposal,
            state="applied",
            applied_by=applied_by,
            updated_at=_now(),
        )
        self._proposals[tid][proposal_id] = applied
        return applied


__all__ = [
    "ImprovementProposal",
    "InMemorySelfEvolvingRepository",
    "ProposalApprovalRequiredError",
]
