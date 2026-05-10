"""Wave 12 §32.3.3 (Engine 3) — Company Brain Timeline tests.

Validates the append-only event log:
- Records events safely (validation, atomic append, JSONL format)
- Reads with optional kind filter + limit
- Summarizes what_worked / what_failed for builder + learning loop
- Rejects unsafe handles (path traversal, oversize)
- Skips malformed JSONL lines (forward-compat)

All tests use ``tmp_path`` so production data/wave12/ is never touched.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_client_acquisition.company_brain_v6.timeline import (
    TimelineHandleInvalid,
    TimelineEvent,
    event_count,
    read_timeline,
    record_event,
    summarize_what_worked_failed,
)


# ─────────────────────────────────────────────────────────────────────
# Recording (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_record_event_creates_file_and_returns_event(tmp_path: Path) -> None:
    """First event creates the JSONL file + returns the recorded event."""
    evt = record_event(
        "test-acme",
        kind="learned",
        summary_ar="العميل يفضّل اللهجة السعودية",
        summary_en="customer prefers Saudi dialect",
        confidence=0.9,
        tags=("tone",),
        base_dir=tmp_path,
    )
    assert evt.kind == "learned"
    assert evt.confidence == 0.9
    assert "tone" in evt.tags
    assert (tmp_path / "test-acme.jsonl").exists()


def test_record_event_appends_existing_file(tmp_path: Path) -> None:
    """Multiple events append (not overwrite)."""
    record_event("test-acme", kind="learned", summary_ar="x1", summary_en="x1", base_dir=tmp_path)
    record_event("test-acme", kind="tried", summary_ar="x2", summary_en="x2", base_dir=tmp_path)
    record_event("test-acme", kind="worked", summary_ar="x3", summary_en="x3", base_dir=tmp_path)
    assert event_count("test-acme", base_dir=tmp_path) == 3


def test_record_event_truncates_long_summaries(tmp_path: Path) -> None:
    """Summaries > 140 chars get truncated (no surprise file growth)."""
    long_text = "ا" * 200  # 200-char Arabic
    evt = record_event(
        "test-acme", kind="learned",
        summary_ar=long_text, summary_en=long_text,
        base_dir=tmp_path,
    )
    assert len(evt.summary_ar) == 140
    assert len(evt.summary_en) == 140


def test_record_event_rejects_invalid_confidence(tmp_path: Path) -> None:
    """confidence outside [0,1] raises ValueError."""
    with pytest.raises(ValueError, match="confidence"):
        record_event(
            "test-acme", kind="learned",
            summary_ar="x", summary_en="x",
            confidence=1.5, base_dir=tmp_path,
        )
    with pytest.raises(ValueError, match="confidence"):
        record_event(
            "test-acme", kind="learned",
            summary_ar="x", summary_en="x",
            confidence=-0.1, base_dir=tmp_path,
        )


def test_record_event_rejects_unsafe_handles(tmp_path: Path) -> None:
    """Path-traversal attempts + oversize handles must be rejected."""
    bad_handles = [
        "../etc/passwd",
        "/absolute/path",
        "test/with/slash",
        "",
        "a" * 100,  # too long
        "test with space",
    ]
    for h in bad_handles:
        with pytest.raises(TimelineHandleInvalid):
            record_event(
                h, kind="learned",
                summary_ar="x", summary_en="x",
                base_dir=tmp_path,
            )


# ─────────────────────────────────────────────────────────────────────
# Reading (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_read_timeline_returns_empty_when_file_missing(tmp_path: Path) -> None:
    """No file → empty list (Article 8 — no fabrication)."""
    events = read_timeline("never-existed", base_dir=tmp_path)
    assert events == []


def test_read_timeline_returns_chronological_order(tmp_path: Path) -> None:
    """Events come back in insertion order (file is append-only; reads
    return newest-last)."""
    record_event("test-acme", kind="learned", summary_ar="first", summary_en="first", base_dir=tmp_path)
    record_event("test-acme", kind="tried", summary_ar="second", summary_en="second", base_dir=tmp_path)
    record_event("test-acme", kind="worked", summary_ar="third", summary_en="third", base_dir=tmp_path)
    events = read_timeline("test-acme", base_dir=tmp_path)
    assert len(events) == 3
    assert events[0].summary_ar == "first"
    assert events[2].summary_ar == "third"


def test_read_timeline_filters_by_kind(tmp_path: Path) -> None:
    """kind_filter returns only matching events."""
    record_event("test-acme", kind="worked", summary_ar="a", summary_en="a", base_dir=tmp_path)
    record_event("test-acme", kind="failed", summary_ar="b", summary_en="b", base_dir=tmp_path)
    record_event("test-acme", kind="worked", summary_ar="c", summary_en="c", base_dir=tmp_path)
    worked = read_timeline("test-acme", kind_filter="worked", base_dir=tmp_path)
    assert len(worked) == 2
    assert all(e.kind == "worked" for e in worked)


def test_read_timeline_skips_malformed_lines(tmp_path: Path) -> None:
    """Malformed JSONL lines are skipped (forward-compat); never raise."""
    record_event("test-acme", kind="learned", summary_ar="ok", summary_en="ok", base_dir=tmp_path)
    # Corrupt the file mid-stream
    path = tmp_path / "test-acme.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write("this is not json\n")
        f.write("{partial: missing quotes}\n")
        f.write(json.dumps({"timestamp": "x", "kind": "tried", "summary_ar": "y",
                            "summary_en": "y", "confidence": 0.5}) + "\n")
    events = read_timeline("test-acme", base_dir=tmp_path)
    # Should return the 2 valid events, skip the 2 corrupt lines
    assert len(events) == 2
    assert events[0].summary_ar == "ok"
    assert events[1].summary_ar == "y"


# ─────────────────────────────────────────────────────────────────────
# Summarization (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_summarize_buckets_by_outcome(tmp_path: Path) -> None:
    """summarize() groups by event kind for builder consumption."""
    record_event("test-acme", kind="worked", summary_ar="رسالة عربية نجحت", summary_en="ar message worked", base_dir=tmp_path)
    record_event("test-acme", kind="failed", summary_ar="رسالة إنجليزية فشلت", summary_en="en message failed", base_dir=tmp_path)
    record_event("test-acme", kind="avoided", summary_ar="تجنبنا واتساب", summary_en="avoided whatsapp", base_dir=tmp_path)
    record_event("test-acme", kind="hypothesis", summary_ar="جربوا LinkedIn", summary_en="try linkedin", base_dir=tmp_path)

    summary = summarize_what_worked_failed("test-acme", base_dir=tmp_path)
    assert len(summary["what_worked"]) == 1
    assert len(summary["what_failed"]) == 1
    assert len(summary["what_avoided"]) == 1
    assert len(summary["open_hypotheses"]) == 1


def test_summarize_returns_empty_for_unknown_customer(tmp_path: Path) -> None:
    """No events → all 4 buckets empty (no fabrication)."""
    summary = summarize_what_worked_failed("never-existed", base_dir=tmp_path)
    assert summary == {
        "what_worked": [], "what_failed": [],
        "what_avoided": [], "open_hypotheses": [],
    }


def test_event_count_cheap_no_parse(tmp_path: Path) -> None:
    """event_count returns line-count without JSON parsing (fast)."""
    assert event_count("never-existed", base_dir=tmp_path) == 0
    record_event("test-acme", kind="learned", summary_ar="x", summary_en="x", base_dir=tmp_path)
    record_event("test-acme", kind="tried", summary_ar="y", summary_en="y", base_dir=tmp_path)
    assert event_count("test-acme", base_dir=tmp_path) == 2


# ─────────────────────────────────────────────────────────────────────
# Total: 12 tests
# ─────────────────────────────────────────────────────────────────────
