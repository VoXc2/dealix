"""Enrichment waterfall — ordered stages + provenance fields per fact."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class WaterfallStage(IntEnum):
    CUSTOMER_BRAIN = 1
    CRM_OR_SHEET = 2
    COMPANY_WEBSITE = 3
    PUBLIC_BUSINESS_INFO = 4
    OPTIONAL_ENRICHMENT_PROVIDER = 5
    MANUAL_RESEARCH = 6
    INSUFFICIENT_DATA = 7


WATERFALL_ORDER: list[str] = [s.name for s in WaterfallStage]


@dataclass
class FactFieldProvenance:
    """Every enriched field should carry provenance (Dealix rule)."""

    field: str
    value_redacted: str
    source_stage: WaterfallStage
    confidence: float
    collected_at_iso: str | None = None
    allowed_use: str = "sales_qualification"
    provenance_note: str = ""
    risk_level: str = "low"
    refresh_needed: bool = False
