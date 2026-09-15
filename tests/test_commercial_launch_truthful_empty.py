from __future__ import annotations

from dealix.commercial_ops import targeting_csv
from scripts import verify_commercial_launch_ready as verify


def _row(**overrides: str) -> dict[str, str]:
    row = {
        "company": "Verified Real Company",
        "contact": "Buyer",
        "segment": "agency_wedge",
        "pain_hypothesis": "Manual execution gap",
        "channel": "email",
        "motion": "A",
        "offer_id": "free_execution_diagnostic",
        "status": "not_contacted",
        "next_action": "draft only",
        "next_action_date": "",
        "priority": "high",
        "notes": "verified relationship test fixture",
    }
    row.update(overrides)
    return row


def _reset() -> None:
    verify.FAILURES.clear()
    verify.WARNINGS.clear()


def test_real_but_closed_target_is_truthful_empty(monkeypatch, capsys) -> None:
    monkeypatch.setattr(targeting_csv, "load_targets", lambda *args, **kwargs: [_row(status="closed_lost")])
    _reset()
    verify.check_targeting_rows()
    verify.check_war_room_build()
    output = capsys.readouterr().out
    assert "truthful_empty real_eligible=0 seed_inventory=1" in output
    assert "war room truthful empty" in output
    assert verify.FAILURES == []


def test_placeholder_only_inventory_never_becomes_war_room(monkeypatch, capsys) -> None:
    placeholder = _row(company="REPLACE: Company", contact="REPLACE: Contact")
    monkeypatch.setattr(targeting_csv, "load_targets", lambda *args, **kwargs: [placeholder])
    _reset()
    verify.check_war_room_build()
    assert "war room truthful empty" in capsys.readouterr().out
    assert verify.FAILURES == []


def test_eligible_real_target_builds_real_war_room(monkeypatch, capsys) -> None:
    monkeypatch.setattr(targeting_csv, "load_targets", lambda *args, **kwargs: [_row()])
    _reset()
    verify.check_war_room_build()
    assert "real eligible targets" in capsys.readouterr().out
    assert verify.FAILURES == []
