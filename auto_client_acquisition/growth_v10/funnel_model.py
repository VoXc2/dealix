"""Funnel model — derive stage transitions + conversion rates from events."""
from __future__ import annotations

from auto_client_acquisition.growth_v10.schemas import (
    EventName,
    EventRecord,
    FunnelReport,
    FunnelStage,
    FunnelStep,
)

# Transition rules: (from, to, triggering_event)
_STAGE_TRANSITIONS: list[tuple[FunnelStage, FunnelStage, EventName]] = [
    (FunnelStage.VISITOR, FunnelStage.LEAD, EventName.LEAD_CREATED),
    (FunnelStage.LEAD, FunnelStage.QUALIFIED, EventName.SERVICE_RECOMMENDED),
    (FunnelStage.QUALIFIED, FunnelStage.DIAGNOSTIC_DELIVERED, EventName.DIAGNOSTIC_DELIVERED),
    (FunnelStage.DIAGNOSTIC_DELIVERED, FunnelStage.PILOT_OFFERED, EventName.PROPOSAL_CREATED),
    (FunnelStage.PILOT_OFFERED, FunnelStage.PAID_OR_COMMITTED, EventName.PAYMENT_REQUESTED_MANUAL),
    (FunnelStage.PAID_OR_COMMITTED, FunnelStage.PROOF_DELIVERED, EventName.PROOF_PACK_GENERATED),
]


def _event_value(name) -> str:
    return name.value if hasattr(name, "value") else str(name)


def compute_funnel(events: list[EventRecord]) -> FunnelReport:
    """Aggregate events into stage transitions + conversion rates.

    Each customer_handle counted once per stage. Conversion rate is
    transitions / origin-stage-count (clamped 0..1).
    """
    # Group events by customer_handle.
    by_handle: dict[str, set[str]] = {}
    for ev in events:
        handle = ev.customer_handle
        ev_name = _event_value(ev.name)
        by_handle.setdefault(handle, set()).add(ev_name)

    # Stage occupancy by handle (if a handle ever hit a stage's triggering event).
    stage_occupants: dict[str, set[str]] = {s.value: set() for s in FunnelStage}
    # All known handles count as visitors.
    for handle in by_handle:
        stage_occupants[FunnelStage.VISITOR.value].add(handle)

    for from_stage, to_stage, trigger in _STAGE_TRANSITIONS:
        trigger_value = trigger.value
        for handle, names in by_handle.items():
            if trigger_value in names:
                stage_occupants[to_stage.value].add(handle)

    steps: list[FunnelStep] = []
    for from_stage, to_stage, _ in _STAGE_TRANSITIONS:
        from_count = len(stage_occupants[from_stage.value])
        to_count = len(stage_occupants[to_stage.value])
        if from_count == 0:
            rate = 0.0
        else:
            rate = max(0.0, min(1.0, to_count / from_count))
        steps.append(FunnelStep(
            from_stage=from_stage,
            to_stage=to_stage,
            count=to_count,
            conversion_rate=round(rate, 4),
        ))

    return FunnelReport(
        stages=steps,
        total_visitors=len(stage_occupants[FunnelStage.VISITOR.value]),
        total_paid=len(stage_occupants[FunnelStage.PAID_OR_COMMITTED.value]),
    )
