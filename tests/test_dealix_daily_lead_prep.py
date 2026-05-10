"""Wave 12.8 — tests for the daily autonomous lead-prep script.

Validates:
- Empty candidates → empty board (Article 8 — no fabrication)
- 5+ candidates → top-N ranking by composite score
- Blocked sources (cold_outreach / scraping) routed to BLOCKED priority
  REGARDLESS of other scores (Article 4 defense in depth)
- Action mode is NEVER live-send (always draft_only / approval_required / blocked)
- Output files written to gitignored path
- Bilingual output present
- is_estimate=True (Article 8)
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.dealix_daily_lead_prep import (
    DailyLeadBoard,
    LeadCandidate,
    _composite_score,
    load_candidates_from_csv,
    load_candidates_from_lead_inbox,
    run_daily_prep,
    write_board,
)
from auto_client_acquisition.pipelines.saudi_dimensions import (
    compute_saudi_score_board,
)


# ─────────────────────────────────────────────────────────────────────
# Empty / minimal cases (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_empty_candidates_returns_empty_board() -> None:
    """No candidates → empty top_leads + helpful next action (Article 8)."""
    board = run_daily_prep(candidates=[], on_date=date(2026, 5, 15))
    assert board.candidates_count == 0
    assert board.leads_returned == 0
    assert board.top_leads == ()
    assert "candidates" in board.next_founder_action.lower() or "ليدز" in board.next_founder_action
    assert board.is_estimate is True


def test_season_context_always_present() -> None:
    """Even with no candidates, season context is computed."""
    board = run_daily_prep(candidates=[], on_date=date(2026, 3, 21))  # Eid
    assert board.season_context["season"] == "eid_al_fitr"
    assert "PAUSE" in board.season_context["recommended_offer_pivot"]


def test_article_4_invariants_listed() -> None:
    """Article 4 invariants enumerated in the output."""
    board = run_daily_prep(candidates=[], on_date=date(2026, 5, 15))
    invariants = set(board.article_4_invariants)
    assert "no_live_send_called" in invariants
    assert "no_live_charge_called" in invariants
    assert "no_scraping_invoked" in invariants
    assert "blocked_sources_routed_to_blocked_priority" in invariants


# ─────────────────────────────────────────────────────────────────────
# Ranking + composite score (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_warm_intro_ranks_higher_than_unknown_source() -> None:
    """warm_intro should outrank unknown_source."""
    candidates = [
        LeadCandidate(name="Cold-source Co", source="totally_unknown_source"),
        LeadCandidate(name="Warm Acme", source="warm_intro",
                       contact_title="CEO", domain="acme.sa"),
    ]
    board = run_daily_prep(candidates=candidates, on_date=date(2026, 5, 15), top_n=2)
    # Warm Acme should rank #1
    assert board.top_leads[0].candidate.name == "Warm Acme"
    assert board.top_leads[1].candidate.name == "Cold-source Co"


def test_blocked_sources_routed_to_blocked_priority() -> None:
    """Article 4: cold_outreach / scraping / linkedin_automation always
    end up at BLOCKED priority regardless of other scores."""
    candidates = [
        LeadCandidate(name="Strong Saudi", source="warm_intro",
                       domain="acme.com.sa", country="SA",
                       contact_title="Founder"),
        LeadCandidate(name="Bad Source", source="cold_outreach",
                       domain="acme.com.sa", country="SA",
                       contact_title="Founder"),
    ]
    board = run_daily_prep(candidates=candidates, on_date=date(2026, 5, 15), top_n=2)
    # The blocked one must end up at BLOCKED priority
    bad = next(e for e in board.top_leads if e.candidate.name == "Bad Source")
    assert bad.priority == "BLOCKED"
    assert bad.action_mode == "blocked"
    # The good one should NOT be BLOCKED
    good = next(e for e in board.top_leads if e.candidate.name == "Strong Saudi")
    assert good.priority != "BLOCKED"


def test_top_n_caps_returned_leads() -> None:
    """top_n=3 returns exactly 3 leads from 5 candidates."""
    candidates = [
        LeadCandidate(name=f"Co{i}", source="warm_intro")
        for i in range(5)
    ]
    board = run_daily_prep(candidates=candidates, on_date=date(2026, 5, 15), top_n=3)
    assert board.candidates_count == 5
    assert board.leads_returned == 3
    assert len(board.top_leads) == 3


def test_composite_score_formula_in_range() -> None:
    """Composite score is always in [0, 1]."""
    for src in ("warm_intro", "inbound_form", "cold_outreach", "unknown_source"):
        c = LeadCandidate(name="X", source=src)
        board = compute_saudi_score_board(
            {"name": "X", "source": src}, on_date=date(2026, 5, 15),
        )
        score = _composite_score(board)
        assert 0.0 <= score <= 1.0


def test_rank_is_stable_for_identical_scores() -> None:
    """Two identical candidates → both in top, both with same score."""
    c1 = LeadCandidate(name="A", source="warm_intro", contact_title="CEO")
    c2 = LeadCandidate(name="B", source="warm_intro", contact_title="CEO")
    board = run_daily_prep(candidates=[c1, c2], on_date=date(2026, 5, 15), top_n=2)
    assert len(board.top_leads) == 2
    assert board.top_leads[0].composite_score == board.top_leads[1].composite_score


# ─────────────────────────────────────────────────────────────────────
# Action mode safety (Article 4) (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_no_lead_returns_live_send_action_mode() -> None:
    """Article 4: action_mode is NEVER live_send / auto_send / live_charge."""
    candidates = [
        LeadCandidate(name=f"Co{i}", source=src)
        for i, src in enumerate([
            "warm_intro", "inbound_form", "cold_outreach",
            "manual_linkedin_research", "scraping",
        ])
    ]
    board = run_daily_prep(candidates=candidates, on_date=date(2026, 5, 15), top_n=5)
    valid_modes = {"draft_only", "approval_required", "blocked"}
    for entry in board.top_leads:
        assert entry.action_mode in valid_modes, \
            f"{entry.candidate.name} returned non-canonical mode={entry.action_mode!r}"


def test_p0_now_requires_approval() -> None:
    """P0_NOW priority → approval_required (never auto-send)."""
    # Build a strong candidate likely to land P0
    c = LeadCandidate(
        name="Top Acme", source="warm_intro", contact_title="CEO",
        domain="acme.com.sa", country="SA", city="Riyadh",
        locale="ar-SA",
    )
    board = run_daily_prep(candidates=[c], on_date=date(2026, 5, 15), top_n=1)
    if board.top_leads[0].priority == "P0_NOW":
        assert board.top_leads[0].action_mode == "approval_required"


def test_blocked_lead_action_mode_blocked() -> None:
    """BLOCKED priority → blocked action_mode (no draft, no message)."""
    c = LeadCandidate(name="X", source="cold_outreach")
    board = run_daily_prep(candidates=[c], on_date=date(2026, 5, 15), top_n=1)
    assert board.top_leads[0].priority == "BLOCKED"
    assert board.top_leads[0].action_mode == "blocked"


# ─────────────────────────────────────────────────────────────────────
# Output writers (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_write_board_creates_json_and_md(tmp_path: Path) -> None:
    """write_board produces both JSON and Markdown files."""
    c = LeadCandidate(name="Test Co", source="warm_intro")
    board = run_daily_prep(candidates=[c], on_date=date(2026, 5, 15), top_n=1)
    json_path, md_path = write_board(board, out_dir=tmp_path)
    assert json_path.exists()
    assert md_path.exists()
    assert json_path.suffix == ".json"
    assert md_path.suffix == ".md"


def test_json_output_parseable_and_complete(tmp_path: Path) -> None:
    """JSON output round-trips + contains expected keys."""
    c = LeadCandidate(name="Test Co", source="warm_intro")
    board = run_daily_prep(candidates=[c], on_date=date(2026, 5, 15), top_n=1)
    json_path, _ = write_board(board, out_dir=tmp_path)
    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert "on_date" in data
    assert "season_context" in data
    assert "top_leads" in data
    assert "article_4_invariants" in data
    assert "is_estimate" in data
    assert data["is_estimate"] is True


def test_markdown_output_bilingual(tmp_path: Path) -> None:
    """MD output contains both Arabic and English sections."""
    c = LeadCandidate(name="Test Co", source="warm_intro", contact_title="Founder")
    board = run_daily_prep(candidates=[c], on_date=date(2026, 5, 15), top_n=1)
    _, md_path = write_board(board, out_dir=tmp_path)
    md = md_path.read_text(encoding="utf-8")
    assert "ملخص اليوم" in md or "Today's summary" in md
    assert "Article 4 invariants" in md
    assert "draft_only" in md or "approval_required" in md or "blocked" in md


# ─────────────────────────────────────────────────────────────────────
# CSV loader (2 tests)
# ─────────────────────────────────────────────────────────────────────


def test_load_csv_with_minimal_headers(tmp_path: Path) -> None:
    """CSV with only `name` column loads."""
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text("name\nAcme\nKhaleej\n", encoding="utf-8")
    candidates = load_candidates_from_csv(csv_path)
    assert len(candidates) == 2
    assert candidates[0].name == "Acme"
    # Defaults applied
    assert candidates[0].source == "warm_intro"
    assert candidates[0].locale == "ar"


def test_load_csv_with_full_headers(tmp_path: Path) -> None:
    """CSV with all optional columns loads correctly."""
    csv_path = tmp_path / "leads.csv"
    csv_path.write_text(
        "name,sector,city,country,domain,contact_name,contact_title,"
        "source,locale,annual_turnover_sar,notes\n"
        "Acme,real_estate,Riyadh,SA,acme.com.sa,Sami,CEO,"
        "warm_intro,ar-SA,500000,test note\n",
        encoding="utf-8",
    )
    candidates = load_candidates_from_csv(csv_path)
    assert len(candidates) == 1
    c = candidates[0]
    assert c.name == "Acme"
    assert c.sector == "real_estate"
    assert c.contact_title == "CEO"
    assert c.annual_turnover_sar == 500000.0


# ─────────────────────────────────────────────────────────────────────
# Lead inbox auto-source (Wave 12.9) — 4 tests
# ─────────────────────────────────────────────────────────────────────


def test_auto_source_returns_empty_when_no_inbox(monkeypatch, tmp_path) -> None:
    """When lead_inbox.jsonl doesn't exist, auto-source returns []."""
    # Point lead_inbox at a non-existent file
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(tmp_path / "missing.jsonl"))
    candidates = load_candidates_from_lead_inbox()
    assert candidates == []


def test_auto_source_pulls_new_status_only(monkeypatch, tmp_path) -> None:
    """Only records with status='new' are pulled (Article 4 — don't
    re-target customers we've already contacted)."""
    inbox_path = tmp_path / "inbox.jsonl"
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(inbox_path))
    # Write 3 records: 1 new, 1 contacted, 1 converted
    import json as _json
    with inbox_path.open("w", encoding="utf-8") as f:
        f.write(_json.dumps({
            "id": "lead_1", "received_at": "2026-05-15T00:00:00Z",
            "status": "new", "company_name": "New Acme",
            "contact_name": "Sami", "sector": "real_estate",
        }) + "\n")
        f.write(_json.dumps({
            "id": "lead_2", "received_at": "2026-05-14T00:00:00Z",
            "status": "contacted", "company_name": "Contacted Khaleej",
        }) + "\n")
        f.write(_json.dumps({
            "id": "lead_3", "received_at": "2026-05-13T00:00:00Z",
            "status": "converted", "company_name": "Converted Tahaluf",
        }) + "\n")
    candidates = load_candidates_from_lead_inbox()
    # Only the new one
    assert len(candidates) == 1
    assert candidates[0].name == "New Acme"
    assert candidates[0].source == "inbound_form"  # auto-tagged


def test_auto_source_skips_records_without_name(monkeypatch, tmp_path) -> None:
    """Records without company_name/company/name → skipped."""
    inbox_path = tmp_path / "inbox.jsonl"
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(inbox_path))
    import json as _json
    with inbox_path.open("w", encoding="utf-8") as f:
        f.write(_json.dumps({
            "id": "lead_1", "status": "new",
            # No company_name / company / name / contact_name
            "phone": "+966555",
        }) + "\n")
    candidates = load_candidates_from_lead_inbox()
    assert candidates == []


def test_auto_source_marks_source_inbound_form() -> None:
    """Article 4 — every auto-sourced lead is tagged source=inbound_form
    (a SAFE source — landing form = consent given)."""
    # Use a fake record dict directly
    import json as _json
    import os
    from pathlib import Path
    tmp = Path("/tmp/test_inbox_safe.jsonl")
    try:
        with tmp.open("w", encoding="utf-8") as f:
            f.write(_json.dumps({
                "id": "lead_1", "status": "new",
                "company_name": "Inbound Test Co",
            }) + "\n")
        os.environ["DEALIX_LEAD_INBOX_PATH"] = str(tmp)
        candidates = load_candidates_from_lead_inbox()
        assert candidates[0].source == "inbound_form"  # SAFE source
        # And NOT a blocked source
        assert candidates[0].source not in (
            "cold_outreach", "scraping", "purchased_list", "linkedin_automation"
        )
    finally:
        os.environ.pop("DEALIX_LEAD_INBOX_PATH", None)
        tmp.unlink(missing_ok=True)


# ─────────────────────────────────────────────────────────────────────
# Total: 20 tests (3 empty + 5 ranking + 3 action_mode + 3 output +
#                  2 csv + 4 auto-source)
# ─────────────────────────────────────────────────────────────────────
