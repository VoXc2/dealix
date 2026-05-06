"""Sales OS — pilot draft and qualify stub."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_sales_os_qualify() -> None:
    c = TestClient(create_app())
    r = c.post("/api/v1/sales-os/qualify", json={"fit": "strong"})
    assert r.status_code == 200
    assert r.json()["action_mode"] == "suggest_only"
