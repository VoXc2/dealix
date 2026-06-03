"""Approval preview — shows what WOULD be sent if approved.

NEVER actually sends. Returns ApprovalPreview with would_send_live=False.
Reuses whatsapp_safe_send concepts as decision-only (no live API call).
"""
from __future__ import annotations

from auto_client_acquisition.whatsapp_decision_bot.policy import is_unsafe_command
from auto_client_acquisition.whatsapp_decision_bot.schemas import ApprovalPreview


def preview_action(
    *,
    action_kind: str,
    text_to_send: str,
    target_handle: str | None = None,
) -> ApprovalPreview:
    """Build an approval preview. ALWAYS would_send_live=False."""
    blocked: list[str] = []

    is_unsafe, matched = is_unsafe_command(text_to_send)
    if is_unsafe:
        blocked.extend(matched)

    # Even safe text — until live gate is on, we block live send
    blocked.append("live_send_gate_off_default")

    return ApprovalPreview(
        action_kind=action_kind,
        target_handle=target_handle,
        text_to_send_ar=text_to_send if _looks_arabic(text_to_send) else "",
        text_to_send_en=text_to_send if not _looks_arabic(text_to_send) else "",
        would_send_live=False,
        blocked_reasons=blocked,
        requires_human_approval=True,
    )


def _looks_arabic(s: str) -> bool:
    return any("؀" <= ch <= "ۿ" for ch in s)
