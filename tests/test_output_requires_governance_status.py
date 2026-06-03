"""Contract: external pipeline action requires Decision Passport (governance signal)."""

from __future__ import annotations

from auto_client_acquisition.revenue_os.anti_waste import validate_pipeline_step


def test_output_requires_governance_status_external_without_passport() -> None:
    vios = validate_pipeline_step(
        has_decision_passport=False,
        lead_source="inbound",
        action_external=True,
        upsell_attempt=False,
        proof_event_count=1,
    )
    assert any(v.code == "no_passport_no_action" for v in vios)
