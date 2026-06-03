"""Trust-default channel policies — compliance operations stack (draft-first)."""

from __future__ import annotations

COMPLIANCE_CHANNEL_POLICIES: tuple[str, ...] = (
    "draft_only_by_default",
    "external_action_approval_required",
    "whatsapp_relationship_or_consent_required",
    "no_cold_whatsapp_automation",
    "no_linkedin_automation",
    "unknown_source_no_outreach",
)


def compliance_channel_policy_valid(slug: str) -> bool:
    return slug in COMPLIANCE_CHANNEL_POLICIES


def external_channel_action_requires_approval(_channel: str) -> bool:
    """Trust ops default: any external channel send goes through approval workflow."""
    return True
