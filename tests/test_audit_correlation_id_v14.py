"""V14 Phase K3 — audit-trail correlation_id full-coverage test.

Closes the registry gap: `audit_trail` status `partial` → `live`.

Existing infrastructure (api/middleware/http_stack.py:RequestIDMiddleware):
- Every incoming request gets a unique request_id (X-Request-ID header
  or auto-generated 12-char hex)
- Bound to structlog contextvars → every log emitted during the
  request shares the same request_id
- Echoed back as X-Request-ID response header

This test verifies the registry's `next_activation_step_en` for
audit_trail: "Unify correlation_id across all paths and add a
full-coverage test."

Asserts:
  1. Every endpoint surfaces an X-Request-ID response header.
  2. A client-supplied X-Request-ID is preserved (not overwritten).
  3. Two distinct requests get distinct correlation IDs.
  4. The same correlation ID appears across multiple endpoints when
     the client supplies it explicitly (cross-service tracing).
  5. Auto-generated IDs are 12-char hex (compact, log-friendly).
"""
from __future__ import annotations

import re
import pytest
from httpx import ASGITransport, AsyncClient


HEX12 = re.compile(r"^[0-9a-f]{12}$")


@pytest.mark.asyncio
async def test_response_carries_x_request_id_header() -> None:
    """Every 2xx response from any router must have X-Request-ID set."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health")
    assert r.status_code == 200
    assert "x-request-id" in {k.lower() for k in r.headers.keys()}
    rid = r.headers.get("X-Request-ID")
    assert rid
    assert HEX12.match(rid), f"auto-generated request_id should be 12-char hex; got {rid!r}"


@pytest.mark.asyncio
async def test_client_supplied_x_request_id_is_preserved() -> None:
    """If the client sends an X-Request-ID header, the middleware
    must echo it back unchanged (cross-service tracing primitive)."""
    from api.main import app

    transport = ASGITransport(app=app)
    custom_id = "trace-abc-12345-deadbeef"
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health", headers={"X-Request-ID": custom_id})
    assert r.status_code == 200
    assert r.headers.get("X-Request-ID") == custom_id


@pytest.mark.asyncio
async def test_two_independent_requests_get_distinct_ids() -> None:
    """Without a client-supplied X-Request-ID, every request must
    receive a fresh auto-generated ID — never reused across requests."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r1 = await client.get("/health")
        r2 = await client.get("/health")
    rid1 = r1.headers.get("X-Request-ID")
    rid2 = r2.headers.get("X-Request-ID")
    assert rid1
    assert rid2
    assert rid1 != rid2, "Each request must get a fresh correlation_id"


@pytest.mark.asyncio
async def test_correlation_id_propagates_across_distinct_endpoints() -> None:
    """The same client-supplied correlation_id must flow through every
    endpoint we hit — proving cross-service traceability for support
    debugging.

    Walks 5 distinct routers and asserts each one echoes the
    correlation_id back so a single trace can be reconstructed.
    """
    from api.main import app

    paths = [
        "/health",
        "/api/v1/founder/status",
        "/api/v1/growth-beast/status",
        "/api/v1/revops/status",
        "/api/v1/support-os/status",
    ]
    custom_id = "shared-trace-99zz77yy55"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for path in paths:
            r = await client.get(path, headers={"X-Request-ID": custom_id})
            # Some paths return 404 in test env (no full DB); we only
            # care about the correlation_id being preserved.
            echoed = r.headers.get("X-Request-ID")
            assert echoed == custom_id, (
                f"Endpoint {path} did not echo X-Request-ID "
                f"(got {echoed!r}, expected {custom_id!r})"
            )


@pytest.mark.asyncio
async def test_auto_request_id_is_compact_hex() -> None:
    """Auto-generated request_ids are 12-char lowercase hex — short
    enough to copy-paste from logs, long enough to be unique."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health")
    rid = r.headers.get("X-Request-ID")
    assert rid
    assert len(rid) == 12, f"auto request_id should be 12 chars; got {len(rid)}: {rid!r}"
    assert HEX12.match(rid), f"auto request_id should be lowercase hex; got {rid!r}"


@pytest.mark.asyncio
async def test_correlation_id_present_on_4xx_5xx_too() -> None:
    """When a request fails (404 / 422 / 500), the X-Request-ID
    header must STILL be set so the failed trace is debuggable.
    No silent loss of correlation."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # A path that almost certainly doesn't exist
        r = await client.get("/nonexistent-route-for-test-12345")
        # And a malformed POST that likely returns 422 / 405
        r2 = await client.post(
            "/api/v1/public/demo-request",
            json={},  # missing required fields
        )

    # Both responses MUST have X-Request-ID set — even on failures.
    assert "x-request-id" in {k.lower() for k in r.headers.keys()}, (
        "404 responses must still carry X-Request-ID for tracing"
    )
    assert "x-request-id" in {k.lower() for k in r2.headers.keys()}, (
        "422/4xx responses must still carry X-Request-ID for tracing"
    )
