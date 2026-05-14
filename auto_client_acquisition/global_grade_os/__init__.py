"""Global-grade operating model — enterprise-ready scoring and trust ladder."""

from __future__ import annotations

from auto_client_acquisition.global_grade_os.agent_governance import (
    AGENT_MVP_RULE,
    describe_agent_policy,
)
from auto_client_acquisition.global_grade_os.capability_index import (
    CAPABILITY_LEVELS,
    CapabilityDimension,
    CapabilityIndexProfile,
    average_capability_level,
)
from auto_client_acquisition.global_grade_os.enterprise_trust import (
    ENTERPRISE_TRUST_LADDER,
    highest_satisfied_trust_level,
    trust_level_satisfied,
)
from auto_client_acquisition.global_grade_os.market_power_score import (
    MARKET_POWER_SIGNALS,
    market_power_activation_score,
)
from auto_client_acquisition.global_grade_os.runtime_governance_product import (
    GOVERNANCE_RUNTIME_COMPONENTS,
    GovernanceDecision,
    governance_runtime_maturity_score,
)
from auto_client_acquisition.global_grade_os.transformation_gap import (
    TransformationDecision,
    transformation_decision,
)

__all__ = [
    "AGENT_MVP_RULE",
    "CAPABILITY_LEVELS",
    "ENTERPRISE_TRUST_LADDER",
    "GOVERNANCE_RUNTIME_COMPONENTS",
    "MARKET_POWER_SIGNALS",
    "CapabilityDimension",
    "CapabilityIndexProfile",
    "GovernanceDecision",
    "TransformationDecision",
    "average_capability_level",
    "describe_agent_policy",
    "governance_runtime_maturity_score",
    "highest_satisfied_trust_level",
    "market_power_activation_score",
    "transformation_decision",
    "trust_level_satisfied",
]
