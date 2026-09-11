"""Relationship Graph — first-class commercial asset.

Tracks ENTITY/PERSON/ROLE/HOW_KNOWN/INTERACTIONS/TRUST/CONSENT etc.
Real relationships outrank scraped lists.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class RelationshipStage(StrEnum):
    SIGNAL = "signal"
    CONTACT_KNOWN = "contact_known"
    CONVERSATION = "conversation"
    QUALIFIED = "qualified"
    DIAGNOSTIC = "diagnostic"
    DISCOVERY = "discovery"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    PILOT = "pilot"
    CUSTOMER = "customer"
    EXPANSION = "expansion"
    DORMANT = "dormant"

class RelationshipRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str
    entity_name: str
    person_name: str = UNKNOWN
    role: str = UNKNOWN
    how_known: str = UNKNOWN  # warm_intro, inbound, event, referral, etc.
    interactions: int = 0
    trust_score: int = Field(default=0, ge=0, le=5)
    consent_state: str = UNKNOWN
    promises: list[str] = Field(default_factory=list)
    open_loop: str = UNKNOWN
    commercial_stage: RelationshipStage = RelationshipStage.SIGNAL
    next_action: str = UNKNOWN
    do_not_contact: bool = False
    last_interaction_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    evidence_refs: list[str] = Field(default_factory=list)

    def can_contact(self) -> bool:
        return not self.do_not_contact and self.consent_state not in ("withdrawn", "do_not_contact")

    def advance_stage(self, new_stage: RelationshipStage, evidence_ref: str = "") -> None:
        self.commercial_stage = new_stage
        if evidence_ref:
            self.evidence_refs.append(evidence_ref)
        self.last_interaction_at = datetime.now(UTC).isoformat()

class RelationshipGraph:
    def __init__(self) -> None:
        self.records: dict[str, RelationshipRecord] = {}

    def add(self, rec: RelationshipRecord) -> None:
        self.records[rec.record_id] = rec

    def warm_relationships(self) -> list[RelationshipRecord]:
        return [r for r in self.records.values() if r.how_known in ("warm_intro", "inbound", "referral", "customer", "event_conversation") and r.trust_score >= 2]

    def stale_opportunities(self, days: int = 14) -> list[RelationshipRecord]:
        # no evidence + no next action + no recent interaction
        stale = []
        for r in self.records.values():
            if not r.evidence_refs and r.next_action == UNKNOWN:
                stale.append(r)
        return stale

    def to_dict(self) -> dict[str, Any]:
        return {"records": [r.model_dump(mode="json") for r in self.records.values()], "warm_count": len(self.warm_relationships())}

__all__ = ["RelationshipGraph", "RelationshipRecord", "RelationshipStage", "UNKNOWN"]
