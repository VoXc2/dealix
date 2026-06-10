"""Commercial ops expansion helpers."""

from __future__ import annotations

from scripts.expand_agency_targets_seed import expand_targets


def test_expand_targets_idempotent(tmp_path, monkeypatch) -> None:
    csv_path = tmp_path / "agency_accounts_seed.csv"
    csv_path.write_text(
        "company,contact,segment,pain_hypothesis,channel,motion,offer_id,status,"
        "next_action,next_action_date,priority,notes\n"
        "Acme,CEO,agency_wedge,pain,email_warm,A,ten_lead_audit,not_contacted,next,,high,\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("scripts.expand_agency_targets_seed.AGENCY_TARGETS_CSV", csv_path)
    before, after = expand_targets(min_rows=5)
    assert before == 1
    assert after >= 5
    _, again = expand_targets(min_rows=5)
    assert again == after
