"""Contract: scraping is a blocked ingestion source in Revenue OS anti-waste."""

from __future__ import annotations

from auto_client_acquisition.revenue_os.anti_waste import validate_pipeline_step


def test_no_scraping_engine_blocked_as_lead_source() -> None:
    vios = validate_pipeline_step(
        has_decision_passport=True,
        lead_source="scraping",
        action_external=False,
        upsell_attempt=False,
        proof_event_count=1,
    )
    codes = {v.code for v in vios}
    assert "blocked_source" in codes
