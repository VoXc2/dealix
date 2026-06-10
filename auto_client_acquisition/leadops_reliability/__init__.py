"""LeadOps Reliability + Debug overlay (Phase 4 Wave 5).

Read-only diagnostic layer over leadops_spine. Tells the founder:
- is the LeadOps pipeline healthy?
- where are leads stuck?
- which fix to apply next?

NEVER mutates state. Composed entirely from existing modules.
"""
from auto_client_acquisition.leadops_reliability.debug import diagnose
from auto_client_acquisition.leadops_reliability.next_fix import suggest_next_fix
from auto_client_acquisition.leadops_reliability.queue_health import (
    queue_health,
)
from auto_client_acquisition.leadops_reliability.source_health import (
    source_health,
)
from auto_client_acquisition.leadops_reliability.status import overall_status

__all__ = [
    "diagnose",
    "overall_status",
    "queue_health",
    "source_health",
    "suggest_next_fix",
]
