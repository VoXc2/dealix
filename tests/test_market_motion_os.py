from __future__ import annotations

import pytest

from auto_client_acquisition.sales_os.market_motion import (
    BoardDecision,
    MarketEvent,
    MarketMotionEvent,
    append_event,
    build_first5_drafts_from_csv,
    build_scoreboard,
    evidence_level_for_event,
    read_events,
)


def _event(contact_id: str, event: MarketEvent, source_ref: str = "src") -> MarketMotionEvent:
    return MarketMotionEvent(
        contact_id=contact_id,
        event=event,
        occurred_at="2026-05-16T09:45:00+00:00",
        source_ref=source_ref,
    )


def test_first5_drafts_use_single_question_and_no_links(tmp_path):
    csv_path = tmp_path / "warm_list.csv"
    csv_path.write_text(
        "\n".join(
            [
                "name,role,company,sector,relationship,city,linkedin_url,notes",
                "Ali,COO,Alpha Co,technology,warm,Riyadh,https://linkedin.com/in/x,met at event",
            ]
        ),
        encoding="utf-8",
    )
    drafts = build_first5_drafts_from_csv(csv_path, limit=1)
    assert len(drafts) == 1
    msg = drafts[0].message_en.lower()
    assert "would it be useful" in msg
    assert msg.count("?") == 1
    assert "http://" not in msg
    assert "https://" not in msg
    assert "pdf" not in msg
    assert "deck" not in msg


def test_evidence_levels_match_l4_to_l7_rules():
    assert evidence_level_for_event(MarketEvent.SENT) == "L4"
    assert evidence_level_for_event(MarketEvent.USED_IN_MEETING) == "L5"
    assert evidence_level_for_event(MarketEvent.ASKS_FOR_SCOPE) == "L6"
    assert evidence_level_for_event(MarketEvent.PILOT_INTRO_REQUESTED) == "L6"
    assert evidence_level_for_event(MarketEvent.INVOICE_PAID) == "L7"


def test_sequence_validation_blocks_invoice_before_scope(tmp_path):
    ledger = tmp_path / "events.jsonl"
    append_event(ledger, _event("c1", MarketEvent.SENT))
    with pytest.raises(ValueError, match="invoice_sent requires asks_for_scope first"):
        append_event(ledger, _event("c1", MarketEvent.INVOICE_SENT))


def test_sequence_validation_blocks_invoice_paid_before_invoice_sent(tmp_path):
    ledger = tmp_path / "events.jsonl"
    append_event(ledger, _event("c1", MarketEvent.SENT))
    append_event(ledger, _event("c1", MarketEvent.ASKS_FOR_SCOPE))
    with pytest.raises(ValueError, match="invoice_paid requires invoice_sent first"):
        append_event(ledger, _event("c1", MarketEvent.INVOICE_PAID))


def test_scoreboard_computes_7_numbers_and_scope_priority_decision():
    events = [
        _event("c1", MarketEvent.SENT),
        _event("c2", MarketEvent.SENT),
        _event("c1", MarketEvent.REPLIED_INTERESTED),
        _event("c1", MarketEvent.MEETING_BOOKED),
        _event("c1", MarketEvent.USED_IN_MEETING),
        _event("c1", MarketEvent.ASKS_FOR_SCOPE),
        _event("c2", MarketEvent.NO_RESPONSE_AFTER_FOLLOW_UP),
    ]
    board = build_scoreboard(events)
    assert board.sent_count == 2
    assert board.reply_rate == 0.5
    assert board.meeting_rate == 0.5
    assert board.l5_count == 1
    assert board.l6_count == 1
    assert board.invoice_sent_count == 0
    assert board.invoice_paid_count == 0
    assert board.board_decision == BoardDecision.PREPARE_SCOPE


def test_scoreboard_recommends_batch2_when_no_replies_after_5():
    events = []
    for idx in range(5):
        cid = f"c{idx}"
        events.append(_event(cid, MarketEvent.SENT))
        events.append(_event(cid, MarketEvent.NO_RESPONSE_AFTER_FOLLOW_UP))
    board = build_scoreboard(events)
    assert board.board_decision == BoardDecision.TEST_BATCH_2


def test_append_and_read_roundtrip(tmp_path):
    ledger = tmp_path / "events.jsonl"
    append_event(ledger, _event("c1", MarketEvent.SENT, "whatsapp:1"))
    stored = read_events(ledger)
    assert len(stored) == 1
    assert stored[0].contact_id == "c1"
    assert stored[0].event == MarketEvent.SENT
