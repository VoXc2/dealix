"""Goal / KPI schema per agent — task 4 of the Agent Operating System.

Every agent declares both an *output* metric (what it produces) and a
*business-impact* metric (why it matters). Doctrine: no AI without a
workflow-anchored outcome.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AgentKPI:
    agent_id: str
    output_metric: str
    output_target: float
    business_impact_metric: str
    business_impact_target: float
    window_days: int = 30

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class KPIValidation:
    ok: bool
    issues: tuple[str, ...]


def new_kpi(
    *,
    agent_id: str,
    output_metric: str,
    output_target: float,
    business_impact_metric: str,
    business_impact_target: float,
    window_days: int = 30,
) -> AgentKPI:
    """Build a validated KPI. Raises ValueError on any structural problem."""
    if not agent_id.strip():
        raise ValueError("agent_id is required")
    if not output_metric.strip():
        raise ValueError("output_metric is required")
    if not business_impact_metric.strip():
        raise ValueError("business_impact_metric is required")
    if output_metric.strip().lower() == business_impact_metric.strip().lower():
        raise ValueError("output_metric must differ from business_impact_metric")
    if output_target <= 0 or business_impact_target <= 0:
        raise ValueError("targets must be positive")
    if window_days <= 0:
        raise ValueError("window_days must be positive")
    return AgentKPI(
        agent_id=agent_id.strip(),
        output_metric=output_metric.strip(),
        output_target=float(output_target),
        business_impact_metric=business_impact_metric.strip(),
        business_impact_target=float(business_impact_target),
        window_days=int(window_days),
    )


def validate_kpi(kpi: AgentKPI) -> KPIValidation:
    """Non-raising validation — returns the list of issues found."""
    issues: list[str] = []
    if not kpi.output_metric.strip():
        issues.append("blank_output_metric")
    if not kpi.business_impact_metric.strip():
        issues.append("blank_business_impact_metric")
    if kpi.output_metric.strip().lower() == kpi.business_impact_metric.strip().lower():
        issues.append("output_metric_equals_business_impact_metric")
    if kpi.output_target <= 0 or kpi.business_impact_target <= 0:
        issues.append("non_positive_target")
    if kpi.window_days <= 0:
        issues.append("non_positive_window")
    return KPIValidation(ok=not issues, issues=tuple(issues))


def kpi_attainment(
    kpi: AgentKPI,
    *,
    output_actual: float,
    business_impact_actual: float,
) -> dict[str, Any]:
    """Compute attainment ratios against the declared targets."""
    return {
        "agent_id": kpi.agent_id,
        "output_attainment": round(output_actual / kpi.output_target, 4),
        "business_impact_attainment": round(
            business_impact_actual / kpi.business_impact_target, 4,
        ),
        "window_days": kpi.window_days,
    }


__all__ = [
    "AgentKPI",
    "KPIValidation",
    "kpi_attainment",
    "new_kpi",
    "validate_kpi",
]
