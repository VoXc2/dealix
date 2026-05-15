"""Agent performance dashboard data layer — task 8 of the Agent OS.

Aggregates quality / latency / cost / compliance signals per agent from the
registry, the friction log, and (when available) the observability traces.
Pure read-only aggregation — never raises on missing observability data.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from auto_client_acquisition.agent_os.agent_registry import get_agent, list_agents
from auto_client_acquisition.agent_os.agent_status import AgentStatus

_FRICTION_PENALTY = 0.1
_HIGH_SEVERITY_PENALTY = 0.2


@dataclass(frozen=True, slots=True)
class AgentPerformanceSummary:
    agent_id: str
    status: str
    quality_score: float
    latency_ms_avg: float
    cost_estimate_total: float
    compliance_ok: bool
    friction_count: int
    trace_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _agent_friction(agent_id: str, customer_id: str, window_days: int) -> list[Any]:
    try:
        from auto_client_acquisition.friction_log import list_events
    except ImportError:
        return []
    events = list_events(customer_id=customer_id, since_days=window_days, limit=500)
    return [e for e in events if getattr(e, "workflow_id", "") == agent_id]


def _agent_traces(agent_id: str) -> list[Any]:
    try:
        from auto_client_acquisition.agent_observability import list_recent_traces
    except ImportError:
        return []
    try:
        traces = list_recent_traces(limit=500)
    except Exception:
        return []
    return [t for t in traces if getattr(t, "agent_name", "") == agent_id]


def summarize_agent(
    agent_id: str,
    *,
    customer_id: str = "dealix_internal",
    window_days: int = 30,
) -> AgentPerformanceSummary | None:
    """Build a performance summary for one agent, or None if unregistered."""
    card = get_agent(agent_id)
    if card is None:
        return None

    friction = _agent_friction(agent_id, customer_id, window_days)
    high_sev = [e for e in friction if getattr(e, "severity", "") == "high"]
    traces = _agent_traces(agent_id)

    quality = 1.0
    quality -= _FRICTION_PENALTY * len(friction)
    quality -= _HIGH_SEVERITY_PENALTY * len(high_sev)
    quality = round(max(0.0, min(1.0, quality)), 4)

    latencies = [t.latency_ms for t in traces if getattr(t, "latency_ms", None) is not None]
    latency_avg = round(sum(latencies) / len(latencies), 2) if latencies else 0.0
    cost_total = round(
        sum(t.cost_estimate or 0.0 for t in traces if getattr(t, "cost_estimate", None) is not None),
        6,
    )

    compliance_ok = card.status != AgentStatus.KILLED.value and not high_sev

    return AgentPerformanceSummary(
        agent_id=agent_id,
        status=card.status,
        quality_score=quality,
        latency_ms_avg=latency_avg,
        cost_estimate_total=cost_total,
        compliance_ok=compliance_ok,
        friction_count=len(friction),
        trace_count=len(traces),
    )


def summarize_all(
    *,
    customer_id: str = "dealix_internal",
    window_days: int = 30,
) -> list[AgentPerformanceSummary]:
    """Performance summaries for every registered agent."""
    out: list[AgentPerformanceSummary] = []
    for card in list_agents():
        summary = summarize_agent(
            card.agent_id,
            customer_id=customer_id,
            window_days=window_days,
        )
        if summary is not None:
            out.append(summary)
    return out


__all__ = [
    "AgentPerformanceSummary",
    "summarize_agent",
    "summarize_all",
]
