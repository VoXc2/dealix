"""The 5 verification systems — proof that the platform is real, not a demo.

A high gate score with low verification coverage means the platform *claims*
capability it has not proven. The maturity engine blocks stage promotion on it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VerificationSystem:
    system_id: str
    name_en: str
    name_ar: str
    checks: tuple[str, ...]


VERIFICATION_SYSTEMS: tuple[VerificationSystem, ...] = (
    VerificationSystem(
        system_id="real_workflow_testing",
        name_en="Real Workflow Testing",
        name_ar="اختبار workflows حقيقية",
        checks=(
            "full_workflows_tested",
            "approvals_tested",
            "failures_and_retries_tested",
            "escalations_tested",
            "edge_cases_tested",
        ),
    ),
    VerificationSystem(
        system_id="governance_validation",
        name_en="Governance Validation",
        name_ar="التحقق من الحوكمة",
        checks=(
            "approvals_enforced",
            "permissions_correct",
            "audit_logs_complete",
            "policies_respected",
            "agents_stay_in_bounds",
        ),
    ),
    VerificationSystem(
        system_id="operational_evaluations",
        name_en="Operational Evaluations",
        name_ar="التقييمات التشغيلية",
        checks=(
            "ai_quality_measured",
            "grounding_measured",
            "workflow_completion_measured",
            "escalation_correctness_measured",
            "business_quality_measured",
        ),
    ),
    VerificationSystem(
        system_id="enterprise_readiness_gates",
        name_en="Enterprise Readiness Gates",
        name_ar="بوابات الجاهزية المؤسسية",
        checks=(
            "every_service_has_gate_scores",
            "gate_thresholds_enforced",
            "gate_evidence_recorded",
        ),
    ),
    VerificationSystem(
        system_id="executive_proof",
        name_en="Executive Proof System",
        name_ar="نظام الإثبات التنفيذي",
        checks=(
            "revenue_increase_proven",
            "time_reduction_proven",
            "operations_improvement_proven",
            "approval_speedup_proven",
            "organizational_leverage_proven",
        ),
    ),
)

_BY_ID: dict[str, VerificationSystem] = {v.system_id: v for v in VERIFICATION_SYSTEMS}
VERIFICATION_SYSTEM_IDS: tuple[str, ...] = tuple(_BY_ID.keys())


def verification_system(system_id: str) -> VerificationSystem | None:
    return _BY_ID.get(system_id)


def verification_coverage(system_id: str, met_checks: dict[str, bool] | None = None) -> int:
    """Percentage 0–100 of a system's checks that are met. Equal weight per check."""
    system = _BY_ID[system_id]
    met = met_checks or {}
    passed = sum(1 for c in system.checks if met.get(c, False))
    return round(100 * passed / len(system.checks))


__all__ = [
    "VERIFICATION_SYSTEMS",
    "VERIFICATION_SYSTEM_IDS",
    "VerificationSystem",
    "verification_coverage",
    "verification_system",
]
