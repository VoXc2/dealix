"""Action Engine catalog — kinds + default Trust Plane modes."""

from __future__ import annotations

from enum import StrEnum


class ActionKind(StrEnum):
    PREPARE_DIAGNOSTIC = "prepare_diagnostic"
    DRAFT_EMAIL = "draft_email"
    DRAFT_LINKEDIN_MESSAGE = "draft_linkedin_message"
    CALL_SCRIPT = "call_script"
    FOLLOW_UP_TASK = "follow_up_task"
    SUPPORT_REPLY_DRAFT = "support_reply_draft"
    PAYMENT_REMINDER = "payment_reminder"
    DELIVERY_TASK = "delivery_task"
    PROOF_REQUEST = "proof_request"
    UPSELL_RECOMMENDATION = "upsell_recommendation"
    PARTNER_INTRO = "partner_intro"
    ASSEMBLE_PROOF_PACK = "assemble_proof_pack"


class ActionMode(StrEnum):
    SUGGEST_ONLY = "suggest_only"
    DRAFT_ONLY = "draft_only"
    APPROVAL_REQUIRED = "approval_required"
    APPROVED_MANUAL = "approved_manual"
    BLOCKED = "blocked"


class ActionRiskTier(StrEnum):
    """RevOps 2026 risk-tiered governance — maps to execution autonomy."""

    GREEN = "green"  # autonomous internal (briefs, scoring, logs)
    YELLOW = "yellow"  # draft + founder one-click approval
    RED = "red"  # blocked or VP/founder sign-off only


# Default per Dealix safety rules — external sends never live-by-default.
ACTION_DEFAULT_MODE: dict[ActionKind, ActionMode] = {
    ActionKind.PREPARE_DIAGNOSTIC: ActionMode.APPROVAL_REQUIRED,
    ActionKind.DRAFT_EMAIL: ActionMode.DRAFT_ONLY,
    ActionKind.DRAFT_LINKEDIN_MESSAGE: ActionMode.DRAFT_ONLY,
    ActionKind.CALL_SCRIPT: ActionMode.SUGGEST_ONLY,
    ActionKind.FOLLOW_UP_TASK: ActionMode.APPROVAL_REQUIRED,
    ActionKind.SUPPORT_REPLY_DRAFT: ActionMode.DRAFT_ONLY,
    ActionKind.PAYMENT_REMINDER: ActionMode.APPROVAL_REQUIRED,
    ActionKind.DELIVERY_TASK: ActionMode.APPROVAL_REQUIRED,
    ActionKind.PROOF_REQUEST: ActionMode.APPROVAL_REQUIRED,
    ActionKind.UPSELL_RECOMMENDATION: ActionMode.SUGGEST_ONLY,
    ActionKind.PARTNER_INTRO: ActionMode.APPROVAL_REQUIRED,
    ActionKind.ASSEMBLE_PROOF_PACK: ActionMode.APPROVAL_REQUIRED,
}

ACTION_RISK_TIER: dict[ActionKind, ActionRiskTier] = {
    ActionKind.PREPARE_DIAGNOSTIC: ActionRiskTier.YELLOW,
    ActionKind.DRAFT_EMAIL: ActionRiskTier.YELLOW,
    ActionKind.DRAFT_LINKEDIN_MESSAGE: ActionRiskTier.YELLOW,
    ActionKind.CALL_SCRIPT: ActionRiskTier.GREEN,
    ActionKind.FOLLOW_UP_TASK: ActionRiskTier.YELLOW,
    ActionKind.SUPPORT_REPLY_DRAFT: ActionRiskTier.YELLOW,
    ActionKind.PAYMENT_REMINDER: ActionRiskTier.RED,
    ActionKind.DELIVERY_TASK: ActionRiskTier.YELLOW,
    ActionKind.PROOF_REQUEST: ActionRiskTier.YELLOW,
    ActionKind.UPSELL_RECOMMENDATION: ActionRiskTier.GREEN,
    ActionKind.PARTNER_INTRO: ActionRiskTier.YELLOW,
    ActionKind.ASSEMBLE_PROOF_PACK: ActionRiskTier.YELLOW,
}


def list_action_catalog() -> list[dict[str, str]]:
    rows = []
    for ak in ActionKind:
        rows.append(
            {
                "action": ak.value,
                "default_mode": ACTION_DEFAULT_MODE[ak].value,
                "risk_tier": ACTION_RISK_TIER[ak].value,
                "trust_plane": "input_guardrail→policy→consent→channel→pii→approval→audit→output_guardrail",
            }
        )
    return rows
