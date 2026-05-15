"""Monthly Value Report — cadence-driven brief mirroring qbr_generator's
markdown pattern.

Pulls from value_ledger, friction_log aggregator, proof_ledger events,
adoption_score. Markdown always emits the bilingual disclaimer and a
"## Limitations" section.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from typing import Any

from auto_client_acquisition.client_os.badges import ProofBadge
from auto_client_acquisition.friction_log.aggregator import aggregate as aggregate_friction
from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision
from auto_client_acquisition.value_os.value_ledger import ValueEvent
from auto_client_acquisition.value_os.value_ledger import list_events as list_value_events

BILINGUAL_DISCLAIMER = (
    "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"
)


def _month_bounds(month: str | None) -> tuple[str, str, str]:
    now = datetime.now(UTC)
    if month:
        year, mo = month.split("-")
        start = datetime(int(year), int(mo), 1, tzinfo=UTC)
    else:
        start = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
    # End of month (exclusive).
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    month_label = start.strftime("%Y-%m")
    return month_label, start.isoformat(), (end - timedelta(seconds=1)).isoformat()


@dataclass
class MonthlyValueReport:
    customer_id: str
    month: str
    period_start: str
    period_end: str
    estimated: list[dict[str, Any]] = field(default_factory=list)
    observed: list[dict[str, Any]] = field(default_factory=list)
    verified: list[dict[str, Any]] = field(default_factory=list)
    client_confirmed: list[dict[str, Any]] = field(default_factory=list)
    proof_events_count: int = 0
    blocked_unsafe_actions_count: int = 0
    adoption_progression: dict[str, float] = field(default_factory=dict)
    friction_summary: dict[str, Any] = field(default_factory=dict)
    limitations: list[str] = field(default_factory=list)
    governance_decision: str = GovernanceDecision.ALLOW_WITH_REVIEW.value
    generated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Monthly Value Report — {self.customer_id}")
        lines.append(f"**Period:** {self.period_start} → {self.period_end} ({self.month})")
        lines.append(f"**Governance:** {self.governance_decision}")
        lines.append("")
        lines.append(f"_{BILINGUAL_DISCLAIMER}_")
        lines.append("")

        lines.append("## Verified Value (sourced)")
        if self.verified or self.client_confirmed:
            for ev in self.client_confirmed:
                lines.append(
                    f"- [{ProofBadge.CLIENT_CONFIRMED.value}] {ev.get('kind','')} "
                    f"— amount={ev.get('amount',0)} (source={ev.get('source_ref','')}, "
                    f"confirmation={ev.get('confirmation_ref','')})"
                )
            for ev in self.verified:
                lines.append(
                    f"- [{ProofBadge.VERIFIED.value}] {ev.get('kind','')} "
                    f"— amount={ev.get('amount',0)} (source={ev.get('source_ref','')})"
                )
        else:
            lines.append("- (none verified this period)")
        lines.append("")

        lines.append("## Observed Value (in workflow)")
        if self.observed:
            for ev in self.observed:
                lines.append(
                    f"- [{ProofBadge.OBSERVED.value}] {ev.get('kind','')} — amount={ev.get('amount',0)}"
                )
        else:
            lines.append("- (none observed this period)")
        lines.append("")

        lines.append("## Estimated Value (range; not claimable externally)")
        if self.estimated:
            for ev in self.estimated:
                lines.append(
                    f"- [{ProofBadge.ESTIMATED.value}] {ev.get('kind','')} — amount={ev.get('amount',0)}"
                )
        else:
            lines.append("- (none estimated this period)")
        lines.append("")

        lines.append("## Proof Events")
        lines.append(f"- proof_events_count: {self.proof_events_count}")
        lines.append(f"- blocked_unsafe_actions_count: {self.blocked_unsafe_actions_count}")
        lines.append("")

        lines.append("## Adoption Progression")
        prev = self.adoption_progression.get("prev")
        curr = self.adoption_progression.get("curr")
        delta = self.adoption_progression.get("delta")
        lines.append(f"- prev: {prev}")
        lines.append(f"- curr: {curr}")
        lines.append(f"- delta: {delta}")
        lines.append("")

        lines.append("## Friction Summary")
        lines.append(f"- total: {self.friction_summary.get('total', 0)}")
        lines.append(f"- top_3_kinds: {self.friction_summary.get('top_3_kinds', [])}")
        lines.append(f"- total_cost_minutes: {self.friction_summary.get('total_cost_minutes', 0)}")
        lines.append("")

        lines.append("## Limitations")
        if self.limitations:
            for limit in self.limitations:
                lines.append(f"- {limit}")
        else:
            lines.append("- (none recorded)")
        lines.append("")
        lines.append(f"_Generated at {self.generated_at}._")
        return "\n".join(lines)


def _by_tier(events: list[ValueEvent]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {
        "estimated": [], "observed": [], "verified": [], "client_confirmed": [],
    }
    for ev in events:
        out.setdefault(ev.tier, []).append(ev.to_dict())
    return out


def generate(
    *,
    customer_id: str,
    month: str | None = None,
    previous_adoption: float | None = None,
    current_adoption: float | None = None,
) -> MonthlyValueReport:
    month_label, start, end = _month_bounds(month)
    # Pull all events; filter to month window.
    all_events = list_value_events(customer_id=customer_id)
    in_window: list[ValueEvent] = []
    for ev in all_events:
        try:
            ts = datetime.fromisoformat(ev.occurred_at)
        except Exception:  # noqa: S112 - skip event with unparsable timestamp
            continue
        # Make naive-safe
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        if start <= ts.isoformat() <= end or start <= ts.isoformat()[:19] <= end:
            in_window.append(ev)

    buckets = _by_tier(in_window)

    friction = aggregate_friction(customer_id=customer_id, window_days=30)

    limitations: list[str] = []
    if not buckets["verified"] and not buckets["client_confirmed"]:
        limitations.append("no_verified_or_client_confirmed_value_this_period")
    if not in_window:
        limitations.append("no_value_events_in_window")
    if friction.total > 0:
        limitations.append(f"friction_events_in_window:{friction.total}")

    delta = 0.0 if (previous_adoption is None or current_adoption is None) else round(
        float(current_adoption) - float(previous_adoption), 1
    )
    adoption_progression = {
        "prev": previous_adoption,
        "curr": current_adoption,
        "delta": delta,
    }

    # blocked_unsafe = high-severity friction events of governance_block kind
    blocked_unsafe = friction.by_kind.get("governance_block", 0)

    return MonthlyValueReport(
        customer_id=customer_id,
        month=month_label,
        period_start=start,
        period_end=end,
        estimated=buckets["estimated"],
        observed=buckets["observed"],
        verified=buckets["verified"],
        client_confirmed=buckets["client_confirmed"],
        proof_events_count=len(in_window),
        blocked_unsafe_actions_count=blocked_unsafe,
        adoption_progression=adoption_progression,
        friction_summary=friction.to_dict(),
        limitations=limitations,
        governance_decision=GovernanceDecision.ALLOW_WITH_REVIEW.value,
    )


__all__ = ["BILINGUAL_DISCLAIMER", "MonthlyValueReport", "generate"]
