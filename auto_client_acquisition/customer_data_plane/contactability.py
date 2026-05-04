"""Contactability gate over the consent registry.

Compatible with the existing ``compliance_os.assess_contactability``
but more granular per channel (consent state per channel). The
existing module stays the safety floor — this gate only adds context.
"""
from __future__ import annotations

from auto_client_acquisition.customer_data_plane.consent_registry import (
    ConsentRegistry,
    get_default_registry,
)
from auto_client_acquisition.customer_data_plane.schemas import (
    ChannelKind,
    ConsentStatus,
    ContactabilityResult,
    ContactabilityVerdict,
)


_BASE_NOTES = [
    "no_cold_outreach",
    "no_scraping",
    "no_linkedin_automation",
    "approval_required_for_external_send",
]


def _kind_requires_active_consent(channel: ChannelKind) -> bool:
    """Channels that REQUIRE active consent to be SAFE."""
    return channel in {
        ChannelKind.WHATSAPP_TEMPLATE,
        ChannelKind.EMAIL_DRAFT,
        ChannelKind.PHONE_CALL_REQUESTED,
    }


def _kind_safe_inbound_only(channel: ChannelKind) -> bool:
    """Channels that are SAFE only when the customer initiated contact."""
    return channel in {
        ChannelKind.WHATSAPP_INBOUND,
        ChannelKind.EMAIL_INBOUND,
    }


def contactability_check(
    contact_id: str,
    channel: ChannelKind | str,
    registry: ConsentRegistry | None = None,
) -> ContactabilityResult:
    """Decide whether reaching the contact on a channel is safe.

    Decision tree:
      1. ``BLOCKED`` channel → BLOCKED.
      2. Inbound-only channel → SAFE (always — customer initiated).
      3. Channel requires active consent → check registry:
         - GRANTED + active → SAFE
         - WITHDRAWN → BLOCKED
         - UNKNOWN → BLOCKED (default deny)
      4. Other channels (LINKEDIN_MANUAL, PARTNER_INTRO) →
         NEEDS_REVIEW (founder reviews each manually).
    """
    ch = channel if isinstance(channel, ChannelKind) else ChannelKind(channel)
    reg = registry or get_default_registry()

    if ch == ChannelKind.BLOCKED:
        return ContactabilityResult(
            contact_id=str(contact_id),
            channel=ch,
            verdict=ContactabilityVerdict.BLOCKED,
            reason="channel marked as BLOCKED",
            consent_known=False,
            safety_notes=list(_BASE_NOTES),
        )

    if _kind_safe_inbound_only(ch):
        return ContactabilityResult(
            contact_id=str(contact_id),
            channel=ch,
            verdict=ContactabilityVerdict.SAFE,
            reason="inbound channel — customer-initiated",
            consent_known=False,
            safety_notes=list(_BASE_NOTES),
        )

    status, record = reg.status_for(contact_id, ch)
    consent_known = status != ConsentStatus.UNKNOWN
    consent_record_id = record.id if record else None

    if _kind_requires_active_consent(ch):
        if status == ConsentStatus.GRANTED:
            return ContactabilityResult(
                contact_id=str(contact_id),
                channel=ch,
                verdict=ContactabilityVerdict.SAFE,
                reason=f"active consent for {ch.value} via {record.consent_source if record else 'unknown'}",
                consent_known=True,
                consent_record_id=consent_record_id,
                safety_notes=list(_BASE_NOTES),
            )
        if status == ConsentStatus.WITHDRAWN:
            return ContactabilityResult(
                contact_id=str(contact_id),
                channel=ch,
                verdict=ContactabilityVerdict.BLOCKED,
                reason="contact withdrew consent on this channel",
                consent_known=True,
                consent_record_id=consent_record_id,
                safety_notes=list(_BASE_NOTES),
            )
        # UNKNOWN — default deny
        return ContactabilityResult(
            contact_id=str(contact_id),
            channel=ch,
            verdict=ContactabilityVerdict.BLOCKED,
            reason=(
                f"consent unknown for {ch.value} — default deny (PDPL-safe). "
                "Capture consent through an inbound reply or website form first."
            ),
            consent_known=False,
            safety_notes=list(_BASE_NOTES),
        )

    # Manual / partner-intro channels — founder reviews
    return ContactabilityResult(
        contact_id=str(contact_id),
        channel=ch,
        verdict=ContactabilityVerdict.NEEDS_REVIEW,
        reason=(
            f"channel {ch.value} requires founder manual review per outreach "
            "(no auto-approval, no automation)"
        ),
        consent_known=consent_known,
        consent_record_id=consent_record_id,
        safety_notes=list(_BASE_NOTES),
    )
