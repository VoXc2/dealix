"""Daily command center facade — shape and safety."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def _client() -> TestClient:
    return TestClient(create_app())


def test_daily_command_center_returns_200_and_required_keys() -> None:
    c = _client()
    r = c.get("/api/v1/full-ops/daily-command-center")
    assert r.status_code == 200
    body = r.json()
    for key in (
        "today_top_3_decisions",
        "growth_queue",
        "sales_queue",
        "support_queue",
        "delivery_queue",
        "cs_queue",
        "partner_queue",
        "compliance_alerts",
        "executive_summary",
        "blocked_actions",
        "proof_summary",
        "next_best_actions",
        "hard_gates",
        "degraded_sections",
        "revenue_execution_next_step",
    ):
        assert key in body
    assert isinstance(body["today_top_3_decisions"], list)
    assert len(body["today_top_3_decisions"]) == 3
    gates = body["hard_gates"]
    assert gates.get("NO_LIVE_SEND") is True
    assert gates.get("NO_COLD_WHATSAPP") is True
    assert "live_whatsapp_outbound" in body["blocked_actions"]


def test_full_ops_status() -> None:
    c = _client()
    r = c.get("/api/v1/full-ops/status")
    assert r.status_code == 200
    assert r.json().get("module") == "revenue_execution"
