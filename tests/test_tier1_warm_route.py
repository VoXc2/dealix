from __future__ import annotations

from auto_client_acquisition.lead_machine_tier1.schemas import ComplianceDecision, LeadCompany
from auto_client_acquisition.lead_machine_tier1.warm_route import choose_warm_route


def test_warm_route_never_defaults_to_cold_whatsapp():
    lead = LeadCompany(company_name="A", phone="+966500000000")
    route = choose_warm_route(lead, ComplianceDecision(allowed=True, status="ok", reasons=[]))
    assert route.route.value != "whatsapp_inbound_only" or route.allowed is False or route.reason != "default"