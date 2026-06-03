"""Self-Evolving OS exports."""

from auto_client_acquisition.self_evolving_os.repositories import (
    ImprovementProposal,
    InMemorySelfEvolvingRepository,
    ProposalApprovalRequiredError,
)

__all__ = ["ImprovementProposal", "InMemorySelfEvolvingRepository", "ProposalApprovalRequiredError"]
