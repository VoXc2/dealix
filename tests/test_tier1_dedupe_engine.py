from __future__ import annotations

from auto_client_acquisition.lead_machine_tier1.dedupe_engine import dedupe_lead
from auto_client_acquisition.lead_machine_tier1.schemas import LeadCompany


def test_dedupe_detects_domain_match():
    lead = LeadCompany(company_name="A", domain="example.sa")
    existing = [LeadCompany(company_name="B", domain="example.sa")]
    result = dedupe_lead(lead, existing)
    assert result.duplicate_of == "example.sa"
    assert "exact_domain" in result.matched_keys