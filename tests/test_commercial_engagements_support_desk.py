"""Tests for Support Desk Sprint runner."""

from __future__ import annotations

from auto_client_acquisition.commercial_engagements.schemas import SupportDeskSprintInput
from auto_client_acquisition.commercial_engagements.support_desk_sprint import (
    run_support_desk_sprint,
)


def test_support_desk_sprint_smoke() -> None:
    inp = SupportDeskSprintInput(
        messages=[
            "أريد استرداد المبلغ",
            {"id": "m2", "text": "سؤال عن الاشتراك والفاتورة"},
        ]
    )
    rep = run_support_desk_sprint(inp)
    d = rep.model_dump()
    assert len(d["items"]) == 2
    assert d["items"][0]["category"]
    assert d["items"][0]["sla_minutes"] > 0
    assert "summary" in d
