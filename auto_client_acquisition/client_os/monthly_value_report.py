"""Monthly Value Report — 8-section client-facing artifact."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MonthlyValueReportSection(str, Enum):
    WHAT_WAS_DONE = "what_was_done"
    WHAT_CHANGED = "what_changed"
    OBSERVED_VALUE = "observed_value"
    ESTIMATED_VALUE = "estimated_value"
    RISKS_BLOCKED = "risks_blocked"
    NEEDS_APPROVAL = "needs_approval"
    CAPABILITY_IMPROVED = "capability_improved"
    NEXT_STEP = "next_step"


MONTHLY_VALUE_REPORT_SECTIONS: tuple[MonthlyValueReportSection, ...] = tuple(
    MonthlyValueReportSection
)


_TITLES: dict[MonthlyValueReportSection, str] = {
    s: f"{i+1}. {s.value.replace('_', ' ').title()}"
    for i, s in enumerate(MONTHLY_VALUE_REPORT_SECTIONS)
}


@dataclass(frozen=True)
class MonthlyValueReport:
    client_id: str
    period: str
    sections: dict[MonthlyValueReportSection, str]

    def __post_init__(self) -> None:
        missing = set(MONTHLY_VALUE_REPORT_SECTIONS) - set(self.sections)
        if missing:
            raise ValueError(
                "missing_value_report_sections:"
                + ",".join(sorted(s.value for s in missing))
            )


def render_monthly_value_report(r: MonthlyValueReport) -> str:
    parts = [f"# Monthly Value Report — {r.client_id} — {r.period}", ""]
    for s in MONTHLY_VALUE_REPORT_SECTIONS:
        parts.append(f"## {_TITLES[s]}")
        parts.append("")
        parts.append(r.sections[s].strip() or "none")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"
