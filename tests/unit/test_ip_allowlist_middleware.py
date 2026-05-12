"""Unit tests for api/middleware/ip_allowlist.py."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

from api.middleware.ip_allowlist import IPAllowlistMiddleware


class _FakeRequest:
    def __init__(
        self,
        path: str,
        allowlist: list[str] | None,
        client_ip: str | None = "10.0.0.5",
        xff: str | None = None,
    ) -> None:
        self.url = SimpleNamespace(path=path)
        self.state = SimpleNamespace(ip_allowlist=allowlist, tenant_id="t1")
        self.client = SimpleNamespace(host=client_ip) if client_ip else None
        self.headers = {"x-forwarded-for": xff} if xff else {}


async def _call(mw: IPAllowlistMiddleware, request: _FakeRequest) -> tuple[int, str]:
    captured = {}

    async def _next(_req: _FakeRequest):
        captured["ok"] = True
        return SimpleNamespace(status_code=200)

    resp = await mw.dispatch(request, _next)  # type: ignore[arg-type]
    body = b""
    if hasattr(resp, "body"):
        body = resp.body
    return resp.status_code, body.decode("utf-8", "replace") if isinstance(body, bytes) else ""


def test_public_path_bypasses_allowlist() -> None:
    mw = IPAllowlistMiddleware(app=None)
    req = _FakeRequest("/api/v1/public/lead-capture", allowlist=["10.0.0.0/24"], client_ip="1.2.3.4")
    code, _ = asyncio.run(_call(mw, req))
    assert code == 200


def test_health_path_bypasses_allowlist() -> None:
    mw = IPAllowlistMiddleware(app=None)
    req = _FakeRequest("/healthz", allowlist=["10.0.0.0/24"], client_ip="1.2.3.4")
    code, _ = asyncio.run(_call(mw, req))
    assert code == 200


def test_no_allowlist_passes_through() -> None:
    mw = IPAllowlistMiddleware(app=None)
    req = _FakeRequest("/api/v1/customers/me", allowlist=None, client_ip="1.2.3.4")
    code, _ = asyncio.run(_call(mw, req))
    assert code == 200


def test_ip_in_allowlist_allowed() -> None:
    mw = IPAllowlistMiddleware(app=None)
    req = _FakeRequest("/api/v1/leads", allowlist=["10.0.0.0/24"], client_ip="10.0.0.5")
    code, _ = asyncio.run(_call(mw, req))
    assert code == 200


def test_ip_outside_allowlist_403() -> None:
    mw = IPAllowlistMiddleware(app=None)
    req = _FakeRequest("/api/v1/leads", allowlist=["10.0.0.0/24"], client_ip="8.8.8.8")
    code, body = asyncio.run(_call(mw, req))
    assert code == 403
    assert "ip_not_allowlisted" in body


def test_xff_header_is_respected() -> None:
    mw = IPAllowlistMiddleware(app=None)
    req = _FakeRequest(
        "/api/v1/leads",
        allowlist=["192.168.1.0/24"],
        client_ip="10.0.0.5",
        xff="192.168.1.42, 10.0.0.5",
    )
    code, _ = asyncio.run(_call(mw, req))
    assert code == 200


def test_unknown_ip_403() -> None:
    mw = IPAllowlistMiddleware(app=None)
    req = _FakeRequest(
        "/api/v1/leads",
        allowlist=["10.0.0.0/24"],
        client_ip=None,
    )
    code, body = asyncio.run(_call(mw, req))
    assert code == 403
    assert "ip_unknown" in body
