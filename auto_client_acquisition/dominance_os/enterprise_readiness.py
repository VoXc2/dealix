"""Enterprise readiness ladder (levels 1-5)."""

from __future__ import annotations

from enum import IntEnum


class EnterpriseReadinessLevel(IntEnum):
    L1_TRUST_PACK = 1
    L2_AUDITABILITY = 2
    L3_CONTROL = 3
    L4_ENTERPRISE_PLATFORM = 4
    L5_ENTERPRISE_AI_OS = 5


def infer_enterprise_readiness_level(
    *,
    has_trust_pack: bool = False,
    has_audit_trail: bool = False,
    has_policy_engine: bool = False,
    has_enterprise_platform_features: bool = False,
    has_ai_control_tower: bool = False,
) -> EnterpriseReadinessLevel:
    """Return the highest level fully achieved (sequential ladder)."""
    if not has_trust_pack:
        return EnterpriseReadinessLevel.L1_TRUST_PACK
    if not has_audit_trail:
        return EnterpriseReadinessLevel.L1_TRUST_PACK
    if not has_policy_engine:
        return EnterpriseReadinessLevel.L2_AUDITABILITY
    if not has_enterprise_platform_features:
        return EnterpriseReadinessLevel.L3_CONTROL
    if not has_ai_control_tower:
        return EnterpriseReadinessLevel.L4_ENTERPRISE_PLATFORM
    return EnterpriseReadinessLevel.L5_ENTERPRISE_AI_OS
