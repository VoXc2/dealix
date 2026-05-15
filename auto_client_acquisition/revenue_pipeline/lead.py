"""Revenue Pipeline — Lead schema (placeholders only, NEVER PII)."""
from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.revenue_pipeline.stage_policy import PipelineStage


def _lead_id(slot: str, sector: str) -> str:
    digest = hashlib.sha256(f"{slot}|{sector}".encode()).hexdigest()
    return f"lead_{digest[:16]}"


class Lead(BaseModel):
    """A single revenue-pipeline lead.

    Fields are placeholder-shaped. Real names / emails / phones MUST
    stay in the founder's private vault, never in this object.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    slot_id: str = Field(min_length=1, max_length=40)
    sector: str = "tbd"
    region: str = "tbd"
    relationship_strength: str = "warm_intro"
    consent_status: str = "not_yet_asked"
    stage: PipelineStage = "warm_intro_selected"
    last_touch_at: datetime | None = None
    expected_amount_sar: int | None = None
    actual_amount_sar: int | None = None
    commitment_evidence: str = ""
    payment_evidence: str = ""
    notes_placeholder: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def make(
        cls,
        *,
        slot_id: str,
        sector: str = "tbd",
        region: str = "tbd",
        **extra: Any,
    ) -> Lead:
        return cls(id=_lead_id(slot_id, sector), slot_id=slot_id,
                   sector=sector, region=region, **extra)
