"""Pydantic v2 schemas for the DesignOps registry layer.

All models use ``extra='forbid'`` so unknown fields in YAML
front-matter or caller-supplied dicts fail loudly.

Generators in a later phase will consume ``LockedBrief`` and emit
``ArtifactManifest``; both are stubbed here at the schema level so
the registry can be wired without waiting for the renderer.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Skill — one record per design-skills/<name>/SKILL.md front-matter block.
# ---------------------------------------------------------------------------


class Skill(BaseModel):
    """A registered DesignOps skill loaded from SKILL.md front-matter."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1)
    mode: Literal["document", "report", "prototype", "email", "social", "deck"]
    scenario: Literal[
        "sales",
        "proof",
        "executive",
        "operations",
        "partnership",
        "growth",
        "customer-success",
    ]
    version: int = Field(default=1, ge=1)

    input_requirements: list[str] = Field(default_factory=list)
    output_format: list[str] = Field(default_factory=list)
    safety_rules: list[str] = Field(default_factory=list)
    approval_mode: Literal[
        "approval_required", "internal_only", "draft_only"
    ] = "approval_required"
    evidence_requirements: list[str] = Field(default_factory=list)

    arabic_first: bool = True
    english_secondary: bool = True
    forbidden_claims: list[str] = Field(default_factory=list)

    example_prompt: str = ""
    acceptance_checklist: list[str] = Field(default_factory=list)
    design_system: str = "dealix"


# NOTE: BriefRequest + LockedBrief live in brief_builder.py (Agent B).
# Re-exported through the package __init__.py.

# ---------------------------------------------------------------------------
# ArtifactManifest — placeholder. Full schema lands in the generator phase.
# ---------------------------------------------------------------------------


class ArtifactManifest(BaseModel):
    """Stub manifest for a rendered artefact. Filled in agent B."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str
    artifact_type: str
    skill_name: str
    customer_handle: str
    approval_state: Literal[
        "approval_required", "approved", "rejected", "draft_only"
    ] = "approval_required"
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
