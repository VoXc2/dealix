"""Smoke tests for commercial digest builder."""

from __future__ import annotations

from dealix.commercial_ops.digest import build_commercial_digest, render_digest_markdown


def test_build_commercial_digest_shape() -> None:
    digest = build_commercial_digest(skip_no_build=True)
    assert digest["schema_version"] in ("1.1", "1.2", "1.3", "1.4", "1.5")
    assert "evidence" in digest
    assert "war_room" in digest
    assert "market_intelligence" in digest
    assert isinstance(digest.get("today_focus_ar"), list)
    assert digest["today_focus_ar"]


def test_render_digest_markdown_contains_sections() -> None:
    digest = build_commercial_digest(skip_no_build=True)
    md = render_digest_markdown(digest)
    assert "War Room" in md or "غرفة" in md
    assert "evidence" in md.lower() or "أدلة" in md
    assert "استخبارات السوق" in md
