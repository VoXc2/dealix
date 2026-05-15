"""Execution OS — gates, scorecards, event→decision, capital review, expansion, anti-patterns."""

from __future__ import annotations

from auto_client_acquisition.execution_os.anti_patterns import (
    AntiPatternSignal,
    ExecutionAntiPattern,
    detect_anti_patterns,
)
from auto_client_acquisition.execution_os.capital_review import (
    CapitalReviewOutputs,
    capital_review_complete,
)
from auto_client_acquisition.execution_os.event_to_decision import (
    ExecutionDecision,
    recommend_decisions,
)
from auto_client_acquisition.execution_os.expansion_engine import (
    ExpansionEntry,
    expansion_path,
)
from auto_client_acquisition.execution_os.gates import (
    ExecutionGate,
    GateResult,
    all_gates_pass,
    evaluate_gate,
)
from auto_client_acquisition.execution_os.scorecards import (
    EXECUTION_OUTPUT_BUCKETS,
    ExecutionWorkTier,
    ProjectScorecard,
    average_project_score,
    execution_work_tier,
)

__all__ = [
    "EXECUTION_OUTPUT_BUCKETS",
    "AntiPatternSignal",
    "CapitalReviewOutputs",
    "ExecutionAntiPattern",
    "ExecutionDecision",
    "ExecutionGate",
    "ExecutionWorkTier",
    "ExpansionEntry",
    "GateResult",
    "ProjectScorecard",
    "all_gates_pass",
    "average_project_score",
    "capital_review_complete",
    "detect_anti_patterns",
    "evaluate_gate",
    "execution_work_tier",
    "expansion_path",
    "recommend_decisions",
]
