"""DesignOps — safety gate, brief builder, visual directions.

Phase 3 + Phase 4 modules. No LLM, no external HTTP.
Importable contracts for the artifact pipeline.
"""
from __future__ import annotations

from auto_client_acquisition.designops.brief_builder import (
    BriefRequest,
    LockedBrief,
    build_brief,
)
from auto_client_acquisition.designops.safety_gate import (
    SafetyGateResult,
    check_artifact,
)
from auto_client_acquisition.designops.visual_directions import (
    VISUAL_DIRECTIONS,
    get_direction,
)

__all__ = [
    "VISUAL_DIRECTIONS",
    "BriefRequest",
    "LockedBrief",
    "SafetyGateResult",
    "build_brief",
    "check_artifact",
    "get_direction",
]
