"""System 35 — Self-Evolving Enterprise Fabric.

Meta-learning and continuous optimization — proposes improvements, applies none
without an approved ticket.
"""

from auto_client_acquisition.self_evolving_os.core import (
    ProposalNotApprovedError,
    SelfEvolvingError,
    SelfEvolvingFabric,
    get_self_evolving_fabric,
    reset_self_evolving_fabric,
)
from auto_client_acquisition.self_evolving_os.schemas import (
    ImprovementProposal,
    ImprovementTarget,
    MetaLearningInsight,
    ProposalStatus,
)

__all__ = [
    "ImprovementProposal",
    "ImprovementTarget",
    "MetaLearningInsight",
    "ProposalNotApprovedError",
    "ProposalStatus",
    "SelfEvolvingError",
    "SelfEvolvingFabric",
    "get_self_evolving_fabric",
    "reset_self_evolving_fabric",
]
