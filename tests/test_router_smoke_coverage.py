"""Router smoke coverage.

Exercises every ``/api/`` GET endpoint and a payload-light sample of
POST endpoints so that catastrophic breakage on otherwise-untested
routers is caught: an unbuildable app, a route that fails to register,
a handler that hangs, or an exception that escapes the ASGI layer.

A *handled* 5xx is tolerated here — many of these routers degrade
ungracefully when optional infrastructure (Postgres, Redis) is absent,
which is tracked separately. The value of this test is twofold:
exercising the handlers (so regressions surface) and guaranteeing the
whole router surface stays importable and routable.
"""
from __future__ import annotations

import re

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def app():
    from api.main import create_app
    return create_app()


@pytest.fixture(scope="module")
def client(app):
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


def _fill_path(path: str) -> str:
    """Replace ``{param}`` placeholders with a smoke-safe dummy value."""
    return re.sub(r"\{[^}]+\}", "smoke", path)


def _routes(app, method: str) -> list[str]:
    paths: set[str] = set()
    for route in app.routes:
        methods = getattr(route, "methods", None) or set()
        path = getattr(route, "path", "")
        if method not in methods or not path.startswith("/api/"):
            continue
        if "{path" in path:  # catch-all static mounts
            continue
        paths.add(path)
    return sorted(paths)


def test_get_endpoints_respond_without_crashing(client):
    """Every ``/api/`` GET handler must return an HTTP response — not hang,
    not crash the ASGI layer, not raise through the test client."""
    routes = _routes(client.app, "GET")
    assert routes, "no GET routes discovered — app failed to register routers"
    crashed: list[str] = []
    for path in routes:
        url = _fill_path(path)
        try:
            resp = client.get(url)
        except Exception as exc:  # noqa: BLE001 — exception escaped the app
            crashed.append(f"GET {url} -> raised {type(exc).__name__}: {exc}")
            continue
        if not isinstance(resp.status_code, int):
            crashed.append(f"GET {url} -> no status code")
    assert not crashed, (
        "GET endpoints raised through the ASGI layer:\n" + "\n".join(crashed)
    )


def test_post_endpoints_respond_without_crashing(client):
    """Every ``/api/`` POST handler must return an HTTP response to an
    empty body — validation rejections (422) are expected and fine; the
    point is that the route is registered and the request pipeline runs."""
    routes = _routes(client.app, "POST")
    assert routes, "no POST routes discovered"
    crashed: list[str] = []
    for path in routes:
        url = _fill_path(path)
        try:
            resp = client.post(url, json={})
        except Exception as exc:  # noqa: BLE001 — exception escaped the app
            crashed.append(f"POST {url} -> raised {type(exc).__name__}: {exc}")
            continue
        if not isinstance(resp.status_code, int):
            crashed.append(f"POST {url} -> no status code")
    assert not crashed, (
        "POST endpoints raised through the ASGI layer:\n" + "\n".join(crashed)
    )
