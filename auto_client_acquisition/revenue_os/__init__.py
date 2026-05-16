"""
Revenue OS spine — Market Radar → Lead Machine → Actions → Proof alignment.

Pure logic + catalogs; no scraping, no outbound sends. Composes existing
`growth_beast.market_radar.MarketSignal` and Decision Passport patterns.
"""

from __future__ import annotations

from auto_client_acquisition.revenue_os.account_model import AccountRow
from auto_client_acquisition.revenue_os.account_scoring import score_account_row
from auto_client_acquisition.revenue_os.action_catalog import (
    ACTION_DEFAULT_MODE,
    ActionKind,
    ActionMode,
    list_action_catalog,
)
from auto_client_acquisition.revenue_os.anti_waste import AntiWasteViolation, validate_pipeline_step
from auto_client_acquisition.revenue_os.dedupe import DedupeHint, suggest_dedupe_fingerprint
from auto_client_acquisition.revenue_os.data_flywheel import (
    FlywheelInputs,
    FlywheelScore,
    compute_flywheel_score,
    flywheel_inputs_from_import_quality,
    flywheel_inputs_from_preview,
    gating_failures,
)
from auto_client_acquisition.revenue_os.draft_pack import build_revenue_draft_pack
from auto_client_acquisition.revenue_os.enrichment_waterfall import (
    WATERFALL_ORDER,
    FactFieldProvenance,
    WaterfallStage,
)
from auto_client_acquisition.revenue_os.data_flywheel import (
    FlywheelInputs,
    FlywheelScore,
    compute_flywheel_score,
    flywheel_inputs_from_import_quality,
    flywheel_inputs_from_preview,
    gating_failures,
)
from auto_client_acquisition.revenue_os.expansion_engine import next_best_offer
from auto_client_acquisition.revenue_os.followup_plan import default_follow_up_plan_bullets
from auto_client_acquisition.revenue_os.governed_value_decisions import (
    CORE_COMMERCIAL_OFFERS,
    EVIDENCE_STATE_LEVEL,
    NORTH_STAR_DEFINITION_AR,
    NORTH_STAR_DEFINITION_EN,
    NORTH_STAR_KEY,
    can_recognize_revenue,
    is_governed_value_decision,
    next_allowed_states,
    validate_transition,
)
from auto_client_acquisition.revenue_os.proof_canonical import ProofEventCanonical
from auto_client_acquisition.revenue_os.revenue_summary import summarize_scored_accounts
from auto_client_acquisition.revenue_os.signal_normalizer import (
    normalize_market_signal,
    normalize_signals_batch,
)
from auto_client_acquisition.revenue_os.source_registry import (
    SourcePolicy,
    Tier1LeadSource,
    forbidden_sources,
    get_source_policy,
    source_policies,
)
from auto_client_acquisition.revenue_os.targeting import (
    SaudiTargetingProfile,
    anti_waste_violations_for_tier1_intake,
    assert_tier1_storage_allowed,
    build_local_discover_body,
    map_tier1_to_intake_lead_source,
    merge_targeting_into_discover_body,
    parse_tier1_lead_source,
)

__all__ = [
    "ACTION_DEFAULT_MODE",
    "AccountRow",
    "WATERFALL_ORDER",
    "ActionKind",
    "ActionMode",
    "AntiWasteViolation",
    "CORE_COMMERCIAL_OFFERS",
    "DedupeHint",
    "EVIDENCE_STATE_LEVEL",
    "FlywheelInputs",
    "FlywheelScore",
    "FactFieldProvenance",
    "FlywheelInputs",
    "FlywheelScore",
    "NORTH_STAR_DEFINITION_AR",
    "NORTH_STAR_DEFINITION_EN",
    "NORTH_STAR_KEY",
    "ProofEventCanonical",
    "SaudiTargetingProfile",
    "SourcePolicy",
    "Tier1LeadSource",
    "WaterfallStage",
    "anti_waste_violations_for_tier1_intake",
    "assert_tier1_storage_allowed",
    "compute_flywheel_score",
    "flywheel_inputs_from_import_quality",
    "flywheel_inputs_from_preview",
    "gating_failures",
    "build_local_discover_body",
    "build_revenue_draft_pack",
    "default_follow_up_plan_bullets",
    "forbidden_sources",
    "gating_failures",
    "get_source_policy",
    "list_action_catalog",
    "map_tier1_to_intake_lead_source",
    "merge_targeting_into_discover_body",
    "next_best_offer",
    "next_allowed_states",
    "normalize_market_signal",
    "normalize_signals_batch",
    "parse_tier1_lead_source",
    "score_account_row",
    "source_policies",
    "summarize_scored_accounts",
    "suggest_dedupe_fingerprint",
    "can_recognize_revenue",
    "compute_flywheel_score",
    "flywheel_inputs_from_import_quality",
    "flywheel_inputs_from_preview",
    "is_governed_value_decision",
    "validate_pipeline_step",
    "validate_transition",
]
