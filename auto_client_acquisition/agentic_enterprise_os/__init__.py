"""Agentic Enterprise OS — the unifying layer over the 12 core systems.

نظام تشغيل المؤسسة الوكيلة — الطبقة الموحِّدة فوق الأنظمة الأساسية الـ12.

Capstone: the Enterprise Maturity System (10-capability scorecard) and the
12-system coverage registry. Gap fills: a unified evaluation harness, a
continuous-evolution loop, and a unified Agent OS view. The maturity index is
wired into the commercial service ladder via ``service_ladder``.
"""

from auto_client_acquisition.agentic_enterprise_os.coverage_registry import (
    CORE_SYSTEMS,
    CoreSystemSpec,
    SystemCoverage,
    coverage_registry,
    coverage_summary,
    module_coverage,
)
from auto_client_acquisition.agentic_enterprise_os.enterprise_maturity import (
    EnterpriseCapabilityScores,
    MaturityStage,
    compute_emi,
    enterprise_maturity_stage,
)
from auto_client_acquisition.agentic_enterprise_os.enterprise_scorecard import (
    EnterpriseScorecard,
    build_enterprise_scorecard,
)
from auto_client_acquisition.agentic_enterprise_os.evaluation_harness import (
    EVAL_DIMENSIONS,
    EvalDimensionResult,
    EvaluationReport,
    run_evaluation_harness,
)
from auto_client_acquisition.agentic_enterprise_os.evolution_loop import (
    EvolutionLoopResult,
    EvolutionRecommendation,
    FrictionEntry,
    run_evolution_loop,
)
from auto_client_acquisition.agentic_enterprise_os.service_ladder import (
    emi_to_ladder_level,
    enterprise_offer_recommendation,
)
from auto_client_acquisition.agentic_enterprise_os.unified_agent_view import (
    UnifiedAgentView,
    build_unified_agent_view,
    list_unified_agent_views,
)

__all__ = [
    "CORE_SYSTEMS",
    "EVAL_DIMENSIONS",
    "CoreSystemSpec",
    "EnterpriseCapabilityScores",
    "EnterpriseScorecard",
    "EvalDimensionResult",
    "EvaluationReport",
    "EvolutionLoopResult",
    "EvolutionRecommendation",
    "FrictionEntry",
    "MaturityStage",
    "SystemCoverage",
    "UnifiedAgentView",
    "build_enterprise_scorecard",
    "build_unified_agent_view",
    "compute_emi",
    "coverage_registry",
    "coverage_summary",
    "emi_to_ladder_level",
    "enterprise_maturity_stage",
    "enterprise_offer_recommendation",
    "list_unified_agent_views",
    "module_coverage",
    "run_evaluation_harness",
    "run_evolution_loop",
]
