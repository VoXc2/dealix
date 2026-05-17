"""Control Rules — when to scale, keep, or kill a channel.

Deterministic verdict from channel performance signals.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

# Defaults — overridable per call.
SCALE_MIN_REPLY_RATE = 0.10
SCALE_MIN_MEETING_RATE = 0.10
KILL_MAX_REPLY_RATE = 0.02


class ChannelVerdict(StrEnum):
    SCALE = "scale"
    KEEP = "keep"
    KILL = "kill"


@dataclass(frozen=True, slots=True)
class ChannelDecision:
    channel: str
    verdict: str
    rationale: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def channel_verdict(
    *,
    channel: str,
    qualified_leads: int,
    reply_rate: float,
    meeting_rate: float,
    compliance_issues: int = 0,
    requires_overpromising: bool = False,
    high_support_burden: bool = False,
) -> ChannelDecision:
    """Classify a channel as scale / keep / kill.

    Kill always wins when the channel is unsafe (compliance issues,
    over-promising, or spammy). Scale needs clean signal on both
    reply and meeting rates. Everything else is keep-and-improve.
    """
    rationale: list[str] = []

    kill = False
    if compliance_issues > 0:
        kill = True
        rationale.append("compliance_issues_present")
    if requires_overpromising:
        kill = True
        rationale.append("requires_overpromising")
    if high_support_burden and qualified_leads <= 0:
        kill = True
        rationale.append("high_support_burden_no_qualified_leads")
    if reply_rate <= KILL_MAX_REPLY_RATE and qualified_leads <= 0:
        kill = True
        rationale.append("reply_rate_floor_and_no_qualified_leads")

    if kill:
        return ChannelDecision(channel, ChannelVerdict.KILL.value, tuple(rationale))

    if (
        qualified_leads > 0
        and reply_rate >= SCALE_MIN_REPLY_RATE
        and meeting_rate >= SCALE_MIN_MEETING_RATE
    ):
        rationale.append("qualified_leads_and_healthy_reply_and_meeting_rates")
        return ChannelDecision(channel, ChannelVerdict.SCALE.value, tuple(rationale))

    rationale.append("signal_present_but_needs_improvement")
    return ChannelDecision(channel, ChannelVerdict.KEEP.value, tuple(rationale))


__all__ = [
    "ChannelDecision",
    "ChannelVerdict",
    "channel_verdict",
]
