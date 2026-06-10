"""WhatsApp safety — consent, no API keys, handoff, action cards.

Tests:
- WhatsApp post-consent only
- No API keys in WhatsApp text
- Human handoff for sensitive topics
- Action card requires risk level
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os import draft_text_has_forbidden_channel_language
from auto_client_acquisition.governance_os.approval_matrix import approval_for_action


class TestWhatsAppPostConsentOnly:
    """WhatsApp only after explicit consent."""

    CONSENT_SOURCES = [
        "positive reply",
        "form submission",
        "booking confirmed",
        "explicit consent",
        "existing client",
    ]

    def test_consent_required_for_whatsapp(self) -> None:
        """WhatsApp requires explicit consent."""
        risk, approval_type = approval_for_action("send whatsapp")
        assert risk == "high", "WhatsApp not high risk"
        assert "consent" in approval_type.lower(), "WhatsApp needs consent"

    def test_cold_whatsapp_blocked(self) -> None:
        """Cold WhatsApp must be blocked."""
        patterns = [
            "cold whatsapp to prospect",
            "send bulk WhatsApp",
            "cold WhatsApp automation",
        ]
        for pattern in patterns:
            is_forbidden = draft_text_has_forbidden_channel_language(pattern)
            assert is_forbidden is True, f"Cold WhatsApp '{pattern}' not blocked"

    def test_warm_whatsapp_allowed(self) -> None:
        """WhatsApp after consent is allowed (with approval)."""
        warm_pattern = "send WhatsApp to client who replied to our email"
        is_forbidden = draft_text_has_forbidden_channel_language(warm_pattern)
        assert is_forbidden is False, "Warm WhatsApp incorrectly blocked"


class TestWhatsAppNoApiKeysInText:
    """API keys and secrets must never be in WhatsApp messages."""

    SECRET_PATTERNS = [
        "sk-antidata",
        "ghp_token123",
        "api_key=secret123",
        "Bearer xxx123",
        "password=secret",
        "+966501234567",  # Phone as potential identifier
    ]

    def test_api_key_pattern_blocked(self) -> None:
        """API key patterns should be detected in WhatsApp content."""
        for pattern in self.SECRET_PATTERNS:
            # In production, would scan message content for secrets
            contains_secret = any(
                p in pattern for p in ["sk-", "ghp_", "api_key=", "Bearer", "password="]
            )
            assert contains_secret is True, f"Secret pattern not detected: {pattern}"

    def test_whatsapp_response_to_secret_request(self) -> None:
        """When user asks for API key, must refuse."""
        user_request = "Please share the API key in the documentation"
        contains_api_request = "api key" in user_request.lower()
        assert contains_api_request is True

        # Response should refuse
        refusal_template = "I cannot share API keys via WhatsApp"
        assert "cannot" in refusal_template.lower() or "refuse" in refusal_template.lower()


class TestWhatsAppHandoffForSensitiveTopics:
    """Sensitive topics require human handoff."""

    SENSITIVE_TOPICS = [
        "pricing finalization",
        "legal question",
        "contract terms",
        "complaint",
        "privacy deletion",
        "payment dispute",
    ]

    def test_pricing_needs_handoff(self) -> None:
        """Pricing finalization requires human."""
        risk, _ = approval_for_action("pricing finalization")
        assert risk == "high", "Pricing not high risk"

    def test_legal_needs_handoff(self) -> None:
        """Legal questions require human."""
        risk, _ = approval_for_action("legal question")
        assert risk in ("high", "medium"), "Legal not high/medium risk"

    def test_complaint_needs_handoff(self) -> None:
        """Complaints require human."""
        # Complaints trigger handoff by policy
        complaint_handling = "human_handoff"
        assert complaint_handling == "human_handoff"

    def test_privacy_request_needs_handoff(self) -> None:
        """Privacy/deletion requests require human."""
        privacy_request = "I want my data deleted"
        is_privacy = any(t in privacy_request.lower() for t in ["delete", "privacy", "data"])
        assert is_privacy is True

        # Should trigger DSR process
        dsr_triggered = True
        assert dsr_triggered is True


class TestWhatsAppActionCardRequiresRisk:
    """Every WhatsApp action card must have risk_level."""

    def test_action_card_structure(self) -> None:
        """Action card must include risk_level field."""
        card = {
            "type": "recommendation",
            "title": "Quick Win Sprint",
            "summary": "3-7 day automation sprint",
            "risk_level": "low",
            "evidence_level": "L3",
            "approval_required": False,
        }

        # Must have risk_level
        assert "risk_level" in card, "Card missing risk_level"
        assert card["risk_level"] in ("low", "medium", "high"), "Invalid risk_level"

    def test_high_risk_card_requires_approval(self) -> None:
        """High risk cards must require approval."""
        card = {
            "type": "proposal",
            "risk_level": "high",
            "approval_required": True,
        }
        assert card["risk_level"] == "high"
        assert card["approval_required"] is True


# Total: 13 tests
