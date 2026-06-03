"""Tests for Quick Win Ops runner."""

from __future__ import annotations

from auto_client_acquisition.commercial_engagements.quick_win_ops import run_quick_win_ops
from auto_client_acquisition.commercial_engagements.schemas import QuickWinOpsInput


def test_quick_win_ops_rollup_and_checklists() -> None:
    inp = QuickWinOpsInput(
        weekly_rows=[
            {"channel": "email", "count": 1},
            {"channel": "email", "count": 2},
            {"channel": "chat", "count": 3},
        ],
        group_by="channel",
    )
    rep = run_quick_win_ops(inp)
    d = rep.model_dump()
    assert d["rollup"]["row_count"] == 3
    assert d["rollup"]["groups"]["email"] == 2
    assert d["rollup"]["groups"]["chat"] == 1
    assert "build" in d["checklists"] and "validate" in d["checklists"]
    assert "human-in-the-loop" in " ".join(d["checklists"]["build"]).lower()
