"""Client Capability Dashboard — typed snapshot of the 7 axes."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.global_grade_os.capability_index import (
    DCIAxis,
    DCIMaturity,
)


@dataclass(frozen=True)
class ClientCapabilitySnapshot:
    client_id: str
    period: str
    by_axis: dict[DCIAxis, DCIMaturity]

    def composite(self) -> float:
        if not self.by_axis:
            return 0.0
        return sum(int(m) for m in self.by_axis.values()) / len(self.by_axis)

    def weakest(self) -> DCIAxis:
        return min(self.by_axis, key=lambda a: int(self.by_axis[a]))
