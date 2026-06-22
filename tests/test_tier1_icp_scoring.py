from __future__ import annotations

from auto_client_acquisition.lead_machine_tier1.icp_scoring import score_lead
from auto_client_acquisition.lead_machine_tier1.schemas import ComplianceDecision, LeadCompany, SignalRecord


def test_icp_scoring_blocks_non_compliant():
    lead = LeadCompany(company_name="A", domain="example.sa", sector="SaaS")
    score = score_lead(
        lead,
        [SignalRecord(signal_name="funding", detected=True, weight=15)],
        ComplianceDecision(allowed=False, status="blocked", reasons=["blocked_source"]),
        20,
    )
    assert score.final_priority.value == "BLOCKED"