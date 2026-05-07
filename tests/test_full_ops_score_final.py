"""Phase 5 — Full-Ops Score finalization tests.

Asserts:
- Score weights sum exactly to 100
- Readiness label thresholds match the spec exactly
- Every layer in SCORE_WEIGHTS appears in compute_full_ops_score breakdown
- No fake green when a module is missing
- Endpoint returns the documented response shape
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.full_ops_radar import (
    SCORE_WEIGHTS,
    compute_full_ops_score,
    readiness_label,
)


def test_score_weights_exactly_100() -> None:
    assert sum(SCORE_WEIGHTS.values()) == 100


def test_score_weights_match_spec() -> None:
    """Spec: LeadOps 15, others 10, Safety 5."""
    assert SCORE_WEIGHTS["leadops"] == 15
    assert SCORE_WEIGHTS["customer_brain"] == 10
    assert SCORE_WEIGHTS["service_sessions"] == 10
    assert SCORE_WEIGHTS["approval_center"] == 10
    assert SCORE_WEIGHTS["payment_ops"] == 10
    assert SCORE_WEIGHTS["support"] == 10
    assert SCORE_WEIGHTS["proof_ledger"] == 10
    assert SCORE_WEIGHTS["customer_portal"] == 10
    assert SCORE_WEIGHTS["executive_dashboard"] == 10
    assert SCORE_WEIGHTS["safety_compliance"] == 5


def test_readiness_label_exact_thresholds() -> None:
    """Spec thresholds: 90+, 75+, 60+, <60."""
    assert readiness_label(100) == "Full Ops Ready"
    assert readiness_label(90) == "Full Ops Ready"
    assert readiness_label(89) == "Customer Ready with Manual Ops"
    assert readiness_label(75) == "Customer Ready with Manual Ops"
    assert readiness_label(74) == "Diagnostic Only"
    assert readiness_label(60) == "Diagnostic Only"
    assert readiness_label(59) == "Internal Only"
    assert readiness_label(0) == "Internal Only"


def test_score_response_shape_complete() -> None:
    s = compute_full_ops_score()
    required_fields = {
        "score", "max_score", "percentage",
        "readiness_label", "breakdown", "weights_table",
        "safety_summary",
    }
    assert set(s.keys()) >= required_fields


def test_breakdown_includes_all_layers() -> None:
    s = compute_full_ops_score()
    layer_names = {item["layer"] for item in s["breakdown"]}
    assert layer_names == set(SCORE_WEIGHTS.keys())


def test_no_fake_green() -> None:
    """If a layer's module is missing, achieved must be 0 (not weight)."""
    s = compute_full_ops_score()
    for item in s["breakdown"]:
        if not item["available"]:
            assert item["achieved"] == 0


def test_safety_summary_documents_no_fake_green() -> None:
    s = compute_full_ops_score()
    assert "no_fake_green" in s["safety_summary"]


@pytest.mark.asyncio
async def test_score_endpoint_returns_complete_payload() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/full-ops-radar/score")
    assert r.status_code == 200
    body = r.json()
    assert "score" in body
    assert "readiness_label" in body
    assert "breakdown" in body
    assert "hard_gates" in body
    assert body["hard_gates"]["no_fake_green"] is True


@pytest.mark.asyncio
async def test_status_endpoint_lists_readiness_labels() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/full-ops-radar/status")
    body = r.json()
    labels = " ".join(body["readiness_labels"])
    assert "Full Ops Ready" in labels
    assert "Customer Ready with Manual Ops" in labels
    assert "Diagnostic Only" in labels
    assert "Internal Only" in labels
