"""Enterprise Readiness — five-level ladder, sell what you operate.

See ``docs/command_control/ENTERPRISE_READINESS.md`` and
``docs/global_grade/ENTERPRISE_READINESS_LADDER.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class ReadinessLevel(IntEnum):
    LEVEL_1_TRUST_PACK = 1
    LEVEL_2_AUDITABILITY = 2
    LEVEL_3_CONTROL = 3
    LEVEL_4_ENTERPRISE_PLATFORM = 4
    LEVEL_5_ENTERPRISE_AI_OS = 5


@dataclass(frozen=True)
class ReadinessRequirement:
    level: ReadinessLevel
    requirements: tuple[str, ...]


READINESS_LEVELS: tuple[ReadinessRequirement, ...] = (
    ReadinessRequirement(
        level=ReadinessLevel.LEVEL_1_TRUST_PACK,
        requirements=(
            "documented_data_handling",
            "ai_policy_in_writing",
            "no_unsafe_automation_offered",
            "proof_pack_format_in_use",
        ),
    ),
    ReadinessRequirement(
        level=ReadinessLevel.LEVEL_2_AUDITABILITY,
        requirements=(
            "structured_audit_events",
            "ai_run_ledger_active",
            "approval_records_persisted",
            "source_passports_for_every_dataset",
        ),
    ),
    ReadinessRequirement(
        level=ReadinessLevel.LEVEL_3_CONTROL,
        requirements=(
            "policy_engine_deployed",
            "role_based_approvals",
            "risk_index_per_agent",
            "incident_response_runbook",
        ),
    ),
    ReadinessRequirement(
        level=ReadinessLevel.LEVEL_4_ENTERPRISE_PLATFORM,
        requirements=(
            "rbac",
            "sso",
            "configurable_data_retention",
            "audit_exports",
            "sla_uptime_and_approval_latency",
            "defined_support_process",
        ),
    ),
    ReadinessRequirement(
        level=ReadinessLevel.LEVEL_5_ENTERPRISE_AI_OS,
        requirements=(
            "ai_control_tower",
            "multi_workflow_governance",
            "business_unit_reporting",
            "executive_value_dashboard",
        ),
    ),
)


def can_sell_level(
    target: ReadinessLevel,
    *,
    operated_requirements: frozenset[str],
) -> tuple[bool, tuple[str, ...]]:
    """Determine whether Dealix may sell ``target`` given current operation.

    Doctrine: sell what you can operate at the previous level. The check
    requires every requirement up to ``target - 1`` to be present.
    """

    needed: list[str] = []
    for entry in READINESS_LEVELS:
        if entry.level >= target:
            break
        needed.extend(entry.requirements)
    missing = tuple(r for r in needed if r not in operated_requirements)
    return (not missing, missing)
