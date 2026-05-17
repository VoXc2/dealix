"""Revenue Autopilot funnel — stage model + forward-only transition rules.

This is the customer-facing funnel of the Revenue Autopilot. It is a
SEPARATE model from ``revenue_pipeline.stage_policy.PipelineStage`` (which
tracks narrow revenue truth). The two coexist by design.

Hard rules (founder doctrine, enforced by the forward map below):
  - no ``invoice_sent`` without ``scope_sent`` — invoice_sent's only
    predecessor is scope_sent.
  - no ``delivery_started`` without ``invoice_paid`` — delivery_started's
    only predecessor is invoice_paid.
  - no revenue counted before ``invoice_paid`` — see ``is_revenue_countable``.

Doctrine: docs/REVENUE_AUTOPILOT.md §5.
"""
from __future__ import annotations

from typing import Literal

FunnelStage = Literal[
    "new_lead",
    "qualified_A",
    "qualified_B",
    "nurture",
    "partner_candidate",
    "meeting_booked",
    "meeting_done",
    "scope_requested",
    "scope_sent",
    "invoice_sent",
    "invoice_paid",
    "delivery_started",
    "proof_pack_sent",
    "sprint_candidate",
    "retainer_candidate",
    "closed_lost",
]


# Allowed forward transitions. The funnel is forward-only; a wrongly
# advanced engagement is corrected by marking ``closed_lost``.
_FORWARD: dict[FunnelStage, set[FunnelStage]] = {
    "new_lead": {
        "qualified_A", "qualified_B", "nurture",
        "partner_candidate", "closed_lost",
    },
    "qualified_A": {"meeting_booked", "nurture", "closed_lost"},
    "qualified_B": {"meeting_booked", "nurture", "closed_lost"},
    "nurture": {"qualified_A", "qualified_B", "meeting_booked", "closed_lost"},
    "partner_candidate": {"meeting_booked", "closed_lost"},
    "meeting_booked": {"meeting_done", "closed_lost"},
    "meeting_done": {"scope_requested", "nurture", "closed_lost"},
    "scope_requested": {"scope_sent", "closed_lost"},
    "scope_sent": {"invoice_sent", "closed_lost"},
    "invoice_sent": {"invoice_paid", "closed_lost"},
    "invoice_paid": {"delivery_started", "closed_lost"},
    "delivery_started": {"proof_pack_sent", "closed_lost"},
    "proof_pack_sent": {"sprint_candidate", "retainer_candidate", "closed_lost"},
    "sprint_candidate": {"retainer_candidate", "closed_lost"},
    "retainer_candidate": {"closed_lost"},
    "closed_lost": set(),
}

# Stages at or after which real money has landed.
REVENUE_STAGES: frozenset[FunnelStage] = frozenset({
    "invoice_paid",
    "delivery_started",
    "proof_pack_sent",
    "sprint_candidate",
    "retainer_candidate",
})


def valid_transitions(stage: FunnelStage) -> set[FunnelStage]:
    """Stages reachable in one forward step from ``stage``."""
    return set(_FORWARD.get(stage, set()))


def advance_stage(current: FunnelStage, target: FunnelStage) -> FunnelStage:
    """Advance ``current`` → ``target``; raise ``ValueError`` if disallowed."""
    allowed = valid_transitions(current)
    if target not in allowed:
        raise ValueError(
            f"invalid funnel transition: {current!r} → {target!r}; "
            f"allowed: {sorted(allowed)}"
        )
    return target


def is_revenue_countable(stage: FunnelStage) -> bool:
    """True only once a paid invoice has landed (``invoice_paid`` or later)."""
    return stage in REVENUE_STAGES


__all__ = [
    "REVENUE_STAGES",
    "FunnelStage",
    "advance_stage",
    "is_revenue_countable",
    "valid_transitions",
]
