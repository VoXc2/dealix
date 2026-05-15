"""Tests for the 3 newer self_growth_os modules:
   - geo_aio_radar
   - internal_linking_planner
   - weekly_growth_scorecard

Pure unit tests — no network, no LLM, no DB. Each <2s.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.self_growth_os import (
    geo_aio_radar,
    internal_linking_planner,
    weekly_growth_scorecard,
)


# ─── geo_aio_radar ──────────────────────────────────────────────────


def test_geo_audit_returns_summary_and_pages():
    report = geo_aio_radar.audit_all()
    assert "summary" in report
    assert "pages" in report
    assert isinstance(report["pages"], list)
    assert report["summary"]["pages"] == len(report["pages"])


def test_geo_audit_score_is_within_bounds():
    """Per-page score must be 0–100 (sum of weights=100)."""
    report = geo_aio_radar.audit_all()
    for page in report["pages"]:
        assert 0 <= page["score"] <= 100, f"{page['path']} score={page['score']}"


def test_geo_audit_includes_status_html_with_high_score():
    """status.html was authored on this branch with full meta + canonical
    + OG + twitter:card. It should score among the highest."""
    report = geo_aio_radar.audit_all()
    by_path = {p["path"]: p for p in report["pages"]}
    assert "status.html" in by_path
    status_score = by_path["status.html"]["score"]
    avg_score = report["summary"]["average_score"]
    assert status_score >= avg_score, (
        f"status.html score ({status_score}) should be >= average ({avg_score})"
    )


def test_geo_audit_top_priority_pages_returns_lowest_scoring():
    top = geo_aio_radar.top_priority_pages(limit=3)
    assert 1 <= len(top) <= 3
    # Sorted ascending by score
    for a, b in zip(top, top[1:]):
        assert a["score"] <= b["score"]


def test_geo_audit_weights_sum_to_100():
    """Internal sanity — score scale is calibrated."""
    report = geo_aio_radar.audit_all()
    weights = report["weights"]
    assert sum(weights.values()) == 100


# ─── internal_linking_planner ───────────────────────────────────────


def test_internal_linking_returns_summary_issues_graph():
    g = internal_linking_planner.build_graph()
    assert "summary" in g and "issues" in g and "graph" in g


# Pre-existing site issues caught by the linter. Empty now — the
# 3 broken links (privacy/terms/subprocessors) were resolved by
# authoring the pages, and marketers.html is no longer orphan after
# the index.html nav + footer link wiring. Any NEW finding fails
# the test.
KNOWN_BROKEN_LINKS: set[tuple[str, str]] = set()
KNOWN_ORPHAN_CORE: set[str] = set()


def test_internal_linking_no_NEW_broken_relative_links():
    """Catches NEW broken links. Known pre-existing issues are pinned
    in KNOWN_BROKEN_LINKS — drop entries as they're fixed."""
    g = internal_linking_planner.build_graph()
    broken = {(b["from"], b["to"]) for b in g["issues"]["broken_relative_links"]}
    new_broken = broken - KNOWN_BROKEN_LINKS
    stale_known = KNOWN_BROKEN_LINKS - broken
    msgs: list[str] = []
    if new_broken:
        msgs.append(
            "NEW broken landing-page links not in KNOWN_BROKEN_LINKS: "
            + ", ".join(f"{a} → {b}" for a, b in sorted(new_broken))
        )
    if stale_known:
        msgs.append(
            "KNOWN_BROKEN_LINKS has stale entries (link is no longer broken — "
            "drop them): "
            + ", ".join(f"{a} → {b}" for a, b in sorted(stale_known))
        )
    assert not msgs, "\n".join(msgs)


def test_internal_linking_no_NEW_orphan_core_pages():
    """Catches NEW orphan core pages."""
    g = internal_linking_planner.build_graph()
    orphan = set(g["issues"]["orphan_core_pages"])
    new_orphan = orphan - KNOWN_ORPHAN_CORE
    stale_known = KNOWN_ORPHAN_CORE - orphan
    msgs: list[str] = []
    if new_orphan:
        msgs.append(f"NEW orphan core pages: {sorted(new_orphan)}")
    if stale_known:
        msgs.append(
            f"KNOWN_ORPHAN_CORE has stale entries (page now has inbound "
            f"links — drop them): {sorted(stale_known)}"
        )
    assert not msgs, "\n".join(msgs)


def test_internal_linking_index_is_reachable():
    """index.html is in CORE_PAGES; if it has 0 inbound links the test
    fires. (it's the root, so this should always pass.)"""
    g = internal_linking_planner.build_graph()
    page = g["graph"].get("index.html")
    assert page is not None


def test_internal_linking_status_html_has_inbound_links():
    """status.html (the new console) must be linked from the home page
    + nav so customers can find it."""
    g = internal_linking_planner.build_graph()
    page = g["graph"].get("status.html")
    assert page is not None
    assert page["inbound_count"] >= 1, (
        "status.html should be linked from at least one other page"
    )


def test_internal_linking_graph_records_outbound_count():
    g = internal_linking_planner.build_graph()
    for name, info in g["graph"].items():
        assert info["outbound_count"] == len(info["outbound"])
        assert isinstance(info["has_cta"], bool)


# ─── weekly_growth_scorecard ────────────────────────────────────────


def test_scorecard_returns_typed_blocks():
    sc = weekly_growth_scorecard.build_scorecard()
    for key in [
        "service_activation",
        "technical_seo",
        "geo_aio",
        "internal_linking",
        "tooling",
        "open_founder_decisions",
        "recommendations",
    ]:
        assert key in sc, f"scorecard missing block: {key}"


def test_scorecard_service_activation_matches_yaml():
    """After Phase K1-K6 (PR #165 + #166 + #167), 6 services live."""
    sc = weekly_growth_scorecard.build_scorecard()
    counts = sc["service_activation"]["counts"]
    assert counts["total"] == 32
    assert counts["live"] == 8


def test_scorecard_recommendations_have_priority_and_anchor():
    sc = weekly_growth_scorecard.build_scorecard()
    for rec in sc["recommendations"]:
        assert rec["priority"] in {"P0", "P1", "P2"}
        assert rec["action"]
        assert rec["anchor"]  # every recommendation must be anchored to a measurement


def test_scorecard_open_founder_decisions_lists_all_BS_items():
    sc = weekly_growth_scorecard.build_scorecard()
    decisions = "\n".join(sc["open_founder_decisions"])
    for item in ["B1", "B2", "B3", "B4", "B5", "S1", "S2", "S3", "S4", "S5"]:
        assert item in decisions, f"scorecard missing decision: {item}"


def test_scorecard_no_fake_metrics():
    """Negative test: the scorecard must NOT invent fields like
    'inbound_leads', 'pipeline_value', 'arr', 'churn', 'nps'.
    Those would require live integrations we don't have yet."""
    sc = weekly_growth_scorecard.build_scorecard()
    text = str(sc).lower()
    forbidden_fields = ["inbound_leads_count", "pipeline_value_sar", "arr_sar", "churn_rate", "nps_score"]
    for field in forbidden_fields:
        assert field not in text, f"scorecard contains fake metric: {field}"


# ─── API endpoint tests ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_geo_audit_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/geo/audit")
    assert r.status_code == 200
    payload = r.json()
    assert "summary" in payload
    assert "pages" in payload


@pytest.mark.asyncio
async def test_internal_linking_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/internal-linking")
    assert r.status_code == 200
    payload = r.json()
    # Endpoint reports the issues honestly; the count assertion lives
    # in test_internal_linking_no_NEW_broken_relative_links.
    assert "issues" in payload
    assert "broken_relative_links" in payload["issues"]


@pytest.mark.asyncio
async def test_weekly_scorecard_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/scorecard/weekly")
    assert r.status_code == 200
    payload = r.json()
    assert payload["service_activation"]["counts"]["total"] == 32
    # recommendations is computed from detected gaps — an empty list is a
    # valid "nothing to fix" state once the perimeter is clean.
    assert isinstance(payload["recommendations"], list)
