"""System 39 — Organizational Resilience Engine.

Reads agent-action failures/retries and derives a circuit-breaker state
so the organization survives chaos instead of collapsing under it.
Read-only — recommends failover, never executes it.
"""

from __future__ import annotations

from auto_client_acquisition.org_consciousness_os._common import read_agent_events
from auto_client_acquisition.org_consciousness_os.schemas import ResilienceSignal
from auto_client_acquisition.revenue_memory.event_store import EventStore

_DEFAULT_MAX_RETRIES = 2


def _circuit_state(failures: int, executed: int) -> str:
    total = failures + executed
    if total == 0:
        return "closed"
    ratio = failures / total
    if ratio >= 0.5:
        return "open"
    if ratio >= 0.2:
        return "half_open"
    return "closed"


def compute_resilience(
    *,
    customer_id: str,
    window_days: int = 30,
    store: EventStore | None = None,
) -> ResilienceSignal:
    """Synthesize a resilience signal for ``customer_id``."""
    events = read_agent_events(
        customer_id=customer_id,
        window_days=window_days,
        store=store,
        event_types=("agent.action_failed", "agent.action_rejected", "agent.action_executed"),
    )

    total_failures = 0
    executed = 0
    total_retries = 0
    retry_exhausted = 0
    by_action_type: dict[str, int] = {}

    for ev in events:
        if ev.event_type == "agent.action_executed":
            executed += 1
            continue
        # failed or rejected
        total_failures += 1
        action_type = str(ev.payload.get("action_type", "unknown"))
        by_action_type[action_type] = by_action_type.get(action_type, 0) + 1
        retries = int(ev.payload.get("retries", 0) or 0)
        total_retries += retries
        max_retries = int(
            ev.payload.get("max_retries", _DEFAULT_MAX_RETRIES) or _DEFAULT_MAX_RETRIES
        )
        if retries >= max_retries:
            retry_exhausted += 1

    state = _circuit_state(total_failures, executed)
    return ResilienceSignal(
        customer_id=customer_id,
        window_days=window_days,
        total_failures=total_failures,
        total_retries=total_retries,
        retry_exhausted=retry_exhausted,
        executed=executed,
        circuit_state=state,
        failover_recommended=state == "open",
        by_action_type=by_action_type,
    )


__all__ = ["compute_resilience"]
