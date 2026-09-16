"""Smoke tests for commercial digest builder."""

from __future__ import annotations

from dealix.commercial_ops.digest import build_commercial_digest, render_digest_markdown


def test_build_commercial_digest_shape() -> None:
    digest = build_commercial_digest(skip_no_build=True)
    assert digest["schema_version"] in ("1.1", "1.2", "1.3", "1.4", "1.5", "1.6")
    assert "evidence" in digest
    assert "war_room" in digest
    assert "market_intelligence" in digest
    assert "official_source_watch" in digest["market_intelligence"]
    assert digest["market_intelligence"]["official_source_watch"]["authority"]["pipeline"] is False
    assert isinstance(digest.get("today_focus_ar"), list)
    assert digest["today_focus_ar"]



def test_digest_focus_never_fabricates_approvals_partners_or_evidence_counts() -> None:
    digest = build_commercial_digest(skip_no_build=True)
    focus = "\n".join(digest["today_focus_ar"])
    assert "10 لمسات موافَق عليها" not in focus
    assert "1 شريك" not in focus
    assert "1 حدث أدلة" not in focus
    assert "لا تثبت علاقة أو موافقة أو فرصة تجارية" in focus
    assert "send/publish/payment" in focus
    expected = f"أحداث الأدلة الموثقة اليوم: {int(digest['evidence'].get('today_total') or 0)}"
    assert expected in focus


def test_render_digest_markdown_contains_sections() -> None:
    digest = build_commercial_digest(skip_no_build=True)
    md = render_digest_markdown(digest)
    assert "War Room" in md or "غرفة" in md
    assert "evidence" in md.lower() or "أدلة" in md
    assert "استخبارات السوق" in md
    assert "Research ≠ Relationship" in md
    assert "Signal ≠ Pipeline" in md
