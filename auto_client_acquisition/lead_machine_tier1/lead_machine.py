from __future__ import annotations

from .compliance_gate import check_compliance
from .dedupe_engine import dedupe_lead
from .deliverability_gate import deliverability_risk_score
from .enrichment_waterfall import run_enrichment_waterfall
from .icp_scoring import score_lead
from .schemas import LeadMachineRunRequest, LeadMachineRunResponse
from .signal_engine import detect_signals
from .source_registry import get_source_definition
from .warm_route import choose_warm_route


class Tier1LeadMachine:
    def run(self, request: LeadMachineRunRequest) -> LeadMachineRunResponse:
        source = get_source_definition(request.provenance.source_name)
        enrichment = run_enrichment_waterfall(request.lead)
        dedupe = dedupe_lead(request.lead, request.existing_records)
        signals = detect_signals(request.lead)
        compliance = check_compliance(request.lead, request.provenance)
        deliverability_risk = deliverability_risk_score(request.lead)
        score = score_lead(request.lead, signals, compliance, deliverability_risk)
        warm_route = choose_warm_route(request.lead, compliance, inbound_whatsapp=request.inbound_whatsapp, consented_whatsapp=request.consented_whatsapp)
        return LeadMachineRunResponse(
            source=source,
            enrichment=enrichment,
            dedupe=dedupe,
            signals=signals,
            score=score,
            compliance=compliance,
            warm_route=warm_route,
        )