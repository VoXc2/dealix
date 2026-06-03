"""Approval policy — which customer-facing actions require explicit approval."""

from __future__ import annotations

from enum import StrEnum


class ApprovalRequirement(StrEnum):
    NONE = "none"
    INTERNAL_REVIEW = "internal_review"
    CLIENT_APPROVAL = "client_approval"
    BLOCKED = "blocked"


def approval_for_external_channel(*, channel: str, has_client_approval: bool) -> ApprovalRequirement:
    ch = channel.strip().lower()
    if ch in ("whatsapp", "linkedin_dm", "sms"):
        return ApprovalRequirement.CLIENT_APPROVAL if has_client_approval else ApprovalRequirement.BLOCKED
    if ch in ("email", "portal"):
        return ApprovalRequirement.INTERNAL_REVIEW
    return ApprovalRequirement.NONE


__all__ = ["ApprovalRequirement", "approval_for_external_channel"]
