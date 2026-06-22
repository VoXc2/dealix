from __future__ import annotations

from auto_client_acquisition.lead_machine_tier1.enrichment_waterfall import run_enrichment_waterfall
from auto_client_acquisition.lead_machine_tier1.schemas import LeadCompany


def test_enrichment_waterfall_stops_after_threshold():
    lead = LeadCompany(company_name="Dealix", domain="dealix.me")
    results = run_enrichment_waterfall(lead, configured_providers={"internal_graph", "manual_research"})
    assert results[0].provider == "internal_graph"
    assert any(item.provider == "manual_research" for item in results)