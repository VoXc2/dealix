"""ROI attribution — connect recorded value to an enterprise engagement.

The Executive Console headline: for a transformation program, aggregate the
value-ledger events into an investment-vs-value picture so leadership sees
the ROI of the engagement.

Tier discipline is preserved end to end: estimated value is reported
separately from observed/verified and is NEVER folded into the headline
realized figure. Every number is an estimate until client-confirmed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from auto_client_acquisition.value_os.value_ledger import list_events


@dataclass
class ExecutiveROISummary:
    customer_id: str
    program_run_id: str
    investment_sar: float          # setup + retainer months committed
    estimated_value_sar: float     # modelled — not claimable
    observed_value_sar: float      # seen in workflow
    realized_value_sar: float      # verified + client_confirmed only
    roi_ratio_realized: float      # realized / investment
    roi_ratio_with_observed: float  # (realized + observed) / investment
    event_count: int
    by_tier: dict[str, dict[str, Any]] = field(default_factory=dict)
    governance_decision: str = "allow_with_review"
    is_estimate: bool = True
    disclaimer: str = (
        "Estimated value is not realized value /"
        " القيمة التقديرية ليست قيمة مُتحقَّقة"
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _round(x: float) -> float:
    return round(float(x), 2)


def attribute_roi(
    *,
    customer_id: str,
    program_run_id: str = "",
    investment_sar: float = 0.0,
    period_days: int = 365,
) -> ExecutiveROISummary:
    """Aggregate the value ledger into an engagement ROI summary.

    ``investment_sar`` is the engagement cost (setup + committed retainer);
    pass 0 to get the value picture without a ratio.
    """
    events = list_events(customer_id=customer_id, period_days=period_days)

    by_tier: dict[str, dict[str, Any]] = {}
    estimated = observed = verified = client_confirmed = 0.0
    for ev in events:
        bucket = by_tier.setdefault(ev.tier, {"count": 0, "total_amount": 0.0})
        bucket["count"] += 1
        bucket["total_amount"] = _round(bucket["total_amount"] + ev.amount)
        if ev.tier == "estimated":
            estimated += ev.amount
        elif ev.tier == "observed":
            observed += ev.amount
        elif ev.tier == "verified":
            verified += ev.amount
        elif ev.tier == "client_confirmed":
            client_confirmed += ev.amount

    realized = verified + client_confirmed
    inv = max(0.0, float(investment_sar))
    roi_realized = _round(realized / inv) if inv > 0 else 0.0
    roi_with_observed = _round((realized + observed) / inv) if inv > 0 else 0.0

    return ExecutiveROISummary(
        customer_id=customer_id,
        program_run_id=program_run_id,
        investment_sar=_round(inv),
        estimated_value_sar=_round(estimated),
        observed_value_sar=_round(observed),
        realized_value_sar=_round(realized),
        roi_ratio_realized=roi_realized,
        roi_ratio_with_observed=roi_with_observed,
        event_count=len(events),
        by_tier=by_tier,
    )


def program_investment_sar(offering_id: str, tier_id: str, months: int = 12) -> float:
    """Total committed investment for a program tier: setup + N retainer months."""
    from auto_client_acquisition.service_catalog import get_enterprise_tier

    tier = get_enterprise_tier(offering_id, tier_id)
    if tier is None:
        return 0.0
    return _round(tier.setup_sar + tier.monthly_sar * max(0, months))


__all__ = [
    "ExecutiveROISummary",
    "attribute_roi",
    "program_investment_sar",
]
