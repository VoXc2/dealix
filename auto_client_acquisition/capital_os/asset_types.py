"""Capital asset type labels for ledger entries (Commercial Trust MVP)."""

from __future__ import annotations

from enum import StrEnum


class CapitalAssetType(StrEnum):
    SCORING_RULE = "scoring_rule"
    DRAFT_TEMPLATE = "draft_template"
    GOVERNANCE_RULE = "governance_rule"
    PROOF_EXAMPLE = "proof_example"
    SECTOR_INSIGHT = "sector_insight"
    PRODUCTIZATION_SIGNAL = "productization_signal"


__all__ = ["CapitalAssetType"]
