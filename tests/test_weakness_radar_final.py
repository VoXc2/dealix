"""Phase 5 — Weakness Radar finalization tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.full_ops_radar import detect_weaknesses


def test_detect_weaknesses_returns_list() -> None:
    weaknesses = detect_weaknesses()
    assert isinstance(weaknesses, list)


def test_each_weakness_has_required_8_fields() -> None:
    """Spec: id, layer, severity, blocker, reason_ar, reason_en, fix_ar,
    fix_en, owner_role + optional related_endpoint, related_doc."""
    weaknesses = detect_weaknesses()
    required = {
        "id", "layer", "severity", "blocker",
        "reason_ar", "reason_en", "fix_ar", "fix_en", "owner_role",
    }
    for w in weaknesses:
        missing = required - set(w.keys())
        assert not missing, f"weakness {w.get('id')} missing: {missing}"


def test_severity_values_documented() -> None:
    weaknesses = detect_weaknesses()
    valid = {"low", "medium", "high", "critical"}
    for w in weaknesses:
        assert w["severity"] in valid


def test_severity_sorted() -> None:
    weaknesses = detect_weaknesses()
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    severities = [order.get(w["severity"], 4) for w in weaknesses]
    assert severities == sorted(severities)


@pytest.mark.asyncio
async def test_weaknesses_endpoint_with_customer_handle() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/full-ops-radar/weaknesses?customer_handle=wr-final")
    assert r.status_code == 200
    body = r.json()
    assert "count" in body
    assert "critical_count" in body
    assert "weaknesses" in body
    assert isinstance(body["weaknesses"], list)


@pytest.mark.asyncio
async def test_evidence_endpoint_traces_every_layer() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/full-ops-radar/evidence")
    body = r.json()
    assert body["evidence_count"] == 10
    for e in body["evidence"]:
        assert "evidence_source" in e
        assert "evidence_kind" in e
