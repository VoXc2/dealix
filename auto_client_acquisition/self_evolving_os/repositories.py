"""Self-evolving repository that enforces propose-only behavior."""

from __future__ import annotations

from auto_client_acquisition.self_evolving_os.schemas import ImprovementProposal


class SelfEvolvingRepository:
    def __init__(self) -> None:
        self._proposals: dict[str, ImprovementProposal] = {}

    def propose(self, proposal: ImprovementProposal) -> ImprovementProposal:
        self._proposals[proposal.proposal_id] = proposal
        return proposal

    def grant_approval(self, *, proposal_id: str, ticket_id: str) -> ImprovementProposal:
        proposal = self._proposals.get(proposal_id)
        if proposal is None:
            raise ValueError("proposal_not_found")
        updated = proposal.model_copy(
            update={"approved": True, "approval_ticket_id": ticket_id, "status": "approved"},
        )
        self._proposals[proposal_id] = updated
        return updated

    def apply(self, *, proposal_id: str) -> ImprovementProposal:
        proposal = self._proposals.get(proposal_id)
        if proposal is None:
            raise ValueError("proposal_not_found")
        if not proposal.approved:
            raise ValueError("approval_required_before_apply")
        updated = proposal.model_copy(update={"status": "applied"})
        self._proposals[proposal_id] = updated
        return updated

    def get(self, *, proposal_id: str) -> ImprovementProposal | None:
        return self._proposals.get(proposal_id)

    def clear_for_test(self) -> None:
        self._proposals.clear()


__all__ = ["SelfEvolvingRepository"]
