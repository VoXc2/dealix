"""Tenant stamping on POST /api/v1/revenue-os/events."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from starlette.testclient import TestClient

from api.main import app
from api.security.auth_deps import get_optional_user


def test_events_stamp_tenant_from_optional_auth():
    mock_user = MagicMock()
    mock_user.tenant_id = "ten_events_auth"

    mock_append = AsyncMock()

    app.dependency_overrides[get_optional_user] = lambda: mock_user
    try:
        with patch("api.routers.revenue_os.append_revenue_event", mock_append):
            client = TestClient(app)
            r = client.post(
                "/api/v1/revenue-os/events",
                json={
                    "event_type": "lead.created",
                    "customer_id": "cust_tenant_test",
                    "subject_type": "account",
                    "subject_id": "acc_1",
                    "payload": {},
                    "actor": "pytest",
                },
            )
        assert r.status_code == 200
        ev = mock_append.await_args.args[0]
        assert ev.tenant_id == "ten_events_auth"
    finally:
        app.dependency_overrides.pop(get_optional_user, None)
