"""Full Ops 2.0 — real learning loops (reply->objection, ticket->KB)."""
from __future__ import annotations

import json

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.learning_loops.reply_objection_loop import (
    build_objection_library,
    load_classified_replies,
)
from auto_client_acquisition.learning_loops.ticket_kb_loop import (
    build_kb_candidates,
    load_ticket_categories,
)


# ── reply -> objection library ───────────────────────────────────


def test_build_objection_library_dedups_and_counts() -> None:
    replies = [
        {"category": "objection_budget", "original_text": "too expensive"},
        {"category": "objection_budget", "original_text": "too expensive"},
        {"category": "objection_budget", "original_text": "over our budget"},
        {"category": "objection_privacy", "original_text": "PDPL concern"},
        {"category": "interested", "original_text": "yes let's go"},
    ]
    lib = build_objection_library(replies)
    by_cat = {e.category: e for e in lib}
    assert by_cat["objection_budget"].count == 3
    # Deduplicated sample text — "too expensive" stored once.
    assert by_cat["objection_budget"].sample_texts.count("too expensive") == 1
    assert by_cat["objection_privacy"].count == 1
    # Non-objection categories are excluded.
    assert "interested" not in by_cat


def test_build_objection_library_sorted_by_count() -> None:
    replies = (
        [{"category": "objection_ai"}] * 5
        + [{"category": "not_now"}] * 2
    )
    lib = build_objection_library(replies)
    assert lib[0].category == "objection_ai"
    assert lib[0].count == 5


def test_load_classified_replies_reads_jsonl(tmp_path, monkeypatch) -> None:
    path = tmp_path / "replies.jsonl"
    path.write_text(
        json.dumps({"category": "objection_budget", "original_text": "غالي"}) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("DEALIX_CLASSIFIED_REPLIES_PATH", str(path))
    rows = load_classified_replies()
    assert len(rows) == 1
    lib = build_objection_library(rows)
    assert lib[0].category == "objection_budget"


def test_load_classified_replies_missing_store_returns_empty(monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_CLASSIFIED_REPLIES_PATH", "/nonexistent/x.jsonl")
    assert load_classified_replies() == []


# ── ticket -> KB-article candidates ──────────────────────────────


def test_build_kb_candidates_threshold() -> None:
    tickets = (
        ["billing"] * 4
        + ["onboarding"] * 2  # below threshold (3)
        + ["payment"] * 3
    )
    candidates = build_kb_candidates(tickets)
    cats = {c.category for c in candidates}
    assert "billing" in cats
    assert "payment" in cats
    assert "onboarding" not in cats  # only recurred twice


def test_build_kb_candidates_excludes_unknown() -> None:
    candidates = build_kb_candidates(["unknown"] * 10)
    assert candidates == []


def test_build_kb_candidates_priority_escalates() -> None:
    candidates = build_kb_candidates(["technical_issue"] * 8, recurrence_threshold=3)
    assert candidates[0].priority == "high"


def test_load_ticket_categories_reads_jsonl(tmp_path, monkeypatch) -> None:
    path = tmp_path / "tickets.jsonl"
    lines = [json.dumps({"category": "refund"}) for _ in range(3)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    monkeypatch.setenv("DEALIX_SUPPORT_TICKETS_PATH", str(path))
    cats = load_ticket_categories()
    assert cats == ["refund", "refund", "refund"]
    candidates = build_kb_candidates(cats)
    assert candidates[0].category == "refund"


def test_load_ticket_categories_missing_store_returns_empty(monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_SUPPORT_TICKETS_PATH", "/nonexistent/t.jsonl")
    assert load_ticket_categories() == []


# ── router ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_weekly_learning_runs_real_loops(tmp_path, monkeypatch) -> None:
    from api.main import app

    rpath = tmp_path / "replies.jsonl"
    rpath.write_text(
        "\n".join(
            json.dumps({"category": "objection_budget", "original_text": "غالي"})
            for _ in range(3)
        )
        + "\n",
        encoding="utf-8",
    )
    tpath = tmp_path / "tickets.jsonl"
    tpath.write_text(
        "\n".join(json.dumps({"category": "billing"}) for _ in range(4)) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("DEALIX_CLASSIFIED_REPLIES_PATH", str(rpath))
    monkeypatch.setenv("DEALIX_SUPPORT_TICKETS_PATH", str(tpath))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-improvement-os/weekly-learning")
    body = r.json()
    assert body["data_status"] == "live"
    loops = {loop["loop"]: loop for loop in body["learning_loops"]}
    reply_loop = loops["reply_to_objection_library"]
    assert reply_loop["replies_analyzed"] == 3
    assert reply_loop["objection_library"][0]["category"] == "objection_budget"
    ticket_loop = loops["ticket_to_kb_article_candidate"]
    assert ticket_loop["tickets_analyzed"] == 4
    assert ticket_loop["kb_article_candidates"][0]["category"] == "billing"
