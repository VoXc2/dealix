"""Capital Asset schema — Wave 19.

Strategic Capital Assets are the reusable artefacts Dealix has BUILT that
compound across engagements: the Dealix Promise API, the 11 non-negotiables,
the 3-offer ladder registry, the investor pager, partner outreach kit, etc.

This is COMPLEMENTARY to `capital_ledger.py` — the ledger holds per-engagement
runtime entries; this module holds Dealix's own strategic asset catalogue
that the founder shows to partners, investors, hires, and reviewers.

The 10 asset types correspond to the 10 strategic surfaces:
  trust_asset, sales_asset, product_asset, doctrine_asset,
  proof_asset, partner_asset, investor_asset, hiring_asset,
  standard_asset, market_asset

Per-asset doctrine: every entry MUST cite its file paths (so reviewers
can verify) and at least one linked non-negotiable id (so the asset is
provably aligned with the doctrine).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AssetType = Literal[
    "trust_asset",
    "sales_asset",
    "product_asset",
    "doctrine_asset",
    "proof_asset",
    "partner_asset",
    "investor_asset",
    "hiring_asset",
    "standard_asset",
    "market_asset",
    "revenue_ops_asset",
]

AssetMaturity = Literal["live", "draft", "planned", "deprecated"]
ProofLevel = Literal["test-backed", "code-backed", "doc-backed", "process-backed"]


@dataclass(frozen=True)
class CapitalAsset:
    """One strategic Capital Asset Dealix has built.

    The 'public' field controls exposure on /api/v1/capital-assets/public
    — only assets explicitly marked public=True surface there. Default is
    False so commercial-sensitive entries never leak by omission.
    """
    asset_id: str
    name: str
    type: AssetType
    strategic_role: str
    file_paths: tuple[str, ...]
    buyer_relevance: tuple[str, ...]
    commercial_use: tuple[str, ...]
    maturity: AssetMaturity
    linked_non_negotiables: tuple[str, ...]
    proof_level: ProofLevel
    last_reviewed: str  # ISO date string (YYYY-MM-DD)
    public: bool = False


__all__ = [
    "AssetType",
    "AssetMaturity",
    "ProofLevel",
    "CapitalAsset",
]
