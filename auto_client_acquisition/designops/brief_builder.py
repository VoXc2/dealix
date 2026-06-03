"""Brief builder — locks artifact requirements before generation.

Pure function. Deterministic. No LLM, no I/O.
If context is insufficient, returns a brief whose ONLY non-empty
field is `missing_context_questions` — explicit "ask before
hallucinating" semantics.
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.designops.visual_directions import (
    VISUAL_DIRECTIONS,
)

_VALID_DIRECTIONS = tuple(d["name"] for d in VISUAL_DIRECTIONS)

VisualDirection = Literal[
    "saudi_executive_trust",
    "minimal_saas_command",
    "proof_ledger_editorial",
    "growth_control_tower",
    "partnership_boardroom",
    "warm_founder_led_beta",
]

DEFAULT_VISUAL_DIRECTION: VisualDirection = "saudi_executive_trust"


class BriefRequest(BaseModel):
    """Caller-supplied context. extra='forbid' to catch typos early."""

    model_config = ConfigDict(extra="forbid")

    skill_name: str = Field(min_length=1)
    customer_handle: str = Field(min_length=1)
    language_primary: str = "ar"
    language_secondary: str = "en"
    visual_direction: VisualDirection | None = None
    sector: str | None = None
    pipeline_state: str | None = None
    proof_event_ids: list[str] = Field(default_factory=list)
    service_id: str | None = None
    notes: str | None = None


class LockedBrief(BaseModel):
    """Frozen brief. Renderers only consume this."""

    model_config = ConfigDict(extra="forbid")

    skill_name: str
    customer_handle: str
    language_primary: str
    language_secondary: str
    visual_direction: VisualDirection
    content_sections: list[dict[str, Any]] = Field(default_factory=list)
    required_evidence: list[str] = Field(default_factory=list)
    missing_context_questions: list[str] = Field(default_factory=list)
    blocked_items: list[str] = Field(default_factory=list)
    next_step: str = "await_founder_review"
    approval_status: Literal["approval_required"] = "approval_required"


# ── Section templates per skill ────────────────────────────────────
# Each entry maps skill_name → list of (id, title_ar, title_en, source_field).
_SECTION_TEMPLATES: dict[str, list[tuple[str, str, str, str]]] = {
    "default": [
        ("intro", "نظرة عامة", "Overview", "service_id"),
        ("context", "السياق", "Context", "pipeline_state"),
        ("proof", "البرهان", "Proof", "proof_event_ids"),
        ("next_step", "الخطوة التالية", "Next Step", "notes"),
    ],
}


def _missing_context(req: BriefRequest) -> list[str]:
    questions: list[str] = []
    if not req.pipeline_state:
        questions.append(
            "What is the customer's current pipeline_state? "
            "(e.g. lead_intake, diagnostic_delivered, pilot_offered)"
        )
    if not req.sector:
        questions.append(
            "Which sector is the customer in? "
            "(e.g. fintech, retail, healthcare)"
        )
    if not req.service_id:
        questions.append(
            "Which service_id is this artifact about? "
            "(e.g. svc_diagnostic_v1)"
        )
    return questions


def _build_sections(
    req: BriefRequest,
    has_proof: bool,
) -> list[dict[str, Any]]:
    template = _SECTION_TEMPLATES.get(req.skill_name, _SECTION_TEMPLATES["default"])
    sections: list[dict[str, Any]] = []
    for sid, title_ar, title_en, src in template:
        section: dict[str, Any] = {
            "id": sid,
            "title_ar": title_ar,
            "title_en": title_en,
            "source_field": src,
        }
        if sid == "proof" and not has_proof:
            section["status"] = "planned / not yet proven"
        sections.append(section)
    return sections


def build_brief(
    req: BriefRequest,
    design_system: dict | None = None,
) -> LockedBrief:
    """Lock the brief. If context insufficient, return ask-first brief."""
    direction: VisualDirection = req.visual_direction or DEFAULT_VISUAL_DIRECTION
    if direction not in _VALID_DIRECTIONS:
        # Defensive: Literal already constrains, but design_system override
        # could try to inject. Fall back to default.
        direction = DEFAULT_VISUAL_DIRECTION

    questions = _missing_context(req)
    if questions:
        return LockedBrief(
            skill_name=req.skill_name,
            customer_handle=req.customer_handle,
            language_primary=req.language_primary,
            language_secondary=req.language_secondary,
            visual_direction=direction,
            content_sections=[],
            required_evidence=[],
            missing_context_questions=questions,
            blocked_items=["insufficient_context"],
            next_step="ask_founder_for_missing_context",
            approval_status="approval_required",
        )

    has_proof = bool(req.proof_event_ids)
    sections = _build_sections(req, has_proof=has_proof)

    required_evidence: list[str] = []
    if req.service_id:
        required_evidence.append(f"service_id:{req.service_id}")
    required_evidence.extend(req.proof_event_ids)

    blocked: list[str] = []
    if not has_proof:
        blocked.append("no_proof_events_attached")

    return LockedBrief(
        skill_name=req.skill_name,
        customer_handle=req.customer_handle,
        language_primary=req.language_primary,
        language_secondary=req.language_secondary,
        visual_direction=direction,
        content_sections=sections,
        required_evidence=required_evidence,
        missing_context_questions=[],
        blocked_items=blocked,
        next_step="await_founder_review",
        approval_status="approval_required",
    )
