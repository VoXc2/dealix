"""Partner Covenant — typed evaluator for the Dealix partner contract.

See ``docs/global_grade/ACADEMY_PARTNERS.md`` and
``docs/operating_manual/DEALIX_NON_NEGOTIABLES.md``.

A partner must accept the covenant in writing before delivering any
work under the Dealix brand or method.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CovenantClause(str, Enum):
    NO_UNSAFE_AUTOMATION = "no_unsafe_automation"
    NO_GUARANTEED_CLAIMS = "no_guaranteed_claims"
    PROOF_PACK_REQUIRED = "proof_pack_required"
    QA_REVIEW_ACCEPTED = "qa_review_accepted"
    GOVERNANCE_RULES_REQUIRED = "governance_rules_required"
    AUDIT_RIGHTS_ACCEPTED = "audit_rights_accepted"


PARTNER_COVENANT_CLAUSES: tuple[CovenantClause, ...] = tuple(CovenantClause)


class CovenantStatus(str, Enum):
    SIGNED = "signed"
    PENDING = "pending"
    VIOLATED = "violated"
    EXPIRED = "expired"


@dataclass(frozen=True)
class PartnerCovenant:
    """A partner's covenant acceptance record."""

    partner_id: str
    partner_name: str
    accepted_clauses: frozenset[CovenantClause]
    status: CovenantStatus
    method_version: str
    signed_at: str | None = None       # ISO-8601
    recertify_by: str | None = None    # ISO-8601

    def __post_init__(self) -> None:
        if not self.partner_id:
            raise ValueError("partner_id_required")
        if not self.partner_name:
            raise ValueError("partner_name_required")
        if not self.method_version:
            raise ValueError("method_version_required")


@dataclass(frozen=True)
class PartnerCovenantEvaluation:
    can_deliver_under_dealix_brand: bool
    missing_clauses: tuple[CovenantClause, ...]
    reasons: tuple[str, ...]


def evaluate_partner_covenant(covenant: PartnerCovenant) -> PartnerCovenantEvaluation:
    """Decide whether the partner may deliver under the Dealix brand."""

    reasons: list[str] = []
    missing = tuple(
        c for c in PARTNER_COVENANT_CLAUSES if c not in covenant.accepted_clauses
    )

    if missing:
        reasons.append("missing_clauses:" + ",".join(c.value for c in missing))
    if covenant.status is CovenantStatus.PENDING:
        reasons.append("covenant_pending_signature")
    if covenant.status is CovenantStatus.VIOLATED:
        reasons.append("partner_paused_for_violation")
    if covenant.status is CovenantStatus.EXPIRED:
        reasons.append("covenant_expired_recertification_required")

    can_deliver = (
        not missing
        and covenant.status is CovenantStatus.SIGNED
    )
    return PartnerCovenantEvaluation(
        can_deliver_under_dealix_brand=can_deliver,
        missing_clauses=missing,
        reasons=tuple(reasons),
    )
