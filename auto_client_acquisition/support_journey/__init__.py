"""Support Journey upgrade (Phase 7 Wave 5).

Adds 7-stage classification on top of existing support_inbox/support_os:
  pre_sales · onboarding · delivery · billing · proof · renewal · privacy

Stage-specific draft replies + escalation policy. Reuses existing
support_os classifier + responder; never replaces.
"""
from auto_client_acquisition.support_journey.classifier import (
    classify_with_stage,
)
from auto_client_acquisition.support_journey.escalation_policy import (
    stage_escalation_policy,
)
from auto_client_acquisition.support_journey.responder import (
    draft_stage_reply,
)
from auto_client_acquisition.support_journey.stages import (
    JOURNEY_STAGES,
    STAGE_SLA_HOURS,
    is_known_stage,
)

__all__ = [
    "JOURNEY_STAGES",
    "STAGE_SLA_HOURS",
    "classify_with_stage",
    "draft_stage_reply",
    "is_known_stage",
    "stage_escalation_policy",
]
