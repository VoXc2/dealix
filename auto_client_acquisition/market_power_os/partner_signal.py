"""Partner gate signals for distribution readiness (Market Power)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PartnerGateSignals:
    understands_dealix_method: bool = False
    respects_no_unsafe_automation: bool = False
    commits_to_proof_pack: bool = False
    accepts_qa: bool = False
    accepts_audit_rights: bool = False
    no_guaranteed_claims: bool = False


_GATE_WEIGHTS: dict[str, int] = {
    "understands_dealix_method": 20,
    "respects_no_unsafe_automation": 20,
    "commits_to_proof_pack": 15,
    "accepts_qa": 15,
    "accepts_audit_rights": 10,
    "no_guaranteed_claims": 20,
}


def compute_partner_gate_readiness(signals: PartnerGateSignals) -> int:
    """Weighted readiness 0-100 for elevating a partner."""
    d = {
        "understands_dealix_method": signals.understands_dealix_method,
        "respects_no_unsafe_automation": signals.respects_no_unsafe_automation,
        "commits_to_proof_pack": signals.commits_to_proof_pack,
        "accepts_qa": signals.accepts_qa,
        "accepts_audit_rights": signals.accepts_audit_rights,
        "no_guaranteed_claims": signals.no_guaranteed_claims,
    }
    if set(d) != set(_GATE_WEIGHTS):
        raise RuntimeError("PartnerGateSignals out of sync with weights")
    if sum(_GATE_WEIGHTS.values()) != 100:
        raise RuntimeError("partner gate weights must sum to 100")
    return sum(_GATE_WEIGHTS[k] for k, v in d.items() if v)
