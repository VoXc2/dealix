"""Scoring bonuses for relationship, notes, recency, and size proxy."""

from __future__ import annotations

from auto_client_acquisition.revenue_os.scoring import score_account_row


def test_engagement_signals_raise_score_without_breaking_icp_cap() -> None:
    base_row = {
        "company_name": "Acme",
        "sector": "logistics",
        "city": "Riyadh",
        "source": "crm_export",
    }
    enriched = {
        **base_row,
        "relationship_status": "contracted",
        "manual_priority": True,
        "notes": "x" * 40,
        "last_contact_days": 10,
        "employee_count": 250,
    }
    full = score_account_row(
        base_row,
        icp_sectors=frozenset({"logistics"}),
        icp_cities=frozenset({"Riyadh"}),
    )
    with_signals = score_account_row(
        enriched,
        icp_sectors=frozenset({"logistics"}),
        icp_cities=frozenset({"Riyadh"}),
    )
    assert full["score"] == 100
    assert with_signals["score"] == 100
    assert "relationship_trust_signal" in with_signals["reasons"]
