"""Regression coverage for the active commercial runtime authority surfaces."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord
from dealix.revenue_ops_autopilot.store import reset_autopilot_store_for_tests

_ADMIN = {"X-Admin-API-Key": "dev"}
_RETIRED_PATHS = {
    "/api/v1/public/services",
    "/api/v1/ops-autopilot/leads/{lead_id}/meeting-brief",
    "/api/v1/invoices/draft",
}


def _collect_paths(routes: object, parent_prefix: str = "") -> list[str]:
    """Collect effective paths across old flat and FastAPI >=0.137 router trees."""
    paths: list[str] = []
    for route in routes:  # type: ignore[union-attr]
        if type(route).__name__ == "_IncludedRouter":
            ctx = getattr(route, "include_context", None)
            prefix = (getattr(ctx, "prefix", "") or "") if ctx is not None else ""
            original_router = getattr(route, "original_router", None)
            if original_router is not None:
                paths.extend(
                    _collect_paths(original_router.routes, parent_prefix + prefix)
                )
            continue
        path = getattr(route, "path", "")
        if path:
            paths.append(parent_prefix + path)
    return paths


@pytest.fixture(autouse=True)
def _isolated_autopilot_store() -> None:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        p = Path(fh.name)
    store = reset_autopilot_store_for_tests(path=p)
    yield
    store._path.unlink(missing_ok=True)


def test_legacy_autopilot_commercial_routes_are_quarantined() -> None:
    from api.main import app
    from api.routers.revenue_ops_autopilot import AUTOPILOT_ROUTERS

    legacy_paths = {
        getattr(route, "path", "")
        for router in AUTOPILOT_ROUTERS
        for route in router.routes
    }
    assert _RETIRED_PATHS.isdisjoint(legacy_paths)

    active_paths = _collect_paths(app.routes)
    for path in _RETIRED_PATHS:
        assert active_paths.count(path) == 1, path


def test_public_services_exposes_quote_only_30_day_pilot() -> None:
    from api.main import app

    cli = TestClient(app)
    r = cli.get("/api/v1/public/services")
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["entry_offer"]["id"] == "free_mini_diagnostic"
    assert data["primary_offer"]["id"] == "revenue_command_pilot_30d"
    assert data["primary_offer"]["duration_days"] == 30
    assert data["primary_offer"]["price_model"] == "customer_specific_quote_only"
    assert data["primary_offer"]["public_fixed_pricing"] is False
    assert data["primary_offer"]["public_checkout"] is False

    text = json.dumps(data, ensure_ascii=False)
    for retired in (
        "seven_day_governance_diagnostic",
        "tiers_sar",
        "4999",
        "9999",
        "15000",
        "تشخيص ٧ أيام",
    ):
        assert retired not in text


def test_meeting_brief_ignores_retired_lead_offer_and_routes_canonical() -> None:
    from api.main import app
    from dealix.revenue_ops_autopilot.store import get_autopilot_store

    store = get_autopilot_store()
    store.upsert_lead(
        FunnelLeadRecord(
            id="lead_runtime_truth",
            company="Acme",
            pain="revenue handoff gap",
            stage="meeting_done",
            offer_id="seven_day_governance_diagnostic",
        ),
    )

    cli = TestClient(app)
    r = cli.get(
        "/api/v1/ops-autopilot/leads/lead_runtime_truth/meeting-brief",
        headers=_ADMIN,
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["entry_offer"] == "free_mini_diagnostic"
    assert data["recommended_offer"] == "revenue_command_pilot_30d"
    assert data["offer_route"] == [
        "FREE_MINI_DIAGNOSTIC",
        "QUALIFIED_DISCOVERY",
        "CUSTOMER_SPECIFIC_QUOTE",
        "REVENUE_COMMAND_PILOT_30D",
    ]
    text = json.dumps(data, ensure_ascii=False)
    assert "seven_day_governance_diagnostic" not in text
    assert "٧ أيام" not in text
    assert "7-Day" not in text
