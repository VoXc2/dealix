"""Canonical Capital OS — every project produces >=1 reusable asset.

Asset types: scoring_rule, draft_template, governance_rule, proof_example,
sector_insight, productization_signal, qa_rubric, arabic_style_pattern.
"""
from auto_client_acquisition.capital_os.capital_ledger import (
    ALLOWED_ASSET_TYPES,
    CapitalAsset,
    add_asset,
    clear_for_test,
    list_assets,
)

__all__ = [
    "ALLOWED_ASSET_TYPES",
    "CapitalAsset",
    "add_asset",
    "clear_for_test",
    "list_assets",
]
