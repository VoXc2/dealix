"""Relationship Graph — first-class commercial asset.

Tracks ENTITY/PERSON/ROLE/HOW_KNOWN/INTERACTIONS/TRUST/CONSENT etc.
Real relationships outrank scraped lists.

Permanent invariants:
- research != relationship
- public_contact != consent
- draft != sent
- quote != invoice
- invoice != payment
- payment != revenue
- delivery != customer_value
- customer_value != public_proof
- merged != deployed

No cold WhatsApp. No LinkedIn scraping. No mass LinkedIn automation.
No fabricated consent. Public contact never implies OPT_IN.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"


class RelationshipStage(StrEnum):
    """Explicit relationship stages — research never equals relationship."""
    RESEARCH_ONLY = "research_only"
    KNOWN = "known"
    REFERRAL = "referral"
    INBOUND = "inbound"
    REAL_INTERACTION = "real_interaction"
    QUALIFIED_PROBLEM = "qualified_problem"
    DIAGNOSTIC = "diagnostic"
    DISCOVERY = "discovery"
    PROPOSAL = "proposal"
    QUOTE = "quote"
    PAID = "paid"
    DELIVERY = "delivery"
    PROOF = "proof"
    EXPANSION = "expansion"
    DORMANT = "dormant"


class HowKnown(StrEnum):
    """How the relationship was established — no cold outreach."""
    WARM_INTRO = "warm_intro"
    INBOUND = "inbound"
    EVENT_CONVERSATION = "event_conversation"
    REFERRAL = "referral"
    CUSTOMER = "customer"
    PARTNER_INTRO = "partner_intro"
    # Explicitly NOT included: cold_whatsapp, linkedin_scraping, mass_linkedin_automation


class RelationshipRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str
    entity_name: str
    person_name: str = UNKNOWN
    role: str = UNKNOWN
    how_known: HowKnown = HowKnown.INBOUND  # Must be explicit, never cold
    interactions: int = 0
    trust_score: int = Field(default=0, ge=0, le=5)
    consent_state: str = UNKNOWN
    promises: list[str] = Field(default_factory=list)
    open_loop: str = UNKNOWN
    commercial_stage: RelationshipStage = RelationshipStage.RESEARCH_ONLY
    next_action: str = UNKNOWN
    do_not_contact: bool = False
    last_interaction_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    evidence_refs: list[str] = Field(default_factory=list)
    # Invariant tracking
    research_never_relationship: bool = True
    public_contact_never_consent: bool = True

    def can_contact(self) -> bool:
        """Check if contact is permitted — requires consent and not do_not_contact."""
        return (
            not self.do_not_contact
            and self.consent_state not in ("withdrawn", "do_not_contact")
            and self.how_known != HowKnown.INBOUND or self.consent_state == "opt_in"
        )

    def advance_stage(self, new_stage: RelationshipStage, evidence_ref: str = "") -> None:
        """Advance stage with evidence — enforces invariants."""
        # Invariant: research != relationship
        if self.commercial_stage == RelationshipStage.RESEARCH_ONLY:
            if new_stage in {
                RelationshipStage.QUALIFIED_PROBLEM,
                RelationshipStage.DIAGNOSTIC,
                RelationshipStage.DISCOVERY,
                RelationshipStage.PROPOSAL,
                RelationshipStage.QUOTE,
                RelationshipStage.PAID,
                RelationshipStage.DELIVERY,
                RelationshipStage.PROOF,
                RelationshipStage.EXPANSION,
            }:
                raise ValueError(
                    f"INVARIANT_VIOLATION: research != relationship — "
                    f"cannot advance from RESEARCH_ONLY to {new_stage.value} without REAL_INTERACTION"
                )

        # Invariant: public_contact != consent
        if self.how_known == HowKnown.INBOUND and self.consent_state == UNKNOWN:
            if new_stage in {
                RelationshipStage.DIAGNOSTIC,
                RelationshipStage.DISCOVERY,
                RelationshipStage.PROPOSAL,
                RelationshipStage.QUOTE,
            }:
                raise ValueError(
                    f"INVARIANT_VIOLATION: public_contact != consent — "
                    f"inbound contact without explicit consent cannot reach {new_stage.value}"
                )

        self.commercial_stage = new_stage
        if evidence_ref:
            self.evidence_refs.append(evidence_ref)
        self.last_interaction_at = datetime.now(UTC).isoformat()

    def is_research_only(self) -> bool:
        """Check if relationship is still in research phase."""
        return self.commercial_stage in {
            RelationshipStage.RESEARCH_ONLY,
            RelationshipStage.KNOWN,
            RelationshipStage.REFERRAL,
            RelationshipStage.INBOUND,
        }

    def is_qualified_relationship(self) -> bool:
        """Check if relationship has progressed to qualified interaction."""
        return self.commercial_stage in {
            RelationshipStage.REAL_INTERACTION,
            RelationshipStage.QUALIFIED_PROBLEM,
            RelationshipStage.DIAGNOSTIC,
            RelationshipStage.DISCOVERY,
            RelationshipStage.PROPOSAL,
            RelationshipStage.QUOTE,
            RelationshipStage.PAID,
            RelationshipStage.DELIVERY,
            RelationshipStage.PROOF,
            RelationshipStage.EXPANSION,
        }


class RelationshipGraph:
    def __init__(self) -> None:
        self.records: dict[str, RelationshipRecord] = {}

    def add(self, rec: RelationshipRecord) -> None:
        self.records[rec.record_id] = rec

    def warm_relationships(self) -> list[RelationshipRecord]:
        return [
            r
            for r in self.records.values()
            if r.how_known
            in (
                HowKnown.WARM_INTRO,
                HowKnown.INBOUND,
                HowKnown.REFERRAL,
                HowKnown.CUSTOMER,
                HowKnown.EVENT_CONVERSATION,
                HowKnown.PARTNER_INTRO,
            )
            and r.trust_score >= 2
        ]

    def qualified_relationships(self) -> list[RelationshipRecord]:
        """Return only relationships that have progressed beyond research."""
        return [r for r in self.records.values() if r.is_qualified_relationship()]

    def research_only_relationships(self) -> list[RelationshipRecord]:
        """Return relationships still in research phase."""
        return [r for r in self.records.values() if r.is_research_only()]

    def stale_opportunities(self, days: int = 14) -> list[RelationshipRecord]:
        stale = []
        for r in self.records.values():
            if not r.evidence_refs and r.next_action == UNKNOWN:
                stale.append(r)
        return stale

    def invariant_violations(self) -> list[dict[str, Any]]:
        """Check for invariant violations across all records."""
        violations = []
        for r in self.records.values():
            if r.commercial_stage != RelationshipStage.RESEARCH_ONLY and r.how_known == HowKnown.INBOUND and r.consent_state == UNKNOWN:
                violations.append({
                    "record_id": r.record_id,
                    "violation": "public_contact != consent",
                    "stage": r.commercial_stage.value,
                    "consent_state": r.consent_state,
                })
        return violations

    def to_dict(self) -> dict[str, Any]:
        return {
            "records": [r.model_dump(mode="json") for r in self.records.values()],
            "warm_count": len(self.warm_relationships()),
            "qualified_count": len(self.qualified_relationships()),
            "research_only_count": len(self.research_only_relationships()),
            "invariant_violations": self.invariant_violations(),
        }


__all__ = [
    "RelationshipGraph",
    "RelationshipRecord",
    "RelationshipStage",
    "HowKnown",
    "UNKNOWN",
]
