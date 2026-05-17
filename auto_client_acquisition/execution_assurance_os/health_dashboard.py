"""Full Ops Health dashboard — one read-only view over every machine.

Combines the maturity scorecard, Definition-of-Done completion, acceptance
gates, and the 10 portfolio KPIs into a single structure for the API and
the CEO review. Degrades gracefully on empty data; never raises.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.execution_assurance_os.definition_of_done import (
    evaluate_acceptance_gate,
    evaluate_dod,
)
from auto_client_acquisition.execution_assurance_os.registry import (
    MachineRegistry,
)
from auto_client_acquisition.execution_assurance_os.scorecard import (
    aggregate_score,
    score_machine,
)

# The 10 portfolio KPIs the founder reviews. `current` stays None until a
# machine is instrumented to report it — an honest "not measured yet".
FULL_OPS_HEALTH_KPIS: tuple[dict[str, str], ...] = (
    {"name": "lead_capture_success_rate", "target": "95%+", "machine": "sales_autopilot"},
    {"name": "lead_scoring_coverage", "target": "100%", "machine": "sales_autopilot"},
    {"name": "qualified_lead_response_time", "target": "<24h", "machine": "sales_autopilot"},
    {"name": "meeting_brief_generation_rate", "target": "100%", "machine": "sales_autopilot"},
    {"name": "scope_to_invoice_conversion", "target": "tracked", "machine": "billing_ops"},
    {"name": "invoice_to_paid_conversion", "target": "tracked", "machine": "billing_ops"},
    {"name": "support_auto_resolution_rate", "target": "40-60%", "machine": "support_autopilot"},
    {"name": "support_escalation_accuracy", "target": "100%", "machine": "support_autopilot"},
    {"name": "approval_compliance_rate", "target": "100%", "machine": "governance_layer"},
    {"name": "evidence_completeness_score", "target": "90%+", "machine": "evidence_ledger"},
)

# The single most important KPI: any non-zero value is a trust failure.
CRITICAL_KPI: dict[str, str] = {
    "name": "high_risk_auto_send",
    "target": "0%",
    "rule": "any non-zero value is a trust failure — investigate immediately",
}

_HARD_GATES: dict[str, bool] = {
    "no_fake_green": True,
    "maturity_attested_in_registry": True,
    "read_only": True,
    "every_score_traceable_to_dod": True,
}


@dataclass(frozen=True, slots=True)
class FullOpsHealth:
    """The complete Full Ops Health view."""

    generated_at: str
    portfolio: dict[str, Any]
    machine_rows: tuple[dict[str, Any], ...]
    kpis: tuple[dict[str, Any], ...]
    critical_kpi: dict[str, str]
    hard_gates: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "portfolio": self.portfolio,
            "machine_rows": list(self.machine_rows),
            "kpis": list(self.kpis),
            "critical_kpi": self.critical_kpi,
            "hard_gates": self.hard_gates,
        }


def build_full_ops_health(reg: MachineRegistry) -> FullOpsHealth:
    """Build the Full Ops Health dashboard from the registry."""
    rows: list[dict[str, Any]] = []
    for spec in reg.machines:
        score = score_machine(spec)
        dod = evaluate_dod(spec)
        gate = evaluate_acceptance_gate(spec)
        rows.append(
            {
                "machine_id": spec.id,
                "name": spec.name,
                "owner": spec.owner,
                "maturity": score.declared_score,
                "level": score.declared_level,
                "target": score.target_score,
                "gap_to_target": score.gap_to_target,
                "dod_pct": dod.pct,
                "dod_met": f"{dod.items_met}/{dod.items_total}",
                "gate_passed": gate.passed,
                "consistency": score.consistency,
                "top_failure_mode": (
                    spec.failure_modes[0] if spec.failure_modes else None
                ),
            }
        )

    kpis = [
        {**kpi, "current": None, "status": "not_measured"}
        for kpi in FULL_OPS_HEALTH_KPIS
    ]

    return FullOpsHealth(
        generated_at=datetime.now(UTC).isoformat(),
        portfolio=aggregate_score(reg).to_dict(),
        machine_rows=tuple(rows),
        kpis=tuple(kpis),
        critical_kpi=CRITICAL_KPI,
        hard_gates=_HARD_GATES,
    )


__all__ = [
    "CRITICAL_KPI",
    "FULL_OPS_HEALTH_KPIS",
    "FullOpsHealth",
    "build_full_ops_health",
]
