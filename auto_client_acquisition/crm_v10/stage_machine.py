"""Stage transition rules for Lead and Deal objects."""
from __future__ import annotations

from auto_client_acquisition.crm_v10.schemas import Deal, Lead

LEAD_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "new": ("qualifying", "disqualified"),
    "qualifying": ("qualified", "disqualified"),
    "qualified": ("converted", "disqualified"),
    "disqualified": (),
    "converted": (),
}


DEAL_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "pilot_offered": ("payment_pending", "lost"),
    "payment_pending": ("paid_or_committed", "lost"),
    "paid_or_committed": ("in_delivery", "lost"),
    "in_delivery": ("won", "lost"),
    "won": (),
    "lost": (),
}


class InvalidStageTransition(ValueError):  # noqa: N818 - public API name
    """Raised when a stage advance is not allowed by the state machine."""


def advance_lead(lead: Lead, target_stage: str) -> Lead:
    allowed = LEAD_TRANSITIONS.get(lead.stage, ())
    if target_stage not in allowed:
        raise InvalidStageTransition(
            f"lead stage {lead.stage!r} cannot advance to {target_stage!r}; "
            f"allowed: {list(allowed)}"
        )
    return lead.model_copy(update={"stage": target_stage})


def advance_deal(deal: Deal, target_stage: str) -> Deal:
    allowed = DEAL_TRANSITIONS.get(deal.stage, ())
    if target_stage not in allowed:
        raise InvalidStageTransition(
            f"deal stage {deal.stage!r} cannot advance to {target_stage!r}; "
            f"allowed: {list(allowed)}"
        )
    return deal.model_copy(update={"stage": target_stage})


__all__ = [
    "DEAL_TRANSITIONS",
    "LEAD_TRANSITIONS",
    "InvalidStageTransition",
    "advance_deal",
    "advance_lead",
]
