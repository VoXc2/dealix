"""Partner readiness score — compliance + operating maturity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PartnerReadinessInputs:
    trust_pack_acknowledged: bool = False
    governance_rules_acknowledged: bool = False
    qa_review_required_acknowledged: bool = False
    proof_pack_required_acknowledged: bool = False
    no_guaranteed_claims_acknowledged: bool = False
    no_unsafe_automation_acknowledged: bool = False
    no_fake_proof_acknowledged: bool = False
    certification_path_defined: bool = False
    audit_rights_defined: bool = False
    delivery_standard_documented: bool = False


_CHECKS: tuple[tuple[str, str], ...] = (
    ("trust_pack_acknowledged", "acknowledge_trust_pack"),
    ("governance_rules_acknowledged", "acknowledge_governance_rules"),
    ("qa_review_required_acknowledged", "acknowledge_qa_review"),
    ("proof_pack_required_acknowledged", "acknowledge_proof_pack"),
    ("no_guaranteed_claims_acknowledged", "acknowledge_no_guaranteed_claims"),
    ("no_unsafe_automation_acknowledged", "acknowledge_no_unsafe_automation"),
    ("no_fake_proof_acknowledged", "acknowledge_no_fake_proof"),
    ("certification_path_defined", "define_certification_path"),
    ("audit_rights_defined", "define_audit_rights"),
    ("delivery_standard_documented", "document_delivery_standard"),
)


def compute_partner_readiness_score(inp: PartnerReadinessInputs) -> tuple[int, list[str]]:
    """Return score 0-100 and list of missing requirement keys."""
    missing: list[str] = []
    for field, code in _CHECKS:
        if not getattr(inp, field):
            missing.append(code)
    passed = len(_CHECKS) - len(missing)
    score = passed * 10
    return score, missing
