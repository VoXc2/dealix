"""Minimal signal record for the growth beast loop."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MarketSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(min_length=1, max_length=64)
    source: str = Field(
        description="e.g. inbound_form, partner_ping, content_reply, founder_note",
    )
    summary_ar: str = ""
    strength: int = Field(ge=0, le=100, default=50)
