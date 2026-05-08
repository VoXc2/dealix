"""
Revenue OS spine — Market Radar → Lead Machine → Actions → Proof alignment.

Pure logic + catalogs; no scraping, no outbound sends. Composes existing
`growth_beast.market_radar.MarketSignal` and Decision Passport patterns.
"""

from __future__ import annotations

from auto_client_acquisition.revenue_os.action_catalog import (
    ACTION_DEFAULT_MODE,
    ActionKind,
    ActionMode,
    list_action_catalog,
)
from auto_client_acquisition.revenue_os.anti_waste import AntiWasteViolation, validate_pipeline_step
from auto_client_acquisition.revenue_os.dedupe import DedupeHint, suggest_dedupe_fingerprint
from auto_client_acquisition.revenue_os.enrichment_waterfall import (
    WATERFALL_ORDER,
    FactFieldProvenance,
    WaterfallStage,
)
from auto_client_acquisition.revenue_os.expansion_engine import next_best_offer
from auto_client_acquisition.revenue_os.proof_canonical import ProofEventCanonical
from auto_client_acquisition.revenue_os.signal_normalizer import (
    normalize_market_signal,
    normalize_signals_batch,
)
from auto_client_acquisition.revenue_os.source_registry import (
    SourcePolicy,
    Tier1LeadSource,
    forbidden_sources,
    source_policies,
)

__all__ = [
    "ACTION_DEFAULT_MODE",
    "WATERFALL_ORDER",
    "ActionKind",
    "ActionMode",
    "AntiWasteViolation",
    "DedupeHint",
    "FactFieldProvenance",
    "ProofEventCanonical",
    "SourcePolicy",
    "Tier1LeadSource",
    "WaterfallStage",
    "forbidden_sources",
    "list_action_catalog",
    "next_best_offer",
    "normalize_market_signal",
    "normalize_signals_batch",
    "source_policies",
    "suggest_dedupe_fingerprint",
    "validate_pipeline_step",
]
