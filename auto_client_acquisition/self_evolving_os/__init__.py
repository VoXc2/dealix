"""Self-evolving OS package."""

from auto_client_acquisition.self_evolving_os.repositories import InMemorySelfEvolvingRepository
from auto_client_acquisition.self_evolving_os.schemas import ImprovementProposal

__all__ = ["ImprovementProposal", "InMemorySelfEvolvingRepository"]
