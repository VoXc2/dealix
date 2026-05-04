"""Tests for the paid-beta staging readiness check.

These tests use httpx's MockTransport to simulate a staging deployment
without ever touching the network.
"""

from __future__ import annotations

import httpx
import pytest

from scripts.paid_beta_ready import (
    LATENCY_FAIL_MS,
    LATENCY_WARN_MS,
    PROBES,
    HttpProbe,
    ProbeResult,
    StagingReport,
    render,
    run_check,
)


BASE = "https://staging.example.test"


def _good_handler(request: httpx.Request) -> httpx.Response:
    """Default mock that returns 200s with bodies that satisfy probe expectations."""
    path = request.url.path
    if path == "/health":
        return httpx.Response(200, json={"status": "ok"})
    if path == "/":
        return httpx.Response(200, json={"version": "3.0.0", "env": "staging"})
    if path == "/docs":
        return httpx.Response(200, text="<html>FastAPI - Swagger UI</html>")
    if path.startswith("/api/v1/command-center/snapshot"):
        return httpx.Response(200, json={"ok": True})
    if path.startswith("/api/v1/personal-operator/daily-brief"):
        return httpx.Response(200, json={"brief": "..."})
    if path.startswith("/api/v1/v3/command-center/snapshot"):
        return httpx.Response(200, json={"ok": True})
    return httpx.Response(404, json={"error": "not_found"})


def _failing_health_handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/health":
        return httpx.Response(500, json={"status": "error"})
    return _good_handler(request)


def _missing_optional_handler(request: httpx.Request) -> httpx.Response:
    """Optional endpoints return 404 — still counts as PASS."""
    path = request.url.path
    if path.startswith("/api/v1/personal-operator/daily-brief"):
        return httpx.Response(404)
    if path.startswith("/api/v1/v3/command-center/snapshot"):
        return httpx.Response(404)
    return _good_handler(request)


@pytest.fixture
def patch_client(monkeypatch: pytest.MonkeyPatch):
    """Patch httpx.Client to use a MockTransport for the duration of a test."""

    def _install(handler):
        transport = httpx.MockTransport(handler)
        original_init = httpx.Client.__init__

        def patched_init(self, *args, **kwargs):  # type: ignore[no-untyped-def]
            kwargs["transport"] = transport
            original_init(self, *args, **kwargs)

        monkeypatch.setattr(httpx.Client, "__init__", patched_init)

    return _install


def test_run_check_all_green(patch_client) -> None:
    patch_client(_good_handler)
    report = run_check(BASE)
    assert isinstance(report, StagingReport)
    assert report.base_url == BASE
    assert report.passed, "expected PASS, got:\n" + render(report)
    assert all(r.passed for r in report.results)


def test_run_check_health_failure(patch_client) -> None:
    patch_client(_failing_health_handler)
    report = run_check(BASE)
    assert not report.passed
    health = next(r for r in report.results if r.probe.name == "health")
    assert not health.passed
    assert health.status == 500


def test_run_check_optional_404_still_passes(patch_client) -> None:
    patch_client(_missing_optional_handler)
    report = run_check(BASE)
    assert report.passed, "optional endpoints returning 404 must not fail the check"


def test_render_marks_result(patch_client) -> None:
    patch_client(_good_handler)
    report = run_check(BASE)
    text = render(report)
    assert "PAID_BETA_READY_CHECK" in text
    assert BASE in text
    assert ("PAID_BETA_READY" in text) or ("NOT_READY" in text)


def test_probes_have_expected_paths() -> None:
    paths = {p.path for p in PROBES}
    assert "/health" in paths
    assert "/" in paths
    assert "/docs" in paths
    assert "/api/v1/command-center/snapshot" in paths


def test_latency_thresholds_sane() -> None:
    assert 0 < LATENCY_WARN_MS < LATENCY_FAIL_MS


def test_probe_result_dataclass() -> None:
    p = HttpProbe(name="x", method="GET", path="/x")
    r = ProbeResult(probe=p, status=200, latency_ms=12.5, passed=True, detail="OK")
    assert r.passed
    assert r.latency_ms == 12.5
    assert r.probe.name == "x"


def test_required_probes_in_canonical_order() -> None:
    """Ensure /health is the first probe (so failures fail fast)."""
    assert PROBES[0].name == "health"
