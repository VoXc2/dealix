"""Self-evolving OS (propose-only, approval gated for apply)."""

from auto_client_acquisition.self_evolving_os.repositories import SelfEvolvingRepository
from auto_client_acquisition.self_evolving_os.schemas import ImprovementProposal

__all__ = ["ImprovementProposal", "SelfEvolvingRepository"]
