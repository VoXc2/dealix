"""Ops Console — Board Decision OS.

نظام قرارات المجلس.

GET /api/v1/ops/board
  Governed-decision classification across canonical action types, the four
  decision-passport hard rules, and a risk register drawn from proof-ledger
  events flagged medium/high risk. Read-only; admin-key gated.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.routers.domains.ops_console._common import governed
from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/ops/board",
    tags=["Ops Console — Board Decision OS"],
    dependencies=[Depends(require_admin_key)],
)

# Canonical action types — classified live by the governance runtime so the
# board sees exactly how each is gated.
_SAMPLE_ACTIONS = (
    "draft_email",
    "send_external_message",
    "draft_linkedin_message",
    "payment_reminder",
    "assemble_proof_pack",
    "partner_intro",
)

_PASSPORT_RULES = (
    {
        "rule": "no_decision_passport_no_action",
        "en": "No external action without a decision passport.",
        "ar": "لا إجراء خارجي بدون جواز قرار.",
    },
    {
        "rule": "no_proof_target_no_action",
        "en": "No action without a defined proof target.",
        "ar": "لا إجراء بدون هدف إثبات محدد.",
    },
    {
        "rule": "no_owner_not_operational",
        "en": "No action without a named owner.",
        "ar": "لا إجراء بدون مالك محدد.",
    },
    {
        "rule": "no_safe_channel_blocked",
        "en": "Action is blocked when no safe channel is available.",
        "ar": "يُحظر الإجراء عند عدم توفر قناة آمنة.",
    },
)


def _governed_decisions() -> list[dict[str, Any]]:
    from auto_client_acquisition.governance_os.runtime_decision import decide

    rows: list[dict[str, Any]] = []
    for action in _SAMPLE_ACTIONS:
        d = decide(action_type=action, context={}, actor="ops_console", risk_score=None)
        rows.append(
            {
                "action_type": action,
                "decision": str(getattr(d, "decision", "")),
                "reason": getattr(d, "reason", ""),
                "risk_level": getattr(d, "risk_level", ""),
                "approval_required": getattr(d, "approval_required", None),
                "safe_alternative": getattr(d, "safe_alternative", ""),
            }
        )
    return rows


def _risk_register() -> list[dict[str, Any]]:
    from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger

    register: list[dict[str, Any]] = []
    for e in get_default_ledger().list_events(limit=200):
        risk_level = str(getattr(e, "risk_level", "") or "").lower()
        if risk_level not in ("high", "medium"):
            continue
        register.append(
            {
                "id": getattr(e, "id", ""),
                "event_type": str(getattr(e, "event_type", "")),
                "risk_level": risk_level,
                "approval_status": getattr(e, "approval_status", ""),
                "created_at": str(getattr(e, "created_at", "")),
            }
        )
    return register[:30]


@router.get("")
async def board_decision_os() -> dict[str, Any]:
    """Governed decisions, passport rules, risk register."""
    try:
        decisions = _governed_decisions()
    except Exception:  # noqa: BLE001
        decisions = []

    try:
        risks = _risk_register()
        risk_note: str | None = None
    except Exception:  # noqa: BLE001
        risks, risk_note = [], "proof_ledger_unavailable"

    return governed(
        {
            "top_decisions": decisions,
            "decision_passport_rules": list(_PASSPORT_RULES),
            "risk_register": {"count": len(risks), "items": risks, "note": risk_note},
        }
    )
