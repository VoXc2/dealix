"""Dealix Sovereignty OS — typed surfaces of the sovereignty doctrine.

Companion docs live under ``docs/sovereignty/``. These modules encode
the sovereign disciplines that protect Dealix from single-provider,
single-tool, single-customer, and single-channel dependence.

All modules are dependency-free and side-effect-free.
"""

from __future__ import annotations

from auto_client_acquisition.sovereignty_os.agent_sovereignty import (
    SOVEREIGN_AGENT_MVP_LEVELS,
    SovereignAgentDecision,
    evaluate_sovereign_agent,
)
from auto_client_acquisition.sovereignty_os.capital_sovereignty import (
    CapitalReview,
    CapitalReviewQuestion,
    REQUIRED_CAPITAL_REVIEW_QUESTIONS,
    capital_review_pass,
)
from auto_client_acquisition.sovereignty_os.commercial_sovereignty import (
    RevenueLine,
    RevenueMix,
    RevenueRole,
    excessive_concentration,
)
from auto_client_acquisition.sovereignty_os.dependency_risk import (
    DEFAULT_DEPENDENCY_MAP,
    DependencyEntry,
    DependencyRiskMap,
    Severity,
    has_uncontrolled_dependencies,
)
from auto_client_acquisition.sovereignty_os.enterprise_sovereignty import (
    SovereignEnterpriseSale,
    can_sell_enterprise_level,
)
from auto_client_acquisition.sovereignty_os.model_router_strategy import (
    ModelClass,
    ModelRouterDecision,
    ModelRouterRequest,
    route_request,
)
from auto_client_acquisition.sovereignty_os.proof_sovereignty import (
    PROOF_PACK_REQUIRED_SECTIONS,
    SovereignProofPack,
    SovereignProofRule,
    proof_pack_complete,
)
from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    PassportStandardCheck,
    PassportValidation,
    validate_passport,
)

__all__ = [
    "SOVEREIGN_AGENT_MVP_LEVELS",
    "SovereignAgentDecision",
    "evaluate_sovereign_agent",
    "CapitalReview",
    "CapitalReviewQuestion",
    "REQUIRED_CAPITAL_REVIEW_QUESTIONS",
    "capital_review_pass",
    "RevenueLine",
    "RevenueMix",
    "RevenueRole",
    "excessive_concentration",
    "DEFAULT_DEPENDENCY_MAP",
    "DependencyEntry",
    "DependencyRiskMap",
    "Severity",
    "has_uncontrolled_dependencies",
    "SovereignEnterpriseSale",
    "can_sell_enterprise_level",
    "ModelClass",
    "ModelRouterDecision",
    "ModelRouterRequest",
    "route_request",
    "PROOF_PACK_REQUIRED_SECTIONS",
    "SovereignProofPack",
    "SovereignProofRule",
    "proof_pack_complete",
    "PassportStandardCheck",
    "PassportValidation",
    "validate_passport",
]
