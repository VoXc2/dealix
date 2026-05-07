"""Phase 4 — Weakness Radar tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.full_ops_radar import detect_weaknesses


def test_detect_weaknesses_returns_list() -> None:
    weaknesses = detect_weaknesses()
    assert isinstance(weaknesses, list)


def test_each_weakness_has_required_fields() -> None:
    weaknesses = detect_weaknesses()
    required_fields = {
        "id", "layer", "severity", "blocker",
        "reason_ar", "reason_en", "fix_ar", "fix_en", "owner_role",
    }
    for w in weaknesses:
        missing = required_fields - set(w.keys())
        assert not missing, f"weakness {w.get('id')} missing fields: {missing}"


def test_weaknesses_sorted_by_severity() -> None:
    weaknesses = detect_weaknesses()
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    severities = [severity_order.get(w["severity"], 4) for w in weaknesses]
    assert severities == sorted(severities)


def test_severity_values_valid() -> None:
    weaknesses = detect_weaknesses()
    valid = {"low", "medium", "high", "critical"}
    for w in weaknesses:
        assert w["severity"] in valid


def test_each_weakness_has_bilingual_text() -> None:
    weaknesses = detect_weaknesses()
    for w in weaknesses:
        # Arabic must contain at least one Arabic char or be valid Arabic-style text
        assert len(w["reason_ar"]) >= 5
        assert len(w["reason_en"]) >= 5
        assert len(w["fix_ar"]) >= 5
        assert len(w["fix_en"]) >= 5


@pytest.mark.asyncio
async def test_weaknesses_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/full-ops-radar/weaknesses")
    assert r.status_code == 200
    body = r.json()
    assert "count" in body
    assert "critical_count" in body
    assert "weaknesses" in body
    assert body["hard_gates"]["no_fake_proof"] is True


@pytest.mark.asyncio
async def test_weaknesses_endpoint_no_500_on_empty_state() -> None:
    """Even with an unknown customer handle, no 500."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/full-ops-radar/weaknesses?customer_handle=ghost-xyz")
    assert r.status_code == 200


def test_detect_weaknesses_never_raises_on_unknown_customer() -> None:
    """Defensive: any input shouldn't blow up."""
    weaknesses = detect_weaknesses(customer_handle="non-existent-xyz")
    assert isinstance(weaknesses, list)
