"""Tests for scripts/dealix_smoke_test.py.

We don't hit production. Instead we run the smoke test against the
local FastAPI app via TestClient and assert the report comes back
with the expected structure + verdict.
"""
from __future__ import annotations

import os
import sys
import threading
import time
from contextlib import contextmanager
from pathlib import Path

import pytest
import uvicorn

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_smoke_test.py"


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_smoke_test  # type: ignore[import-not-found]
        return dealix_smoke_test
    finally:
        sys.path.pop(0)


def test_smoke_script_exists_and_has_shebang():
    assert SCRIPT.exists()
    assert SCRIPT.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3")


def test_checks_list_has_all_v5_layers():
    """The CHECKS list MUST cover all 12 v5 layers + Phase I founder."""
    mod = _import_module()
    paths = {c.path for c in mod.CHECKS}
    expected_status_endpoints = {
        "/api/v1/customer-loop/status",
        "/api/v1/role-command/status",
        "/api/v1/service-quality/status",
        "/api/v1/agent-governance/status",
        "/api/v1/reliability/status",
        "/api/v1/vertical-playbooks/status",
        "/api/v1/customer-data/status",
        "/api/v1/finance/status",
        "/api/v1/delivery-factory/status",
        "/api/v1/proof-ledger/status",
        "/api/v1/gtm/status",
        "/api/v1/security-privacy/status",
        # Phase I aggregate
        "/api/v1/founder/dashboard",
    }
    missing = expected_status_endpoints - paths
    assert not missing, f"smoke test missing checks for: {missing}"


def test_smoke_run_against_unreachable_url_returns_exit_2():
    """If the deploy isn't reachable at all, exit 2 (not 1)."""
    mod = _import_module()
    rc = mod.main([
        "--base-url", "http://127.0.0.1:1",  # nothing listens on port 1
        "--timeout", "1",
        "--json",
    ])
    assert rc == 2


@contextmanager
def _live_server(app, host: str = "127.0.0.1", port: int = 0):
    """Spin up the FastAPI app on an ephemeral port for one test."""
    config = uvicorn.Config(
        app, host=host, port=port,
        log_level="warning", access_log=False,
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    # Wait for the server to bind to a port (started + servers available)
    deadline = time.time() + 10
    while time.time() < deadline:
        if server.started and server.servers:
            socks = server.servers[0].sockets
            if socks:
                actual_port = socks[0].getsockname()[1]
                yield f"http://{host}:{actual_port}"
                server.should_exit = True
                thread.join(timeout=5)
                return
        time.sleep(0.1)
    server.should_exit = True
    thread.join(timeout=5)
    raise RuntimeError("uvicorn server failed to bind in time")


def test_smoke_against_local_app_passes_all_required():
    """Run the smoke test against the in-process FastAPI app — all
    required checks should pass with verdict 0."""
    from api.main import create_app
    mod = _import_module()
    app = create_app()
    with _live_server(app) as base_url:
        report = mod.run(base_url, timeout=10)
    assert report["failed_required"] == 0, (
        f"failures: "
        f"{[r for r in report['results'] if not r['ok']]}"
    )
    assert report["passed"] == report["total"]


def test_smoke_render_text_includes_verdict():
    mod = _import_module()
    fake_report = {
        "schema_version": 1,
        "generated_at": "2026-01-01T00:00:00+00:00",
        "base_url": "http://example",
        "total": 1,
        "passed": 1,
        "failed_required": 0,
        "results": [{
            "name": "ping",
            "method": "GET",
            "path": "/health",
            "required": True,
            "status": 200,
            "elapsed_ms": 5.0,
            "ok": True,
            "detail": "",
        }],
    }
    text = mod.render_text(fake_report)
    assert "Dealix smoke test" in text
    assert "all required checks passed" in text
