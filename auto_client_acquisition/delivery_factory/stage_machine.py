"""Stage Machine — 8-stage Delivery Standard state transitions.

آلة الحالات لمراحل التسليم الثماني (Discover → Diagnose → Design → Build →
Validate → Deliver → Prove → Expand).

Pure state machine. Persistence and event emission happen in the wiring
layer (delivery_event_writer.py) so this module stays trivially testable.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.delivery_factory.delivery_checklist import (
    STAGES_ORDER,
    Stage,
)
from core.logging import get_logger

log = get_logger(__name__)


class TransitionError(ValueError):
    """Raised when an invalid stage transition is requested."""


class StageTransition(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")
    project_id: str
    from_stage: Stage | None
    to_stage: Stage
    actor: str
    note_ar: str | None = None
    note_en: str | None = None
    at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class ProjectState(BaseModel):
    """Mutable-by-replacement project state. The store of record is the event log."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")
    project_id: str = Field(default_factory=lambda: f"prj_{uuid4().hex[:12]}")
    current_stage: Stage = Stage.DISCOVER
    transitions: list[StageTransition] = Field(default_factory=list)
    ships: bool | None = None  # set by Validate -> Deliver decision
    quality_score: int | None = None
    proof_pack_ref: str | None = None
    handoff_ref: str | None = None
    renewal_ref: str | None = None
    closed_at: str | None = None


def _index_of(stage: Stage) -> int:
    return STAGES_ORDER.index(stage)


def can_transition(
    state: ProjectState, to_stage: Stage, *, ships: bool | None = None
) -> tuple[bool, str | None]:
    """Return (ok, reason_if_not).

    Rules:
    - Forward only by one stage.
    - Validate → Deliver is gated on ships == True.
    - Cannot go past Expand.
    """
    current_idx = _index_of(Stage(state.current_stage))
    target_idx = _index_of(to_stage)

    if target_idx <= current_idx:
        return False, f"cannot move backwards from {state.current_stage} to {to_stage}"
    if target_idx - current_idx > 1:
        return False, f"must advance one stage at a time; cannot skip from {state.current_stage} to {to_stage}"
    if Stage(state.current_stage) == Stage.VALIDATE and to_stage == Stage.DELIVER:
        if ships is not True:
            return False, "Validate → Deliver blocked: QA `ships` must be True"
    return True, None


def transition(
    state: ProjectState,
    to_stage: Stage,
    actor: str,
    *,
    ships: bool | None = None,
    note_ar: str | None = None,
    note_en: str | None = None,
) -> ProjectState:
    """Apply a transition, returning a new state. Raises TransitionError on failure."""
    ok, reason = can_transition(state, to_stage, ships=ships)
    if not ok:
        raise TransitionError(reason or "invalid transition")

    new_transition = StageTransition(
        project_id=state.project_id,
        from_stage=Stage(state.current_stage),
        to_stage=to_stage,
        actor=actor,
        note_ar=note_ar,
        note_en=note_en,
    )
    log.info(
        "delivery_stage_transition",
        project_id=state.project_id,
        from_stage=str(state.current_stage),
        to_stage=str(to_stage),
        actor=actor,
    )
    return state.model_copy(
        update={
            "current_stage": to_stage,
            "transitions": [*state.transitions, new_transition],
            "ships": ships if to_stage == Stage.DELIVER else state.ships,
            "closed_at": datetime.now(UTC).isoformat()
            if to_stage == Stage.EXPAND
            else state.closed_at,
        }
    )


def start_project(project_id: str | None = None, actor: str = "system") -> ProjectState:
    """Create a fresh project in Discover with an initial transition record."""
    pid = project_id or f"prj_{uuid4().hex[:12]}"
    initial = StageTransition(
        project_id=pid,
        from_stage=None,
        to_stage=Stage.DISCOVER,
        actor=actor,
        note_en="Project started",
        note_ar="بدء المشروع",
    )
    return ProjectState(
        project_id=pid,
        current_stage=Stage.DISCOVER,
        transitions=[initial],
    )


def progress_summary(state: ProjectState) -> dict[str, Any]:
    """Compact summary suitable for dashboards."""
    return {
        "project_id": state.project_id,
        "current_stage": state.current_stage,
        "stages_done": [t.to_stage for t in state.transitions if t.from_stage is not None],
        "transitions_count": len(state.transitions),
        "ships": state.ships,
        "quality_score": state.quality_score,
        "proof_pack_ref": state.proof_pack_ref,
        "handoff_ref": state.handoff_ref,
        "renewal_ref": state.renewal_ref,
        "closed_at": state.closed_at,
    }
