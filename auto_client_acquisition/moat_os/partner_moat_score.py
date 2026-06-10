"""Partner layer contribution to moat (certification + QA + governance adherence)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PartnerMoatSignals:
    certified_method: bool = False
    qa_standard_accepted: bool = False
    governance_rules_accepted: bool = False
    proof_pack_required: bool = False
    co_sell_playbook: bool = False
    partner_dashboard: bool = False
    audit_rights_accepted: bool = False
    zero_compliance_incidents: bool = False


def partner_moat_score(s: PartnerMoatSignals) -> int:
    """0–100 coarse score from boolean gates."""
    weights = (
        (s.certified_method, 15),
        (s.qa_standard_accepted, 15),
        (s.governance_rules_accepted, 15),
        (s.proof_pack_required, 15),
        (s.co_sell_playbook, 10),
        (s.partner_dashboard, 5),
        (s.audit_rights_accepted, 15),
        (s.zero_compliance_incidents, 10),
    )
    return sum(w for ok, w in weights if ok)
