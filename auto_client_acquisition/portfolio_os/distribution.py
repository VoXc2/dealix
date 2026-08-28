"""V18 Distribution Graph + Proof-to-Distribution (Workstream C/D / §9-11).

ASSET → AUDIENCE → BUYING_GROUP_ROLE → CHANNEL → BUYING_SITUATION → CTA →
EVIDENCE → OUTCOME. Proof reuse is gated on customer permission, claim
support, anonymization, provenance, expiry and sensitivity. No fake
testimonials; no unapproved logos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class DistributionEdge:
    """One distribution edge with expected outcome."""

    asset: str
    audience: str
    buying_group_role: str = "UNKNOWN_STAKEHOLDER"
    channel: str = ""
    buying_situation: str = ""
    cta: str = ""
    evidence: str = ""
    outcome: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "asset": self.asset,
            "audience": self.audience,
            "buying_group_role": self.buying_group_role,
            "channel": self.channel,
            "buying_situation": self.buying_situation,
            "cta": self.cta,
            "evidence": self.evidence,
            "outcome": self.outcome,
        }


def build_distribution_edge(
    asset: str,
    audience: str,
    *,
    buying_group_role: str = "UNKNOWN_STAKEHOLDER",
    channel: str = "",
    buying_situation: str = "",
    cta: str = "",
    evidence: str = "",
    outcome: str = "",
) -> DistributionEdge:
    return DistributionEdge(
        asset=asset,
        audience=audience,
        buying_group_role=buying_group_role,
        channel=channel,
        buying_situation=buying_situation,
        cta=cta,
        evidence=evidence,
        outcome=outcome,
    )


@dataclass(frozen=True, slots=True)
class ProofReuseAssessment:
    """Before reuse of any proof artifact, all gates must pass."""

    proof_id: str
    customer_permission_state: str = "unknown"  # none|granted|denied|unknown
    claim_support: str = ""  # what the artifact actually supports
    anonymization_state: str = "not_required"  # required_done|required_pending|not_required
    source: str = ""
    provenance: str = ""
    expiry: str = ""  # ISO date or "none"
    sensitivity: str = "public"  # public|internal|confidential
    reusable: bool = False
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "proof_id": self.proof_id,
            "customer_permission_state": self.customer_permission_state,
            "claim_support": self.claim_support,
            "anonymization_state": self.anonymization_state,
            "source": self.source,
            "provenance": self.provenance,
            "expiry": self.expiry,
            "sensitivity": self.sensitivity,
            "reusable": self.reusable,
            "reasons": self.reasons,
        }


def evaluate_proof_reuse(
    proof_id: str,
    *,
    customer_permission_state: str = "unknown",
    claim_support: str = "",
    anonymization_state: str = "not_required",
    source: str = "",
    provenance: str = "",
    expiry: str = "",
    sensitivity: str = "public",
) -> ProofReuseAssessment:
    """Deterministic proof reuse gate. Reusable only when every control
    passes; unknown permission or expired/sensitive artifacts are blocked."""
    reasons: list[str] = []

    permission = str(customer_permission_state or "unknown").strip().lower()
    if permission == "granted":
        pass
    elif permission == "denied":
        reasons.append("PERMISSION_DENIED")
    else:
        reasons.append("PERMISSION_UNKNOWN_OR_MISSING")

    if not str(claim_support or "").strip():
        reasons.append("NO_CLAIM_SUPPORT")

    anon = str(anonymization_state or "").strip().lower()
    if anon == "required_pending":
        reasons.append("ANONYMIZATION_PENDING")
    if anon not in {"required_done", "not_required", "required_pending"}:
        reasons.append("ANONYMIZATION_STATE_INVALID")

    if not str(source or "").strip():
        reasons.append("NO_SOURCE")
    if not str(provenance or "").strip():
        reasons.append("NO_PROVENANCE")

    if str(expiry or "").strip() and str(expiry or "").strip().lower() != "none":
        # If an expiry is declared, treat it as active risk unless explicitly
        # marked "none"; a concrete expiry date is checked by the caller with
        # a clock. Deterministic here: only "none" is acceptable for reuse.
        reasons.append("EXPIRY_NOT_NONE")

    sens = str(sensitivity or "").strip().lower()
    if sens == "confidential":
        reasons.append("CONFIDENTIAL")
    if sens not in {"public", "internal", "confidential"}:
        reasons.append("SENSITIVITY_INVALID")

    reusable = not reasons
    return ProofReuseAssessment(
        proof_id=proof_id,
        customer_permission_state=customer_permission_state,
        claim_support=claim_support,
        anonymization_state=anonymization_state,
        source=source,
        provenance=provenance,
        expiry=expiry,
        sensitivity=sensitivity,
        reusable=reusable,
        reasons=reasons,
    )
