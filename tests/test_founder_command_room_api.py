"""Tests for the Founder Command Room endpoint (GET /api/v1/founder/command-room).

Mounts the router in isolation (no DB / no full-app lifespan) so the test is
fast and self-contained. Guards the admin-key auth contract and the aggregated
snapshot shape, including that launch readiness reflects the live war-room
summary and the response stays draft-only and quote-only.
"""
from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.founder_command_room import router

PATH = "/api/v1/founder/command-room"
ADMIN_KEY = "founder-command-room-test-key"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    # Force a known admin key for this test regardless of any ADMIN_API_KEYS
    # already set in the CI environment. require_admin_key reads the env at
    # request time, so monkeypatch.setenv makes ADMIN_KEY the only valid key
    # for the duration of the test (auto-restored afterwards).
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_requires_admin_key(client: TestClient) -> None:
    assert client.get(PATH).status_code == 401
    assert client.get(PATH, headers={"X-Admin-API-Key": "wrong"}).status_code == 403


def test_snapshot_shape_and_launch_readiness(client: TestClient) -> None:
    r = client.get(PATH, headers={"X-Admin-API-Key": ADMIN_KEY})
    assert r.status_code == 200
    j = r.json()

    # Top-level aggregated contract.
    assert {"generated_at", "mode", "launch", "offer_ladder", "summary"} <= set(j)
    assert j["mode"] == "draft_only"

    # Compatibility ladder = 6 canonical commercial states; founder actions = 4 pending items.
    assert len(j["offer_ladder"]) == 6
    assert len(j["launch"]["founder_actions"]) == 4
    assert j["launch"]["article13_target"] == 3

    # The founder-facing path must never recreate a public fixed-price catalogue.
    rendered_ladder = repr(j["offer_ladder"])
    assert "Customer-Specific Quote" in rendered_ladder
    assert "Revenue Command Pilot" in rendered_ladder
    assert "Invoice ≠ Payment" in rendered_ladder
    for retired in (
        "Micro Sprint",
        "Data Pack",
        "Managed Ops",
        "Transformation Diagnostic Sprint",
        "Custom Enterprise System",
        "499 SAR",
        "1,500 SAR",
        "2,999",
        "4,999",
        "7,500",
        "25,000",
        "100,000",
    ):
        assert retired not in rendered_ladder

    # Launch readiness reflects the live war-room summary.
    summary = j["summary"]
    assert {"today", "revenue", "queues", "risks", "top_targets"} <= set(summary)
    assert j["launch"]["paid"] == summary["revenue"]["paid"]

    # Doctrine flags surface to the UI and stay enforced.
    assert summary["risks"]["no_live_auto_send"] is True
    assert summary["risks"]["no_cold_whatsapp"] is True
