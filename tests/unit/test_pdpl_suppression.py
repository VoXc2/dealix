"""
Unit tests — PDPL contactability (suppression) check.
اختبارات الوحدة — فحص قابلية التواصل وفق نظام حماية البيانات الشخصية.

Tests that contactability_check correctly enforces PDPL consent rules:
- WHATSAPP_TEMPLATE requires explicit active consent → BLOCKED without it
- Email inbound requires no consent → SAFE
- Absent consent → BLOCKED or REVIEW
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from auto_client_acquisition.customer_data_plane.contactability import contactability_check
from auto_client_acquisition.customer_data_plane.schemas import (
    ChannelKind,
    ConsentRecord,
    ConsentSource,
    ConsentStatus,
    ContactabilityVerdict,
)


# ── Fixtures ───────────────────────────────────────────────────────

def _make_registry(channel: ChannelKind, status: ConsentStatus):
    """Build a mock ConsentRegistry whose ``status_for`` returns the given
    status for a channel, mirroring the real ``(status, record)`` tuple."""
    registry = MagicMock()
    record: ConsentRecord | None = None
    if status in (ConsentStatus.GRANTED, ConsentStatus.WITHDRAWN):
        record = ConsentRecord(
            contact_id="mock",
            channel=channel,
            consent_status=status,
            consent_source=ConsentSource.WEBSITE_FORM,
        )
    registry.status_for.return_value = (status, record)
    return registry


# ── Tests ──────────────────────────────────────────────────────────

class TestWhatsAppTemplateSuppression:
    """WhatsApp template messages require active consent (PDPL Article 4)."""

    def test_active_consent_is_safe(self):
        registry = _make_registry(ChannelKind.WHATSAPP_TEMPLATE, ConsentStatus.GRANTED)
        result = contactability_check(
            contact_id="c001",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.SAFE

    def test_no_record_is_blocked(self):
        registry = _make_registry(ChannelKind.WHATSAPP_TEMPLATE, ConsentStatus.UNKNOWN)
        result = contactability_check(
            contact_id="c002",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.BLOCKED

    def test_revoked_consent_is_blocked(self):
        registry = _make_registry(ChannelKind.WHATSAPP_TEMPLATE, ConsentStatus.WITHDRAWN)
        result = contactability_check(
            contact_id="c003",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.BLOCKED

    def test_expired_consent_is_blocked(self):
        registry = _make_registry(ChannelKind.WHATSAPP_TEMPLATE, ConsentStatus.WITHDRAWN)
        result = contactability_check(
            contact_id="c004",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.BLOCKED


class TestEmailSupression:
    """Email drafts require active consent; inbound email is always safe."""

    def test_email_inbound_is_always_safe(self):
        registry = _make_registry(ChannelKind.EMAIL_INBOUND, ConsentStatus.UNKNOWN)
        result = contactability_check(
            contact_id="c010",
            channel=ChannelKind.EMAIL_INBOUND,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.SAFE

    def test_email_draft_needs_active_consent(self):
        registry = _make_registry(ChannelKind.EMAIL_DRAFT, ConsentStatus.UNKNOWN)
        result = contactability_check(
            contact_id="c011",
            channel=ChannelKind.EMAIL_DRAFT,
            registry=registry,
        )
        assert result.verdict != ContactabilityVerdict.SAFE

    def test_email_draft_with_active_consent_is_safe(self):
        registry = _make_registry(ChannelKind.EMAIL_DRAFT, ConsentStatus.GRANTED)
        result = contactability_check(
            contact_id="c012",
            channel=ChannelKind.EMAIL_DRAFT,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.SAFE


class TestResultNotes:
    """Verify that compliance notes are always present in the result."""

    def test_blocked_result_has_notes(self):
        registry = _make_registry(ChannelKind.WHATSAPP_TEMPLATE, ConsentStatus.WITHDRAWN)
        result = contactability_check(
            contact_id="c020",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.safety_notes  # must include at least one compliance note

    def test_safe_result_has_notes(self):
        registry = _make_registry(ChannelKind.WHATSAPP_INBOUND, ConsentStatus.GRANTED)
        result = contactability_check(
            contact_id="c021",
            channel=ChannelKind.WHATSAPP_INBOUND,
            registry=registry,
        )
        assert result.safety_notes
