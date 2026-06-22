from __future__ import annotations

from .schemas import LeadMachineRunResponse


def rank_leads(results: list[LeadMachineRunResponse]) -> list[LeadMachineRunResponse]:
    return sorted(
        results,
        key=lambda item: (
            item.score.final_priority.value,
            -(item.score.fit + item.score.intent + item.score.urgency),
        ),
    )