"""LeadOps Spine — connects intake → normalize → dedupe → compliance →
enrich → score → brief → offer route → next action → draft → approval.

Each step is a thin wrapper around an existing module. The Spine
itself is just the orchestrator that runs them in order, persists the
LeadOpsRecord envelope, and routes drafts to the approval queue.

See: docs/FULL_OPS_10_LAYER_CURRENT_REALITY.md (Layer 1) for the
reuse map this spine sits on top of.
"""
from auto_client_acquisition.leadops_spine.compliance_gate import (
    check_compliance,
)
from auto_client_acquisition.leadops_spine.draft_builder import build_draft
from auto_client_acquisition.leadops_spine.next_action import (
    suggest_next_action,
)
from auto_client_acquisition.leadops_spine.offer_router import route_offer
from auto_client_acquisition.leadops_spine.orchestrator import (
    debug_lead,
    list_records,
    run_pipeline,
)

__all__ = [
    "build_draft",
    "check_compliance",
    "debug_lead",
    "list_records",
    "route_offer",
    "run_pipeline",
    "suggest_next_action",
]
