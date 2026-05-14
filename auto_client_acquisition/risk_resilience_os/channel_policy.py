"""Channel risk — draft-first and forbidden automations."""

from __future__ import annotations

FORBIDDEN_CHANNEL_AUTOMATIONS: frozenset[str] = frozenset(
    {
        "cold_whatsapp",
        "linkedin_automation",
        "scraping_based_outreach",
        "unapproved_bulk_email",
    },
)


def channel_automation_forbidden(slug: str) -> bool:
    return slug.strip().lower() in FORBIDDEN_CHANNEL_AUTOMATIONS


def whatsapp_client_use_allowed(*, relationship_or_consent: bool, approved_external: bool) -> bool:
    """WhatsApp: only with relationship/consent basis; external sends need approval."""
    return relationship_or_consent and approved_external
