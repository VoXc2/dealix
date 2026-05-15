"""System 41 — Operational Value Engine.

Synthesizes ROI / impact from validated value- and capital-ledger events
against the friction cost in the same window. Value/capital ledgers have
no store, so events are passed in by the caller. Always an estimate.
"""

from __future__ import annotations

from auto_client_acquisition.capital_os.capital_ledger import (
    CapitalLedgerEvent,
    capital_ledger_event_valid,
)
from auto_client_acquisition.friction_log.aggregator import aggregate as friction_aggregate
from auto_client_acquisition.org_consciousness_os.schemas import OperationalValueSignal
from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

# Bilingual disclaimer — estimates are never presented as verified outcomes.
_DISCLAIMER = "تقدير تشغيلي وليس نتيجة موثّقة. | " "Operational estimate, not a verified outcome."


def compute_operational_value(
    *,
    customer_id: str,
    value_events: list[ValueLedgerEvent] | None = None,
    capital_events: list[CapitalLedgerEvent] | None = None,
    friction_window_days: int = 30,
) -> OperationalValueSignal:
    """Synthesize an operational-value signal for ``customer_id``."""
    value_events = value_events or []
    capital_events = capital_events or []

    valid_value = [e for e in value_events if value_ledger_event_valid(e)]
    valid_capital = [e for e in capital_events if capital_ledger_event_valid(e)]

    metric_delta = sum(e.after - e.before for e in valid_value)

    agg = friction_aggregate(customer_id=customer_id, window_days=friction_window_days)
    friction_cost = agg.total_cost_minutes
    roi_ratio = round(metric_delta / max(1, friction_cost), 3)

    summary = (
        f"{len(valid_value)} verified value event(s), "
        f"{len(valid_capital)} capital asset(s); metric delta {metric_delta} "
        f"against {friction_cost} friction minutes. {_DISCLAIMER}"
    )

    return OperationalValueSignal(
        customer_id=customer_id,
        value_events_count=len(value_events),
        capital_events_count=len(capital_events),
        valid_value_events=len(valid_value),
        valid_capital_events=len(valid_capital),
        value_metric_delta=metric_delta,
        friction_cost_minutes=friction_cost,
        roi_ratio=roi_ratio,
        impact_summary=summary,
        is_estimate=True,
    )


__all__ = ["compute_operational_value"]
