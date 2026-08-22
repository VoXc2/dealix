"""Regression tests for read-only PR portfolio triage signals."""

from __future__ import annotations

import importlib.util
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "triage_open_prs.py"

_spec = importlib.util.spec_from_file_location("triage_open_prs", MODULE_PATH)
assert _spec and _spec.loader
triage = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(triage)

NOW = datetime(2026, 8, 2, tzinfo=UTC)


def _pr(number: int, title: str, updated: str, **overrides: object) -> dict:
    pr = {
        "number": number,
        "title": title,
        "updatedAt": updated,
        "createdAt": updated,
        "author": {"login": "VoXc2"},
        "labels": [],
        "isDraft": False,
        "baseRefName": "main",
        "headRefName": f"branch-{number}",
        "mergeStateStatus": "CLEAN",
        "url": f"https://example.invalid/{number}",
    }
    pr.update(overrides)
    return pr


def test_draft_bucket_remains_first_match() -> None:
    pr = _pr(
        1,
        "fix(security): rotate auth dependency",
        "2026-08-01T00:00:00Z",
        isDraft=True,
    )
    assert triage.classify(pr) == "draft"


def test_duplicate_titles_ignore_conventional_prefix_and_pr_reference() -> None:
    prs = [
        _pr(10, "feat(company): Add Company Command #900", "2026-08-01T00:00:00Z"),
        _pr(11, "fix: add company command", "2026-08-01T00:00:00Z"),
        _pr(12, "docs: Different topic", "2026-08-01T00:00:00Z"),
    ]
    groups = triage.duplicate_title_groups(prs)
    assert list(groups) == ["add company command"]
    assert [pr["number"] for pr in groups["add company command"]] == [10, 11]


def test_risk_flags_surface_staleness_conflict_duplicate_and_stack() -> None:
    pr = _pr(
        20,
        "feat: add company command",
        "2026-06-30T00:00:00Z",
        mergeStateStatus="DIRTY",
        baseRefName="feat/saas-foundation",
    )
    flags = triage.risk_flags(
        pr,
        duplicate_keys={"add company command"},
        now=NOW,
    )
    assert flags == [
        "stale_33d",
        "merge_conflict",
        "duplicate_title",
        "stacked_on:feat/saas-foundation",
    ]


def test_summary_counts_each_stale_pr_once() -> None:
    prs = [
        _pr(30, "feat: old one", "2026-06-01T00:00:00Z"),
        _pr(31, "fix: fresh one", "2026-07-20T00:00:00Z"),
    ]
    buckets = triage.build_buckets(prs)
    summary = triage.build_summary(prs, buckets, now=NOW)
    assert summary["stale_total"] == 1
    assert summary["conflicted_total"] == 0
    assert summary["duplicate_title_groups"] == []
    assert summary["items"][0]["age_days"] == 62


def test_markdown_exposes_portfolio_signals_without_disposition() -> None:
    prs = [
        _pr(40, "feat: Add loop verifier", "2026-06-01T00:00:00Z"),
        _pr(41, "fix: add loop verifier", "2026-08-01T00:00:00Z"),
    ]
    buckets = triage.build_buckets(prs)
    rendered = triage.render_markdown(buckets, len(prs), all_prs=prs, now=NOW)
    assert "Duplicate-title groups: 1" in rendered
    assert "stale_62d" in rendered
    assert "`add loop verifier`: #40, #41" in rendered
    assert "never merge or close PRs from triage output" in rendered
