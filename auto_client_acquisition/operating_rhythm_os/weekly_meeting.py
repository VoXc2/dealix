"""Weekly Operating Meeting minutes — 10-section structure."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class WeeklyMeetingSection(str, Enum):
    TOP_3_CEO_DECISIONS = "top_3_ceo_decisions"
    REVENUE_PIPELINE = "revenue_pipeline"
    ACTIVE_DELIVERY = "active_delivery"
    PROOF_PACKS = "proof_packs"
    GOVERNANCE_RISKS = "governance_risks"
    CLIENT_ADOPTION = "client_adoption"
    PRODUCTIZATION_SIGNALS = "productization_signals"
    CAPITAL_ALLOCATION = "capital_allocation"
    STOP_KILL_LIST = "stop_kill_list"
    COMMITMENTS = "commitments"


WEEKLY_MEETING_SECTIONS: tuple[WeeklyMeetingSection, ...] = tuple(WeeklyMeetingSection)


@dataclass(frozen=True)
class WeeklyMeetingMinutes:
    week: str
    sections: dict[WeeklyMeetingSection, str]
    decisions_count: int
    commitments_count: int
    risk_to_reduce: str
    proof_to_strengthen: str
    thing_to_stop: str

    def __post_init__(self) -> None:
        missing = set(WEEKLY_MEETING_SECTIONS) - set(self.sections)
        if missing:
            raise ValueError(
                "missing_weekly_meeting_sections:"
                + ",".join(sorted(s.value for s in missing))
            )
        if self.decisions_count < 3:
            raise ValueError("weekly_meeting_requires_3_decisions")
        if self.commitments_count < 3:
            raise ValueError("weekly_meeting_requires_3_commitments")
        if not self.thing_to_stop.strip():
            raise ValueError("weekly_meeting_requires_one_thing_to_stop")
