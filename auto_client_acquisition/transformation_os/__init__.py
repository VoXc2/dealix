"""Transformation OS — the 5-stage AI transformation framework.

Assessment to Pilot to Workflow Redesign to Operational Deployment to
Governance & Scale. Each stage is tied to a rung of the offer ladder
and each transition is gated by verified evidence.
"""

from __future__ import annotations

from auto_client_acquisition.transformation_os.schemas import (
    STAGE_TO_OFFER,
    StageEvidence,
    TransformationRecord,
    TransformationStage,
)
from auto_client_acquisition.transformation_os.stage_machine import (
    ALLOWED_TRANSITIONS,
    advance_stage,
    can_advance,
)
from auto_client_acquisition.transformation_os.store import (
    clear_for_test,
    emit,
    list_records,
)

__all__ = [
    "ALLOWED_TRANSITIONS",
    "STAGE_TO_OFFER",
    "StageEvidence",
    "TransformationRecord",
    "TransformationStage",
    "advance_stage",
    "can_advance",
    "clear_for_test",
    "emit",
    "list_records",
]
