"""Self-evolving proposal repository (propose-only until approved)."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository
from auto_client_acquisition.self_evolving_os.schemas import ImprovementProposal


class InMemorySelfEvolvingRepository:
    def __init__(self) -> None:
        self._proposals: dict[tuple[str, str], ImprovementProposal] = {}

    def create_proposal(self, *, tenant_id: str, title: str, summary: str, proposed_by: str) -> ImprovementProposal:
        proposal = ImprovementProposal(
            proposal_id=f"imp_{uuid4().hex[:10]}",
            tenant_id=tenant_id,
            title=title,
            summary=summary,
            proposed_by=proposed_by,
        )
        self._proposals[(tenant_id, proposal.proposal_id)] = proposal
        return proposal

    def get_proposal(self, *, tenant_id: str, proposal_id: str) -> ImprovementProposal:
        try:
            return self._proposals[(tenant_id, proposal_id)]
        except KeyError as exc:
            raise ValueError("proposal_not_found") from exc

    def request_apply(
        self,
        *,
        tenant_id: str,
        proposal_id: str,
        actor: str,
        control_repo: InMemoryControlPlaneRepository,
    ) -> str:
        proposal = self.get_proposal(tenant_id=tenant_id, proposal_id=proposal_id)
        ticket = control_repo.request_policy_edit(
            tenant_id=tenant_id,
            actor=actor,
            policy_id=f"self_evolving:{proposal_id}",
            patch={"proposal_id": proposal_id, "operation": "apply"},
        )
        updated = replace(
            proposal,
            state="proposed",
            approval_ticket_id=ticket.ticket_id,
            updated_at=datetime.now(UTC).isoformat(),
        )
        self._proposals[(tenant_id, proposal_id)] = updated
        return ticket.ticket_id

    def approve_proposal(self, *, tenant_id: str, proposal_id: str, approved_by: str) -> ImprovementProposal:
        proposal = self.get_proposal(tenant_id=tenant_id, proposal_id=proposal_id)
        updated = replace(
            proposal,
            state="approved",
            approved_by=approved_by,
            updated_at=datetime.now(UTC).isoformat(),
        )
        self._proposals[(tenant_id, proposal_id)] = updated
        return updated

    def apply_proposal(self, *, tenant_id: str, proposal_id: str) -> ImprovementProposal:
        proposal = self.get_proposal(tenant_id=tenant_id, proposal_id=proposal_id)
        if proposal.state != "approved":
            raise ValueError("proposal_requires_approval")
        updated = replace(proposal, state="applied", updated_at=datetime.now(UTC).isoformat())
        self._proposals[(tenant_id, proposal_id)] = updated
        return updated
