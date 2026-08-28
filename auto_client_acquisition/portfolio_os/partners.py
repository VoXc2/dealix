"""V18 Partner / Referral Compounding (Workstream H / §16).

For every real relationship evaluate lawful natural paths. Never invent a
referral; never call a public employee/contact a relationship. All paths
require relationship evidence and consent-aware posture.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class PartnerPath(StrEnum):
    CUSTOMER_REFERRAL = "CUSTOMER_REFERRAL"
    INTERNAL_REFERRAL = "INTERNAL_REFERRAL"
    PARTNER_INTRODUCTION = "PARTNER_INTRODUCTION"
    CHANNEL_PARTNERSHIP = "CHANNEL_PARTNERSHIP"
    IMPLEMENTATION_PARTNERSHIP = "IMPLEMENTATION_PARTNERSHIP"
    CO_DELIVERY = "CO_DELIVERY"
    SAUDI_MARKET_ACCESS = "SAUDI_MARKET_ACCESS"
    B2G_PRIME = "B2G_PRIME"
    SUBCONTRACTOR_PATH = "SUBCONTRACTOR_PATH"


_VALID_PATHS = frozenset(p.value for p in PartnerPath)


@dataclass(frozen=True, slots=True)
class PartnerPathAssessment:
    """One evaluated compounding path for one relationship."""

    relationship_id: str
    path: str
    status: str = "NOT_EVALUATED"  # NOT_EVALUATED|PLAUSIBLE|ACTIVE|DECLINED
    relationship_evidence: str = ""
    consent_state: str = "unknown"
    next_action: str = ""
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "relationship_id": self.relationship_id,
            "path": self.path,
            "status": self.status,
            "relationship_evidence": self.relationship_evidence,
            "consent_state": self.consent_state,
            "next_action": self.next_action,
            "reasons": self.reasons,
        }


def assess_partner_path(
    relationship_id: str,
    path: str,
    *,
    relationship_evidence: str = "",
    consent_state: str = "unknown",
    plausible: bool = False,
    active: bool = False,
    declined: bool = False,
    next_action: str = "",
) -> PartnerPathAssessment:
    """Deterministic path evaluation.

    - No relationship evidence → status NOT_EVALUATED (never invented).
    - plausible/active/declined only when relationship evidence exists.
    - A public employee/contact without two-way exchange is never ACTIVE.
    """
    reasons: list[str] = []
    if path not in _VALID_PATHS:
        reasons.append(f"INVALID_PATH:{path}")
    if not str(relationship_evidence or "").strip():
        reasons.append("NO_RELATIONSHIP_EVIDENCE")
        return PartnerPathAssessment(
            relationship_id=relationship_id,
            path=path,
            status="NOT_EVALUATED",
            relationship_evidence=relationship_evidence,
            consent_state=consent_state,
            next_action="",
            reasons=reasons,
        )
    if active and not plausible:
        reasons.append("ACTIVE_WITHOUT_PLAUSIBLE")
    if active and str(consent_state or "").lower() not in {
        "consented",
        "opted_in",
        "explicit_consent",
        "approved",
    }:
        reasons.append("ACTIVE_WITHOUT_CONSENT")
    status = "NOT_EVALUATED"
    if declined:
        status = "DECLINED"
    elif active and not reasons:
        status = "ACTIVE"
    elif plausible and not reasons:
        status = "PLAUSIBLE"
    return PartnerPathAssessment(
        relationship_id=relationship_id,
        path=path,
        status=status,
        relationship_evidence=relationship_evidence,
        consent_state=consent_state,
        next_action=next_action,
        reasons=reasons,
    )
