from __future__ import annotations

from .provenance import validate_provenance
from .schemas import ComplianceDecision, ConsentState, LeadCompany, ProvenanceRecord
from .suppression import suppression_reasons


def check_compliance(lead: LeadCompany, provenance: ProvenanceRecord) -> ComplianceDecision:
    reasons = validate_provenance(provenance) + suppression_reasons(lead)
    if provenance.consent_state == ConsentState.revoked:
        reasons.append("consent_revoked")
    if provenance.source_name == "blocked_scraping_source":
        reasons.append("scraping_blocked")
    allowed = len(reasons) == 0 or reasons == ["refresh_needed"]
    status = "ok" if allowed else "blocked"
    return ComplianceDecision(allowed=allowed, status=status, reasons=reasons)