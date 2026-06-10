"""Ops-autopilot routers must be registered in OpenAPI (founder cockpit wiring gate)."""

from __future__ import annotations

from api.main import create_app

_REQUIRED_OPS_AUTOPILOT_PATHS = (
    "/api/v1/ops-autopilot/founder/cockpit",
    "/api/v1/ops-autopilot/founder/daily-pack",
    "/api/v1/ops-autopilot/founder/strongest-plan",
    "/api/v1/ops-autopilot/founder/ceo-master-plan",
    "/api/v1/ops-autopilot/war-room/today-pack",
    "/api/v1/ops-autopilot/founder/full-autonomous-ops",
)


def test_ops_autopilot_routes_in_openapi() -> None:
    app = create_app()
    paths = set(app.openapi().get("paths", {}).keys())
    missing = [p for p in _REQUIRED_OPS_AUTOPILOT_PATHS if p not in paths]
    assert not missing, f"ops-autopilot routes missing from OpenAPI: {missing}"
