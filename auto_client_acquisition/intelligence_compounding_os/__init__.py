"""Data & Intelligence Compounding — safe operating learning layer."""

from __future__ import annotations

from auto_client_acquisition.intelligence_compounding_os.arabic_quality_patterns import (
    ARABIC_INTELLIGENCE_DIMENSIONS,
    arabic_intelligence_coverage_score,
)
from auto_client_acquisition.intelligence_compounding_os.benchmark_candidates import (
    BENCHMARK_CANDIDATE_SLUGS,
    benchmark_candidate_eligible,
)
from auto_client_acquisition.intelligence_compounding_os.client_intelligence import (
    CLIENT_INTELLIGENCE_METRICS,
    client_intelligence_coverage_score,
)
from auto_client_acquisition.intelligence_compounding_os.data_intelligence import (
    DATA_PATTERN_TYPES,
    data_pattern_actionable,
    pattern_confidence_band,
)
from auto_client_acquisition.intelligence_compounding_os.decision_engine import (
    CompoundingDecision,
    suggest_compounding_decision,
)
from auto_client_acquisition.intelligence_compounding_os.event_collector import (
    INTELLIGENCE_EVENT_STREAMS,
    intelligence_event_stream_valid,
)
from auto_client_acquisition.intelligence_compounding_os.governance_intelligence import (
    GOVERNANCE_INTELLIGENCE_SIGNALS,
    governance_intelligence_coverage_score,
)
from auto_client_acquisition.intelligence_compounding_os.intelligence_dashboard import (
    INTELLIGENCE_DASHBOARD_SIGNALS,
    intelligence_dashboard_coverage_score,
)
from auto_client_acquisition.intelligence_compounding_os.intelligence_quality import (
    INTELLIGENCE_QUALITY_CONTROLS,
    intelligence_quality_controls_met,
)
from auto_client_acquisition.intelligence_compounding_os.market_intelligence import (
    MARKET_SIGNAL_SOURCES,
    MarketSignalRecord,
    market_pattern_actionable_repeats,
    market_signal_record_valid,
)
from auto_client_acquisition.intelligence_compounding_os.product_intelligence import (
    PRODUCT_SIGNAL_SOURCES,
    ProductIntelligenceVerdict,
    product_intelligence_verdict,
)
from auto_client_acquisition.intelligence_compounding_os.workflow_intelligence import (
    WORKFLOW_INTELLIGENCE_SIGNALS,
    workflow_productization_candidate,
)

__all__ = (
    "ARABIC_INTELLIGENCE_DIMENSIONS",
    "BENCHMARK_CANDIDATE_SLUGS",
    "CLIENT_INTELLIGENCE_METRICS",
    "DATA_PATTERN_TYPES",
    "GOVERNANCE_INTELLIGENCE_SIGNALS",
    "INTELLIGENCE_DASHBOARD_SIGNALS",
    "INTELLIGENCE_EVENT_STREAMS",
    "INTELLIGENCE_QUALITY_CONTROLS",
    "MARKET_SIGNAL_SOURCES",
    "PRODUCT_SIGNAL_SOURCES",
    "WORKFLOW_INTELLIGENCE_SIGNALS",
    "CompoundingDecision",
    "MarketSignalRecord",
    "ProductIntelligenceVerdict",
    "arabic_intelligence_coverage_score",
    "benchmark_candidate_eligible",
    "client_intelligence_coverage_score",
    "data_pattern_actionable",
    "governance_intelligence_coverage_score",
    "intelligence_dashboard_coverage_score",
    "intelligence_event_stream_valid",
    "intelligence_quality_controls_met",
    "market_pattern_actionable_repeats",
    "market_signal_record_valid",
    "pattern_confidence_band",
    "product_intelligence_verdict",
    "suggest_compounding_decision",
    "workflow_productization_candidate",
)
