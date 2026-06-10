"""Smoke test for marketing queue-approval → Approval Center."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-queue-approval-key")
    return TestClient(app)


def test_marketing_queue_approval_creates_pending(client: TestClient) -> None:
    headers = {"X-Admin-API-Key": "test-queue-approval-key"}
    r = client.post("/api/v1/ops-autopilot/marketing/queue-approval", headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("ok") is True
    assert body.get("approval_id")
