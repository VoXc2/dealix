"""Escalation helper — surfaces approval-required actions, never auto-executes."""
from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.customer_inbox_v10.schemas import Conversation


def escalate(conv: Conversation, reason: str) -> dict:
    """Return an approval_required escalation envelope."""
    return {
        "conversation_id": conv.id,
        "customer_handle": conv.customer_handle,
        "reason": reason,
        "action_mode": "approval_required",
        "assigned_owner": conv.assigned_owner or "founder",
        "escalated_at": datetime.now(UTC).isoformat(),
    }
