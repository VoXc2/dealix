"""Map growth_starter_7_day steps to governed draft-only actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.revenue_os.action_catalog import (
    ACTION_DEFAULT_MODE,
    ActionKind,
    ActionMode,
)
from auto_client_acquisition.workflow_os_v10.service_session_workflow import GROWTH_STARTER_7_DAY

_STEP_ACTIONS: dict[str, tuple[ActionKind, str]] = {
    "day_1_kickoff_diagnostic": (ActionKind.PREPARE_DIAGNOSTIC, "kickoff diagnostic"),
    "day_2_top10_opportunity_list": (ActionKind.FOLLOW_UP_TASK, "top-10 list"),
    "day_3_arabic_outreach_drafts": (ActionKind.DRAFT_EMAIL, "Arabic drafts"),
    "day_4_followup_plan": (ActionKind.FOLLOW_UP_TASK, "follow-up plan"),
    "day_5_proof_event_log": (ActionKind.PROOF_REQUEST, "proof log"),
    "day_6_qa_gate_review": (ActionKind.DELIVERY_TASK, "QA gate"),
    "day_7_proof_pack_assemble": (ActionKind.ASSEMBLE_PROOF_PACK, "proof pack"),
}


@dataclass(frozen=True)
class ServiceSessionStepResult:
    workflow_id: str
    step: str
    action_kind: str
    default_mode: str
    description_en: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "step": self.step,
            "action_kind": self.action_kind,
            "default_mode": self.default_mode,
            "description_en": self.description_en,
            "draft_only": True,
            "requires_approval": True,
        }


def resolve_step(step: str) -> ServiceSessionStepResult | None:
    row = _STEP_ACTIONS.get(step)
    if not row:
        return None
    kind, desc = row
    mode = ACTION_DEFAULT_MODE.get(kind, ActionMode.APPROVAL_REQUIRED)
    return ServiceSessionStepResult(
        workflow_id=GROWTH_STARTER_7_DAY.workflow_id,
        step=step,
        action_kind=kind.value,
        default_mode=mode.value,
        description_en=desc,
    )


def execute_step(step: str, *, customer_id: str = "", lead_id: str = "") -> dict[str, Any]:
    resolved = resolve_step(step)
    if not resolved:
        return {"ok": False, "error": f"unknown step: {step}"}
    return {
        "ok": True,
        "customer_id": customer_id,
        "lead_id": lead_id,
        "plan": resolved.as_dict(),
        "next": "queue_approval_center",
    }


def list_workflow_steps() -> list[dict[str, Any]]:
    return [execute_step(s)["plan"] for s in GROWTH_STARTER_7_DAY.steps if resolve_step(s)]
