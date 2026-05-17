"""Funnel Scoreboard — the only 10 numbers that matter, daily.

Target Accounts -> Conversations -> Proof Pack Requests -> Meetings ->
Scopes -> Invoices -> Paid -> Proof Packs Delivered -> Upsells -> Referrals.

Measures output (revenue motion), not activity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from itertools import pairwise
from typing import Any


class FunnelStage(StrEnum):
    TARGET_ACCOUNTS = "target_accounts"
    CONVERSATIONS = "conversations"
    PROOF_PACK_REQUESTS = "proof_pack_requests"
    MEETINGS = "meetings"
    SCOPES = "scopes"
    INVOICES = "invoices"
    PAID = "paid"
    PROOF_PACKS_DELIVERED = "proof_packs_delivered"
    UPSELLS = "upsells"
    REFERRALS = "referrals"


FUNNEL_ORDER: tuple[FunnelStage, ...] = (
    FunnelStage.TARGET_ACCOUNTS,
    FunnelStage.CONVERSATIONS,
    FunnelStage.PROOF_PACK_REQUESTS,
    FunnelStage.MEETINGS,
    FunnelStage.SCOPES,
    FunnelStage.INVOICES,
    FunnelStage.PAID,
    FunnelStage.PROOF_PACKS_DELIVERED,
    FunnelStage.UPSELLS,
    FunnelStage.REFERRALS,
)

TARGETS_30D: dict[FunnelStage, int] = {
    FunnelStage.TARGET_ACCOUNTS: 100,
    FunnelStage.CONVERSATIONS: 30,
    FunnelStage.PROOF_PACK_REQUESTS: 10,
    FunnelStage.MEETINGS: 5,
    FunnelStage.SCOPES: 2,
    FunnelStage.INVOICES: 1,
    FunnelStage.PAID: 1,
    FunnelStage.PROOF_PACKS_DELIVERED: 1,
    FunnelStage.UPSELLS: 0,
    FunnelStage.REFERRALS: 1,
}

TARGETS_90D: dict[FunnelStage, int] = {
    FunnelStage.TARGET_ACCOUNTS: 300,
    FunnelStage.CONVERSATIONS: 90,
    FunnelStage.PROOF_PACK_REQUESTS: 30,
    FunnelStage.MEETINGS: 18,
    FunnelStage.SCOPES: 8,
    FunnelStage.INVOICES: 5,
    FunnelStage.PAID: 4,
    FunnelStage.PROOF_PACKS_DELIVERED: 3,
    FunnelStage.UPSELLS: 1,
    FunnelStage.REFERRALS: 5,
}


@dataclass(frozen=True, slots=True)
class FunnelScoreboard:
    period: str
    counts: dict[str, int]
    targets: dict[str, int]
    gaps: dict[str, int]
    conversion_rates: dict[str, float]
    bottleneck_stage: str
    on_track: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalize_counts(counts: dict[str, int]) -> dict[FunnelStage, int]:
    out: dict[FunnelStage, int] = {}
    for stage in FUNNEL_ORDER:
        out[stage] = max(0, int(counts.get(stage.value, counts.get(stage, 0))))
    return out


def _conversion_rates(counts: dict[FunnelStage, int]) -> dict[str, float]:
    rates: dict[str, float] = {}
    for prev, nxt in pairwise(FUNNEL_ORDER):
        upstream = counts[prev]
        rates[f"{prev.value}->{nxt.value}"] = round(counts[nxt] / upstream, 3) if upstream else 0.0
    return rates


def worst_bottleneck(counts: dict[str, int]) -> str:
    """Return the funnel transition with the weakest conversion rate.

    Stages with zero upstream volume are skipped — you cannot have a
    conversion bottleneck where nothing entered.
    """
    norm = _normalize_counts(counts)
    worst_stage = FunnelStage.TARGET_ACCOUNTS.value
    worst_rate = 2.0
    for prev, nxt in pairwise(FUNNEL_ORDER):
        if norm[prev] <= 0:
            continue
        rate = norm[nxt] / norm[prev]
        if rate < worst_rate:
            worst_rate = rate
            worst_stage = nxt.value
    return worst_stage


def build_scoreboard(counts: dict[str, int], period: str = "30d") -> FunnelScoreboard:
    """Build the daily funnel scoreboard against 30d or 90d targets."""
    norm = _normalize_counts(counts)
    targets = TARGETS_90D if period == "90d" else TARGETS_30D
    gaps = {s.value: targets[s] - norm[s] for s in FUNNEL_ORDER}
    on_track = all(gap <= 0 for gap in gaps.values())
    return FunnelScoreboard(
        period=period,
        counts={s.value: norm[s] for s in FUNNEL_ORDER},
        targets={s.value: targets[s] for s in FUNNEL_ORDER},
        gaps=gaps,
        conversion_rates=_conversion_rates(norm),
        bottleneck_stage=worst_bottleneck(counts),
        on_track=on_track,
    )


__all__ = [
    "FUNNEL_ORDER",
    "TARGETS_30D",
    "TARGETS_90D",
    "FunnelScoreboard",
    "FunnelStage",
    "build_scoreboard",
    "worst_bottleneck",
]
