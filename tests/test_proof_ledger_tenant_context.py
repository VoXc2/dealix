"""Proof ledger stamps dealix_tenant_id when JWT user present."""

from __future__ import annotations

from unittest.mock import MagicMock

from starlette.testclient import TestClient

from api.main import app
from api.security.auth_deps import get_optional_user


def test_proof_event_payload_gets_tenant_from_auth():
    mock_user = MagicMock()
    mock_user.tenant_id = "ten_proof_test"

    app.dependency_overrides[get_optional_user] = lambda: mock_user
    try:
        client = TestClient(app)
        r = client.post(
            "/api/v1/proof-ledger/events",
            json={
                "event_type": "lead_intake",
                "payload": {"note": "unit"},
            },
        )
        assert r.status_code == 200
        data = r.json()
        assert data.get("payload", {}).get("dealix_tenant_id") == "ten_proof_test"
    finally:
        app.dependency_overrides.pop(get_optional_user, None)
