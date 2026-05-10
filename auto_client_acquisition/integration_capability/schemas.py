"""Integration Capability schemas — Pydantic v2."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

IntegrationLevel = Literal[1, 2, 3]
# 1 = manual_csv (paste / upload)
# 2 = read_only OAuth
# 3 = controlled_write (approved-only mutations)

IntegrationCategory = Literal[
    "lead_source",
    "crm",
    "spreadsheet",
    "calendar",
    "messaging",
    "payment",
    "compliance",
    "email",
    "analytics",
    "observability",
]


class IntegrationCapability(BaseModel):
    """One integration's trust truth-table entry.

    Hard rule (Article 4): L3 is only set when 'L3_proven_by_5_plus_customers'
    is True AND a name reference is provided. Tests enforce.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    integration_id: str = Field(..., min_length=1, max_length=64)
    name_ar: str
    name_en: str
    category: IntegrationCategory
    current_level: IntegrationLevel
    supported_directions: tuple[Literal["inbound", "outbound", "bidirectional"], ...]
    oauth_required: bool
    trigger_for_next_level_ar: str  # bilingual when next-level activation triggers
    trigger_for_next_level_en: str
    hard_gates_respected: tuple[str, ...]
    L3_proven_by_5_plus_customers: bool = False  # required True for current_level==3
    last_tested_at_iso: str  # YYYY-MM-DD or full ISO
    is_estimate: bool = True
