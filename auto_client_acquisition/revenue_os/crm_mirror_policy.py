"""Fail-closed policy for mirroring Dealix commercial truth into HubSpot.

Dealix Company OS / Revenue Mesh owns commercial truth. HubSpot is an
operational CRM mirror only. A fit score, directory record, research record,
draft proposal, invoice, or CRM deal must never manufacture relationship,
opportunity, payment, or revenue truth.

This module is intentionally deterministic and side-effect free so legacy
intake/pipeline code cannot bypass the Revenue Mesh truth firewall simply by
calling the HubSpot adapter directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.agents.intake import Lead, LeadStatus


REAL_TRUTH_CLASSES = frozenset({"real"})
CONTACT_MIRROR_STATES = frozenset(
    {
        "real_relationship",
        "qualification_candidate",
        "qualified",
        "diagnostic",
        "discovery",
        "quote",
        "pilot",
        "paid",
        "proof",
        "recurring",
    }
)
DEAL_MIRROR_STATES = frozenset(
    {
        "qualified",
        "diagnostic",
        "discovery",
        "quote",
        "pilot",
        "paid",
        "proof",
        "recurring",
    }
)


@dataclass(frozen=True, slots=True)
class HubSpotMirrorDecision:
    """Deterministic decision for one HubSpot mirror attempt."""

    allow_contact: bool
    allow_deal: bool
    reasons: tuple[str, ...]
    relationship_state: str
    evidence_id: str
    opportunity_id: str
    payment_verified: bool
    payment_evidence_id: str
    approved_quote_amount_sar: float | None

    @property
    def blocked(self) -> bool:
        return not self.allow_contact


def _text(metadata: dict[str, Any], key: str) -> str:
    value = metadata.get(key)
    return str(value).strip() if value is not None else ""


def _bool(metadata: dict[str, Any], key: str) -> bool:
    return metadata.get(key) is True


def _approved_quote_amount(metadata: dict[str, Any]) -> float | None:
    """Return an approved quote amount only when quote evidence is present.

    A lead budget is not a quote and a quote is not revenue. This value is used
    only as CRM opportunity metadata and is never payment evidence.
    """

    if not _text(metadata, "quote_evidence_id"):
        return None
    value = metadata.get("approved_quote_amount_sar")
    if value is None or isinstance(value, bool):
        return None
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return None
    return amount if amount >= 0 else None


def evaluate_hubspot_mirror(lead: Lead) -> HubSpotMirrorDecision:
    """Evaluate whether a lead may be mirrored to HubSpot.

    Required contact evidence:
    - an internal trusted adapter explicitly stamped ``authority_verified``;
    - ``truth_class == real``;
    - a source-bound ``evidence_id``;
    - relationship state at/after a real relationship;
    - an actual email or phone (never a fabricated placeholder).

    A HubSpot deal requires the stronger qualified-opportunity state plus an
    ``opportunity_id``. ``closedwon`` additionally requires verified payment
    evidence. Unknown/research/synthetic/test records fail closed.
    """

    metadata = lead.metadata if isinstance(lead.metadata, dict) else {}
    reasons: list[str] = []

    relationship_state = _text(metadata, "relationship_state").casefold()
    truth_class = _text(metadata, "truth_class").casefold()
    evidence_id = _text(metadata, "evidence_id")
    opportunity_id = _text(metadata, "opportunity_id")
    payment_evidence_id = _text(metadata, "payment_evidence_id")
    payment_verified = _bool(metadata, "payment_verified") and bool(payment_evidence_id)

    if not _bool(metadata, "authority_verified"):
        reasons.append("AUTHORITY_NOT_VERIFIED")
    if truth_class not in REAL_TRUTH_CLASSES:
        reasons.append("TRUTH_CLASS_NOT_REAL")
    if _bool(metadata, "self_test"):
        reasons.append("SELF_TEST")
    if _bool(metadata, "synthetic"):
        reasons.append("SYNTHETIC")
    if _bool(metadata, "suppressed"):
        reasons.append("SUPPRESSED")
    if _bool(metadata, "opted_out"):
        reasons.append("OPTED_OUT")
    if not evidence_id:
        reasons.append("NO_EVIDENCE_ID")
    if relationship_state not in CONTACT_MIRROR_STATES:
        reasons.append("RELATIONSHIP_NOT_VERIFIED")
    if not (lead.contact_email or lead.contact_phone):
        reasons.append("NO_REAL_CONTACT_IDENTIFIER")

    allow_contact = not reasons

    deal_reasons: list[str] = []
    if not allow_contact:
        deal_reasons.append("CONTACT_MIRROR_BLOCKED")
    if relationship_state not in DEAL_MIRROR_STATES:
        deal_reasons.append("OPPORTUNITY_NOT_QUALIFIED")
    if not opportunity_id:
        deal_reasons.append("NO_OPPORTUNITY_ID")
    if lead.status == LeadStatus.WON and not payment_verified:
        deal_reasons.append("WON_WITHOUT_PAYMENT_EVIDENCE")

    allow_deal = not deal_reasons
    all_reasons = tuple(dict.fromkeys([*reasons, *deal_reasons]))

    return HubSpotMirrorDecision(
        allow_contact=allow_contact,
        allow_deal=allow_deal,
        reasons=all_reasons,
        relationship_state=relationship_state,
        evidence_id=evidence_id,
        opportunity_id=opportunity_id,
        payment_verified=payment_verified,
        payment_evidence_id=payment_evidence_id,
        approved_quote_amount_sar=_approved_quote_amount(metadata),
    )
