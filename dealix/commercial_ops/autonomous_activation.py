"""Evidence-first daily commercial activation over the existing Dealix War Room.

This module does not send, publish, price, contract, charge, or promote a target
into a relationship. It creates an internal commercial command that the existing
commercial workload router can hand to the canonical Dealix agent council.
"""

from __future__ import annotations

import hashlib
from typing import Any

COMMAND_SCHEMA = "dealix.commercial_autopilot.command.v1"
CURRENT_PATH = (
    "Free Mini Diagnostic -> Qualified Discovery -> Customer-Specific Quote -> "
    "Customer-Specific Governed Delivery -> Verified Payment / Start Condition -> Delivery -> Proof"
)

TRUTH_STATEMENT = {
    "ranking_does_not_create_relationship": True,
    "ranking_does_not_create_revenue": True,
    "readiness_does_not_equal_execution_authority": True,
    "planner_never_sends_external": True,
    "planner_never_issues_execution_authority": True,
}

_PRIORITY = {"high": 60.0, "medium": 35.0, "low": 15.0}


def _non_empty(value: Any) -> str:
    return str(value or "").strip()


def _work_id(row: dict[str, Any], index: int) -> str:
    stable = "|".join(
        (
            _non_empty(row.get("company")),
            _non_empty(row.get("channel")),
            _non_empty(row.get("status")),
            str(index),
        )
    )
    return "activation-" + hashlib.sha256(stable.encode("utf-8")).hexdigest()[:16]


def _priority(row: dict[str, Any], index: int) -> float:
    base = _PRIORITY.get(_non_empty(row.get("priority")).lower(), 35.0)
    return max(1.0, base - min(index, 20) * 0.5)


def _interaction_evidence(row: dict[str, Any]) -> str:
    for key in (
        "interaction_evidence_ref",
        "real_interaction_evidence_ref",
        "explicit_inbound_evidence_ref",
    ):
        value = _non_empty(row.get(key))
        if value:
            return value
    return ""


def _item_for_target(row: dict[str, Any], index: int, *, source_ref: str) -> dict[str, Any]:
    status = _non_empty(row.get("status")) or "not_contacted"
    evidence_ref = _interaction_evidence(row)
    item = {
        "id": _work_id(row, index),
        "stage": "ATTENTION",
        "channel": "internal",
        "proposed_action": "research",
        "action_class": "INTERNAL_EXECUTABLE",
        "priority_score": _priority(row, index),
        "authority_reason": "WAR_ROOM_TARGET_IS_RESEARCH_ONLY_UNTIL_CANONICAL_INTERACTION_OR_INBOUND_EVIDENCE",
        "objective": "Build or refresh a source-backed account dossier and next evidence requirement.",
        "evidence_refs": [source_ref],
        "signal": {"signal_type": "account_research"},
        "commercial_path": CURRENT_PATH,
        "external_effect_allowed": False,
    }

    if status in {"message_drafted", "approved_to_send", "sent_manual"}:
        item["proposed_action"] = "internal_review"
        item["objective"] = (
            "Review the draft/history, verify channel eligibility and collect missing relationship/consent evidence; "
            "do not treat the legacy status label as execution authority."
        )
        item["authority_reason"] = "LEGACY_OR_WORKFLOW_STATUS_IS_NOT_EXTERNAL_EXECUTION_AUTHORITY"
    elif status in {"replied", "meeting_booked"}:
        if evidence_ref:
            item["stage"] = "INTERACTION"
            item["proposed_action"] = "qualify"
            item["objective"] = "Qualify the evidenced interaction and identify the next evidence required for a qualified problem."
            item["evidence_refs"] = [source_ref, evidence_ref]
            item["authority_reason"] = "INTERACTION_EVIDENCE_PRESENT_INTERNAL_QUALIFICATION_ONLY"
        else:
            item["proposed_action"] = "internal_review"
            item["objective"] = "Capture canonical interaction evidence before any relationship or qualification promotion."
            item["authority_reason"] = "STATUS_WITHOUT_INTERACTION_EVIDENCE_CANNOT_PROMOTE_COMMERCIAL_TRUTH"

    return item


def build_activation_command(war_room: dict[str, Any], *, source_ref: str = "data/war_room_today.json") -> dict[str, Any]:
    targets = war_room.get("targets") if isinstance(war_room.get("targets"), dict) else {}
    raw_items = targets.get("items") if isinstance(targets.get("items"), list) else []
    items = [
        _item_for_target(row, index, source_ref=f"{source_ref}#target-{index + 1}")
        for index, row in enumerate(raw_items)
        if isinstance(row, dict)
    ]
    items.sort(key=lambda row: (-float(row["priority_score"]), str(row["id"])))
    top = items[:5]

    return {
        "schema": COMMAND_SCHEMA,
        "source_ref": source_ref,
        "truth_statement": dict(TRUTH_STATEMENT),
        "commercial_path": CURRENT_PATH,
        "primary_focus": top[0] if top else None,
        "founder_top_5": top,
        "approval_queue": [],
        "ready_policy_governed_queue": [],
        "execution_authorized_queue": [],
        "manual_native_queue": [],
        "blocked_queue": [],
        "activation_policy": {
            "new_scheduler": False,
            "new_permanent_agent": False,
            "external_send": False,
            "public_publish": False,
            "paid_spend": False,
            "named_price_or_discount": False,
            "payment_or_refund": False,
            "legal_or_contract_commitment": False,
            "research_target_is_relationship": False,
            "legacy_approved_to_send_is_execution_authority": False,
            "exact_action_fingerprint_required_before_any_external_handoff": True
        }
    }
