"""Dealix Capability Index (DCI) — 7 axes × 0–5 maturity.

See ``docs/global_grade/CAPABILITY_INDEX.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum


class DCIAxis(str, Enum):
    REVENUE = "revenue"
    CUSTOMER = "customer"
    OPERATIONS = "operations"
    KNOWLEDGE = "knowledge"
    DATA = "data"
    GOVERNANCE = "governance"
    REPORTING = "reporting"


DCI_AXES: tuple[DCIAxis, ...] = tuple(DCIAxis)


class DCIMaturity(IntEnum):
    ABSENT = 0
    MANUAL = 1
    STRUCTURED = 2
    AI_ASSISTED = 3
    GOVERNED_WORKFLOW = 4
    OPTIMIZED_OS = 5


DCI_MATURITY_LABELS: dict[DCIMaturity, str] = {
    DCIMaturity.ABSENT: "Absent",
    DCIMaturity.MANUAL: "Manual",
    DCIMaturity.STRUCTURED: "Structured",
    DCIMaturity.AI_ASSISTED: "AI-Assisted",
    DCIMaturity.GOVERNED_WORKFLOW: "Governed Workflow",
    DCIMaturity.OPTIMIZED_OS: "Optimized OS",
}


@dataclass(frozen=True)
class DCIReading:
    axis: DCIAxis
    maturity: DCIMaturity
    confidence: float = 1.0  # 0..1; how confident the calibration is

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence_out_of_range")


@dataclass(frozen=True)
class DCIReport:
    client: str
    readings: tuple[DCIReading, ...]
    captured_at: str  # ISO-8601 string; the module stays dependency-free
    method_version: str
    notes: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        seen: set[DCIAxis] = set()
        for r in self.readings:
            if r.axis in seen:
                raise ValueError(f"duplicate_axis:{r.axis.value}")
            seen.add(r.axis)
        missing = set(DCI_AXES) - seen
        if missing:
            raise ValueError(
                "incomplete_dci_report:" + ",".join(a.value for a in sorted(missing, key=lambda a: a.value))
            )

    def composite(self) -> float:
        return sum(r.maturity for r in self.readings) / len(self.readings)

    def weakest(self) -> DCIReading:
        return min(self.readings, key=lambda r: r.maturity)

    def strongest(self) -> DCIReading:
        return max(self.readings, key=lambda r: r.maturity)

    def by_axis(self) -> dict[DCIAxis, DCIMaturity]:
        return {r.axis: r.maturity for r in self.readings}
