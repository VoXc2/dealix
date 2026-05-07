"""Phase 4 — Full-Ops Score tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.full_ops_radar import (
    SCORE_WEIGHTS,
    compute_full_ops_score,
    readiness_label,
    run_all_health_checks,
)


def test_score_weights_sum_to_100() -> None:
    assert sum(SCORE_WEIGHTS.values()) == 100


def test_readiness_label_thresholds() -> None:
    assert readiness_label(95) == "Full Ops Ready"
    assert readiness_label(90) == "Full Ops Ready"
    assert readiness_label(89) == "Customer Ready with Manual Ops"
    assert readiness_label(75) == "Customer Ready with Manual Ops"
    assert readiness_label(74) == "Diagnostic Only"
    assert readiness_label(60) == "Diagnostic Only"
    assert readiness_label(59) == "Internal Only"
    assert readiness_label(0) == "Internal Only"


def test_score_returns_numeric_score() -> None:
    s = compute_full_ops_score()
    assert isinstance(s["score"], int)
    assert isinstance(s["max_score"], int)
    assert s["max_score"] == 100
    assert 0 <= s["score"] <= s["max_score"]
    assert s["readiness_label"] in (
        "Full Ops Ready", "Customer Ready with Manual Ops",
        "Diagnostic Only", "Internal Only",
    )


def test_score_breakdown_includes_all_layers() -> None:
    s = compute_full_ops_score()
    layers = {item["layer"] for item in s["breakdown"]}
    expected = set(SCORE_WEIGHTS.keys())
    assert layers == expected


def test_score_no_fake_green_when_module_missing() -> None:
    """Sanity: each layer's achieved score equals weight only if available."""
    s = compute_full_ops_score()
    for item in s["breakdown"]:
        if not item["available"]:
            assert item["achieved"] == 0


def test_health_checks_returns_10_layers() -> None:
    checks = run_all_health_checks()
    assert len(checks) == 10
    layers = {c["layer"] for c in checks}
    assert "leadops" in layers
    assert "safety_compliance" in layers


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/full-ops-radar/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "full_ops_radar"
    assert body["hard_gates"]["no_fake_green"] is True


@pytest.mark.asyncio
async def test_score_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/full-ops-radar/score")
    assert r.status_code == 200
    body = r.json()
    assert "score" in body
    assert "readiness_label" in body
    assert body["safety_summary"] == "no_fake_green_each_layer_verified_via_health_check"


@pytest.mark.asyncio
async def test_evidence_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/full-ops-radar/evidence")
    assert r.status_code == 200
    body = r.json()
    assert body["evidence_count"] == 10
    for e in body["evidence"]:
        assert "evidence_source" in e
        assert "available" in e
