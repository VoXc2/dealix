"""Quick Win Ops — weekly rollup + delivery phase checklist snippets."""

from __future__ import annotations

from collections import Counter
from typing import Any

from auto_client_acquisition.commercial_engagements.schemas import (
    QuickWinOpsInput,
    QuickWinOpsReport,
)
from auto_client_acquisition.delivery_os.framework import (
    DEFAULT_PHASE_CHECKLISTS,
    DeliveryPhase,
)

_PHASE_MAP = {
    "build": DeliveryPhase.BUILD,
    "validate": DeliveryPhase.VALIDATE,
}


def run_quick_win_ops(inp: QuickWinOpsInput | dict[str, Any]) -> QuickWinOpsReport:
    if isinstance(inp, dict):
        inp = QuickWinOpsInput.model_validate(inp)

    rows = inp.weekly_rows
    key = inp.group_by
    counts: Counter[str] = Counter()
    for r in rows:
        raw = r.get(key, "unknown")
        counts[str(raw)] += 1

    rollup = {
        "row_count": len(rows),
        "group_by": key,
        "groups": dict(counts),
    }

    checklists: dict[str, list[str]] = {}
    for phase in inp.checklist_phases:
        dp = _PHASE_MAP.get(phase.lower())
        if dp is None:
            continue
        checklists[phase.lower()] = list(DEFAULT_PHASE_CHECKLISTS[dp])

    return QuickWinOpsReport(rollup=rollup, checklists=checklists)
