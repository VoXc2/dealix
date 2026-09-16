"""Tests for CommunicationNegotiationEngine — authority hardening, fail-closed, canonical external execution gate."""

from __future__ import annotations

import pytest

from dealix.commercial.communication_negotiation import (
    UNKNOWN,
    CommunicationNegotiationEngine,
    CommunicationTask,
    NegotiationState,
    SenderIdentityEvidence,
    SiteReadinessEvidence,
)


class TestSenderIdentityEvidence:
    """Sender identity must be evidence-backed — no placeholder defaults."""

    def test_valid_evidence_accepted(self):
        evidence = SenderIdentityEvidence(
            email="verified@company.com",
            phone="+966501234567",
            evidence_ref="identity_verification_2024_001",
            verified_at="2024-01-15T10:30:00+00:00",
        )
        assert evidence.email == "verified@company.com"
        assert evidence.phone == "+966501234567"

    def test_placeholder_email_rejected(self):
        with pytest.raises(ValueError, match="placeholder|founder@dealix|UNKNOWN"):
            SenderIdentityEvidence(
                email="founder@dealix.me",
                phone="+966501234567",
                evidence_ref="identity_verification_2024_001",
                verified_at="2024-01-15T10:30:00+00:00",
            )

    def test_placeholder_phone_rejected(self):
        with pytest.raises(ValueError, match="placeholder|XXXX|UNKNOWN"):
            SenderIdentityEvidence(
                email="verified@company.com",
                phone="+9665XXXXXXXX",
                evidence_ref="identity_verification_2024_001",
                verified_at="2024-01-15T10:30:00+00:00",
            )

    def test_unknown_email_rejected(self):
        with pytest.raises(ValueError, match="placeholder|UNKNOWN"):
            SenderIdentityEvidence(
                email=UNKNOWN,
                phone="+966501234567",
                evidence_ref="identity_verification_2024_001",
                verified_at="2024-01-15T10:30:00+00:00",
            )

    def test_unknown_phone_rejected(self):
        with pytest.raises(ValueError, match="placeholder|UNKNOWN"):
            SenderIdentityEvidence(
                email="verified@company.com",
                phone=UNKNOWN,
                evidence_ref="identity_verification_2024_001",
                verified_at="2024-01-15T10:30:00+00:00",
            )

    def test_empty_email_rejected(self):
        with pytest.raises(ValueError):
            SenderIdentityEvidence(
                email="",
                phone="+966501234567",
                evidence_ref="identity_verification_2024_001",
                verified_at="2024-01-15T10:30:00+00:00",
            )

    def test_empty_phone_rejected(self):
        with pytest.raises(ValueError):
            SenderIdentityEvidence(
                email="verified@company.com",
                phone="",
                evidence_ref="identity_verification_2024_001",
                verified_at="2024-01-15T10:30:00+00:00",
            )

    def test_missing_evidence_ref_rejected(self):
        with pytest.raises(ValueError):
            SenderIdentityEvidence(
                email="verified@company.com",
                phone="+966501234567",
                evidence_ref="",
                verified_at="2024-01-15T10:30:00+00:00",
            )

    def test_frozen_model(self):
        evidence = SenderIdentityEvidence(
            email="verified@company.com",
            phone="+966501234567",
            evidence_ref="identity_verification_2024_001",
            verified_at="2024-01-15T10:30:00+00:00",
        )
        with pytest.raises(Exception):
            evidence.email = "other@company.com"


class TestSiteReadinessEvidence:
    """Site/provider/social readiness must fail closed unless evidenced."""

    def test_valid_readiness_accepted(self):
        readiness = SiteReadinessEvidence(
            site_ready=True,
            provider_ready=True,
            social_ready=True,
            evidence_ref="readiness_check_2024_001",
            checked_at="2024-01-15T10:30:00+00:00",
        )
        assert readiness.site_ready is True
        assert readiness.provider_ready is True
        assert readiness.social_ready is True

    def test_defaults_false_fail_closed(self):
        readiness = SiteReadinessEvidence(
            evidence_ref="readiness_check_2024_001",
            checked_at="2024-01-15T10:30:00+00:00",
        )
        assert readiness.site_ready is False
        assert readiness.provider_ready is False
        assert readiness.social_ready is False

    def test_explicit_false_values(self):
        readiness = SiteReadinessEvidence(
            site_ready=False,
            provider_ready=False,
            social_ready=False,
            evidence_ref="readiness_check_2024_001",
            checked_at="2024-01-15T10:30:00+00:00",
        )
        assert readiness.site_ready is False
        assert readiness.provider_ready is False
        assert readiness.social_ready is False

    def test_missing_evidence_ref_rejected(self):
        with pytest.raises(ValueError):
            SiteReadinessEvidence(
                site_ready=True,
                provider_ready=True,
                social_ready=True,
                evidence_ref="",
                checked_at="2024-01-15T10:30:00+00:00",
            )

    def test_frozen_model(self):
        readiness = SiteReadinessEvidence(
            site_ready=True,
            provider_ready=True,
            social_ready=True,
            evidence_ref="readiness_check_2024_001",
            checked_at="2024-01-15T10:30:00+00:00",
        )
        with pytest.raises(Exception):
            readiness.site_ready = False


class TestCommunicationTask:
    """Communication task — draft-only, no sender authority, no queue/scheduler."""

    def test_create_task_draft_only(self):
        engine = CommunicationNegotiationEngine()
        task = engine.create_task(
            channel="email",
            recipient="client@company.com",
            subject="Test Subject",
            body_ar="محتوى عربي",
            body_en="English content",
            sender_identity_ref="identity_verification_2024_001",
            site_readiness_ref="readiness_check_2024_001",
        )
        assert task.negotiation_state == NegotiationState.DRAFT
        assert task.social_automated is False
        assert task.approval_required is True
        assert task.sent is False
        assert task.task_id.startswith("comm_")

    def test_create_task_requires_sender_identity_ref(self):
        engine = CommunicationNegotiationEngine()
        with pytest.raises(ValueError):
            engine.create_task(
                channel="email",
                recipient="client@company.com",
                subject="Test Subject",
                body_ar="محتوى عربي",
                body_en="English content",
                sender_identity_ref="",
                site_readiness_ref="readiness_check_2024_001",
            )

    def test_create_task_requires_site_readiness_ref(self):
        engine = CommunicationNegotiationEngine()
        with pytest.raises(ValueError):
            engine.create_task(
                channel="email",
                recipient="client@company.com",
                subject="Test Subject",
                body_ar="محتوى عربي",
                body_en="English content",
                sender_identity_ref="identity_verification_2024_001",
                site_readiness_ref="",
            )

    def test_task_frozen_model(self):
        engine = CommunicationNegotiationEngine()
        task = engine.create_task(
            channel="email",
            recipient="client@company.com",
            subject="Test Subject",
            body_ar="محتوى عربي",
            body_en="English content",
            sender_identity_ref="identity_verification_2024_001",
            site_readiness_ref="readiness_check_2024_001",
        )
        with pytest.raises(Exception):
            task.negotiation_state = NegotiationState.SENT

    def test_task_cannot_be_constructed_with_sent_true(self):
        with pytest.raises(ValueError, match="sent.*must be False|draft.*only"):
            CommunicationTask(
                task_id="comm_test",
                channel="email",
                recipient="client@company.com",
                subject="Test",
                body_ar="AR",
                body_en="EN",
                sender_identity_ref="ref1",
                site_readiness_ref="ref2",
                negotiation_state=NegotiationState.DRAFT,
                social_automated=False,
                sent=True,
            )

    def test_task_cannot_be_constructed_with_social_automated_true(self):
        with pytest.raises(ValueError, match="social_automated.*must be False|draft.*only"):
            CommunicationTask(
                task_id="comm_test",
                channel="email",
                recipient="client@company.com",
                subject="Test",
                body_ar="AR",
                body_en="EN",
                sender_identity_ref="ref1",
                site_readiness_ref="ref2",
                negotiation_state=NegotiationState.DRAFT,
                social_automated=True,
                sent=False,
            )

    def test_task_cannot_be_constructed_with_non_draft_state(self):
        with pytest.raises(ValueError, match="negotiation_state.*must be DRAFT|draft.*only"):
            CommunicationTask(
                task_id="comm_test",
                channel="email",
                recipient="client@company.com",
                subject="Test",
                body_ar="AR",
                body_en="EN",
                sender_identity_ref="ref1",
                site_readiness_ref="ref2",
                negotiation_state=NegotiationState.APPROVED,
                social_automated=False,
                sent=False,
            )


class TestCommunicationNegotiationEngine:
    """Authority-hardened communication engine."""

    def test_prepare_external_action_packet_delegates_to_canonical_gate(self):
        engine = CommunicationNegotiationEngine()
        packet = engine.prepare_external_action_packet(
            task=CommunicationTask(
                task_id="comm_test123",
                channel="email",
                recipient="client@company.com",
                subject="Test",
                body_ar="AR",
                body_en="EN",
                sender_identity_ref="identity_verification_2024_001",
                site_readiness_ref="readiness_check_2024_001",
            ),
            action_class="EMAIL_SEND",
            purpose_class="TRANSACTIONAL",
            artifact_ref="artifact_001",
            content_sha256="a" * 64,
            identity_or_relationship_ref="relationship_001",
            consent_or_channel_eligibility_ref="consent_001",
            suppression_check_ref="suppression_001",
            suppression_clear=True,
            claim_evidence_refs=["claim_001"],
            sender_identity_ref="identity_verification_2024_001",
            opt_out_mechanism_ref="optout_001",
            risk_class="LOW",
            exact_scope="send email to client@company.com",
            expires_at="2025-01-15T10:30:00+00:00",
            provider="smtp",
            idempotency_key="idem_001",
        )
        assert packet["action_id"] == "comm_test123"
        assert packet["action_class"] == "EMAIL_SEND"
        assert packet["schema_version"] == "dealix.external-action-packet.v2"
        assert "packet_integrity_sha256" in packet
        assert "action_hash" in packet
        assert len(packet["action_hash"]) == 16

    def test_automate_social_reports_draft_preparation_only(self):
        engine = CommunicationNegotiationEngine()
        result = engine.automate_social(site_readiness_ref="readiness_check_2024_001")

        assert result["automated"] is False
        assert result["draft_only"] is True
        assert result["preparation_capable"] is True
        assert result["site_readiness_ref"] == "readiness_check_2024_001"
        assert result["site_ready"] is False
        assert "requires" in result
        assert any("Evidenced SiteReadinessEvidence with social_ready=True" in r for r in result["requires"])
        assert any("Canonical ExternalActionPacket for COMPANY_SOCIAL_PUBLISH" in r for r in result["requires"])
        assert any("CanonicalAuthorityResolver" in r for r in result["requires"])
        assert any("evaluate_resolved_external_action verdict=READY_FOR_PROVIDER_EXECUTION" in r for r in result["requires"])

    def test_automate_social_provider_readiness_unknown_by_default(self):
        engine = CommunicationNegotiationEngine()
        result = engine.automate_social()

        for platform in ["linkedin", "x", "instagram", "tiktok", "youtube", "facebook"]:
            assert result["provider_readiness"][platform] == "unknown"

    def test_automate_social_channels_zero(self):
        engine = CommunicationNegotiationEngine()
        result = engine.automate_social()
        assert result["channels"] == 0

    def test_to_dict_returns_safe_summary(self):
        engine = CommunicationNegotiationEngine()
        result = engine.to_dict()

        assert result["social_platforms"] == 6
        assert result["site_ready"] is False
        assert result["requires_evidence"] is True

    def test_no_approve_and_send_method(self):
        """Ensure approve_and_send is not present — delegates to canonical external_execution_gate."""
        engine = CommunicationNegotiationEngine()
        assert not hasattr(engine, "approve_and_send")

    def test_no_internal_queue_or_scheduler(self):
        """Ensure no internal queue/scheduler attributes."""
        engine = CommunicationNegotiationEngine()
        # No queue, scheduler, sender, or similar attributes
        attrs = [attr for attr in dir(engine) if not attr.startswith("_")]
        assert "queue" not in attrs
        assert "scheduler" not in attrs
        assert "sender" not in attrs
        assert "send" not in attrs  # no direct send method


class TestIntegrationWithExternalExecutionGate:
    """Integration tests ensuring canonical external execution gate contracts are reused."""

    def test_packet_includes_all_required_fields(self):
        engine = CommunicationNegotiationEngine()
        task = engine.create_task(
            channel="whatsapp",
            recipient="+966501234567",
            subject="Test",
            body_ar="اختبار",
            body_en="Test",
            sender_identity_ref="identity_verification_2024_001",
            site_readiness_ref="readiness_check_2024_001",
        )
        packet = engine.prepare_external_action_packet(
            task=task,
            action_class="WHATSAPP_SEND",
            purpose_class="INBOUND_REPLY",
            artifact_ref="artifact_001",
            content_sha256="b" * 64,
            identity_or_relationship_ref="relationship_001",
            consent_or_channel_eligibility_ref="consent_001",
            suppression_check_ref="suppression_001",
            suppression_clear=True,
            claim_evidence_refs=["claim_001"],
            sender_identity_ref="identity_verification_2024_001",
            opt_out_mechanism_ref="optout_001",
            risk_class="MEDIUM",
            exact_scope="reply to inbound whatsapp",
            expires_at="2025-01-15T10:30:00+00:00",
            provider="whatsapp_business",
            idempotency_key="idem_002",
        )

        # Verify all required fields from ExternalActionPacket schema
        required_fields = [
            "schema_version", "action_id", "action_class", "purpose_class",
            "destination", "channel", "environment", "artifact_ref",
            "content_sha256", "identity_or_relationship_ref",
            "consent_or_channel_eligibility_ref", "suppression_check_ref",
            "suppression_clear", "claim_evidence_refs", "sender_identity_ref",
            "opt_out_mechanism_ref", "risk_class", "exact_scope",
            "expires_at", "provider", "idempotency_key",
            "packet_integrity_sha256", "action_hash"
        ]
        for field in required_fields:
            assert field in packet, f"Missing required field: {field}"

        assert packet["schema_version"] == "dealix.external-action-packet.v2"
        assert packet["action_class"] == "WHATSAPP_SEND"
        assert packet["purpose_class"] == "INBOUND_REPLY"
        assert packet["environment"] == "production"
        assert packet["channel"] == "whatsapp"
        assert packet["destination"] == "+966501234567"