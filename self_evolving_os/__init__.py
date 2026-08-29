"""Legacy self-evolving compatibility package.

Proposal generation is evidence-bound and mutation authority is deactivated.
Canonical repository changes must flow through the Dealix Development Factory.
"""

from .auto_applier import (
    LEGACY_COMPATIBILITY_ONLY,
    LEGACY_DEACTIVATION_REASON,
    ApplicationResult,
    AutoApplier,
)
from .improvement_generator import (
    UNKNOWN,
    ImprovementGenerator,
    ImprovementProposal,
    ImprovementSignal,
    MetricObservation,
)
from .review_queue import ApprovalResult, ReviewQueue

__all__ = [
    "UNKNOWN",
    "MetricObservation",
    "ImprovementGenerator",
    "ImprovementProposal",
    "ImprovementSignal",
    "AutoApplier",
    "ApplicationResult",
    "LEGACY_COMPATIBILITY_ONLY",
    "LEGACY_DEACTIVATION_REASON",
    "ReviewQueue",
    "ApprovalResult",
]
