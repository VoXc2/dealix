from __future__ import annotations

from scripts.revenue.batch_outreach_queue import is_outbound_authorized


def test_verified_public_research_never_grants_outbound_authority() -> None:
    row = {"company": "Public Exhibitor", "email": "info@example.com", "verification_status": "verified_public", "status": "research_only"}
    assert is_outbound_authorized(row) is False


def test_public_contact_without_consent_proof_is_blocked() -> None:
    row = {"company": "Public Company", "email": "info@example.com", "owner_decision": "approved_to_send", "consent_status": "opted_in", "human_approved": "true", "live_gate": "true"}
    assert is_outbound_authorized(row) is False


def test_legacy_queue_requires_all_target_level_gates() -> None:
    row = {"company": "Opted In Company", "email": "buyer@example.com", "owner_decision": "approved_to_send", "consent_status": "opted_in", "consent_proof_url": "https://crm.example/consent/123", "human_approved": "true", "live_gate": "true"}
    assert is_outbound_authorized(row) is True
