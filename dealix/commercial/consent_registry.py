"""Consent Registry — structured operating state for PDPL.

States: NO_CONSENT, SERVICE_CONTACT_ONLY, MARKETING_OPT_IN, CUSTOMER_RELATIONSHIP, WITHDRAWN, DO_NOT_CONTACT
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

class ConsentState(StrEnum):
    NO_CONSENT = "no_consent"
    SERVICE_CONTACT_ONLY = "service_contact_only"
    MARKETING_OPT_IN = "marketing_opt_in"
    CUSTOMER_RELATIONSHIP = "customer_relationship"
    WITHDRAWN = "withdrawn"
    DO_NOT_CONTACT = "do_not_contact"

class ConsentRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    record_id: str
    person_id: str
    channel: str  # email, whatsapp, etc.
    state: ConsentState
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    method: str = "unknown"  # form, inbound, opt_in_link, etc.
    purpose: str = "unknown"
    source: str = "unknown"
    evidence_ref: str = ""

    def is_opted_in(self) -> bool:
        return self.state in (ConsentState.MARKETING_OPT_IN, ConsentState.CUSTOMER_RELATIONSHIP)

    def is_withdrawn(self) -> bool:
        return self.state in (ConsentState.WITHDRAWN, ConsentState.DO_NOT_CONTACT)

class ConsentRegistry:
    def __init__(self) -> None:
        self.records: dict[str, ConsentRecord] = {}

    def set(self, rec: ConsentRecord) -> None:
        self.records[rec.record_id] = rec

    def get_state(self, person_id: str, channel: str) -> ConsentState:
        # latest record for person+channel
        latest = None
        for r in self.records.values():
            if r.person_id == person_id and r.channel == channel:
                if latest is None or r.timestamp > latest.timestamp:
                    latest = r
        return latest.state if latest else ConsentState.NO_CONSENT

    def can_send(self, person_id: str, channel: str) -> bool:
        state = self.get_state(person_id, channel)
        return state in (ConsentState.MARKETING_OPT_IN, ConsentState.CUSTOMER_RELATIONSHIP, ConsentState.SERVICE_CONTACT_ONLY)

    def withdraw(self, person_id: str, channel: str, reason: str = "") -> ConsentRecord:
        rec = ConsentRecord(record_id=f"withdraw_{person_id}_{channel}_{datetime.now(UTC).isoformat()}", person_id=person_id, channel=channel, state=ConsentState.WITHDRAWN, method="withdrawal", purpose=reason, source="user_request")
        self.set(rec)
        return rec

    def to_dict(self) -> dict[str, Any]:
        return {"records": [r.model_dump(mode="json") for r in self.records.values()]}

__all__ = ["ConsentRegistry", "ConsentRecord", "ConsentState"]
