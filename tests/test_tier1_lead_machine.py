from __future__ import annotations

from datetime import datetime

from auto_client_acquisition.lead_machine_tier1.lead_machine import Tier1LeadMachine
from auto_client_acquisition.lead_machine_tier1.schemas import LeadCompany, LeadMachineRunRequest, ProvenanceRecord


def _request(**metadata):
    return LeadMachineRunRequest(
        lead=LeadCompany(company_name="Dealix Clinic", domain="clinic.sa", city="Jeddah", sector="clinics", metadata=metadata),
        provenance=ProvenanceRecord(source_name="manual_warm_network", source_type="manual", collected_at=datetime.utcnow(), allowed_use="warm_manual_only", consent_state="granted", confidence=0.9, refresh_needed=False, risk_level="low"),
    )


def test_tier1_lead_machine_runs():
    result = Tier1LeadMachine().run(_request(crm_installed=True, payment_provider=True, founder_intro=True, inbound=True))
    assert result.source.source_name == "manual_warm_network"
    assert result.compliance.allowed is True
    assert result.warm_route.allowed is True
    assert result.score.final_priority.value in {"P0_NOW", "P1_THIS_WEEK", "P2_NURTURE", "P3_LOW_PRIORITY"}