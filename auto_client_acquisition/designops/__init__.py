"""DesignOps OS — Dealix design system + skill registry + safety gate +
brief builder + visual directions + artifact types.

Pure local composition. No LLM. No external HTTP.
"""
from __future__ import annotations

from auto_client_acquisition.designops.artifact_types import ArtifactType
from auto_client_acquisition.designops.brief_builder import (
    DEFAULT_VISUAL_DIRECTION,
    BriefRequest,
    LockedBrief,
    VisualDirection,
    build_brief,
)
from auto_client_acquisition.designops.design_system_loader import (
    load_design_system,
)
from auto_client_acquisition.designops.safety_gate import (
    SafetyGateResult,
    check_artifact,
)
from auto_client_acquisition.designops.schemas import (
    ArtifactManifest,
    Skill,
)
from auto_client_acquisition.designops.skill_registry import (
    get_skill,
    list_skills,
    validate_skill,
)
from auto_client_acquisition.designops.visual_directions import (
    VISUAL_DIRECTIONS,
    get_direction,
)

__all__ = [
    "ArtifactManifest",
    "ArtifactType",
    "BriefRequest",
    "DEFAULT_VISUAL_DIRECTION",
    "LockedBrief",
    "SafetyGateResult",
    "Skill",
    "VISUAL_DIRECTIONS",
    "VisualDirection",
    "build_brief",
    "check_artifact",
    "get_direction",
    "get_skill",
    "list_skills",
    "load_design_system",
    "validate_skill",
]
