"""Tests for scripts/v6_endpoint_perimeter.py.

We never hit production. Either we point the script at an in-process
FastAPI app spun up on an ephemeral port (live-server fixture pattern,
same as ``tests/test_dealix_smoke_test_cli.py``), or at a port nothing
is listening on, to exercise the unreachable branch.
"""
from __future__ import annotations

import io
import json
import sys
import threading
import time
from contextlib import contextmanager, redirect_stdout
from pathlib import Path

import pytest
import uvicorn

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
SCRIPT = SCRIPTS_DIR / "v6_endpoint_perimeter.py"


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import v6_endpoint_perimeter  # type: ignore[import-not-found]
        return v6_endpoint_perimeter
    finally:
        sys.path.pop(0)


# Endpoints required by the v6 Phase 1 spec — keep in lockstep with
# the script. If the script regresses, this test fails loud.
EXPECTED_PATHS: set[str] = {
    "/health",
    "/api/v1/customer-loop/status",
    "/api/v1/customer-data/status",
    "/api/v1/agent-governance/status",
    "/api/v1/delivery-factory/status",
    "/api/v1/proof-ledger/status",
    "/api/v1/finance/status",
    "/api/v1/gtm/status",
    "/api/v1/role-command/ceo",
    "/api/v1/role-command/sales",
    "/api/v1/reliability/status",
    "/api/v1/security-privacy/status",
    "/api/v1/vertical-playbooks/status",
    "/api/v1/founder/dashboard",
    "/api/v1/founder/status",
    "/api/v1/diagnostic/status",
    "/api/v1/company-brain/status",
    "/api/v1/search-radar/status",
    "/api/v1/self-growth/status",
    "/api/v1/self-growth/service-activation",
    "/api/v1/self-growth/seo/audit",
    "/api/v1/service-quality/status",
}


def test_script_exists_with_shebang():
    assert SCRIPT.exists(), f"missing {SCRIPT}"
    head = SCRIPT.read_text(encoding="utf-8").splitlines()[0]
    assert head == "#!/usr/bin/env python3", f"bad shebang: {head!r}"


def test_checks_list_covers_every_required_endpoint():
    mod = _import_module()
    paths = {c.path for c in mod.CHECKS}
    missing = EXPECTED_PATHS - paths
    assert not missing, f"perimeter is missing: {sorted(missing)}"
    # Every expected path is required (we don't quietly downgrade
    # any route to optional).
    for c in mod.CHECKS:
        if c.path in EXPECTED_PATHS:
            assert c.required is True, f"{c.path} should be required"
            assert c.expected_status == 200, (
                f"{c.path} should expect 200, got {c.expected_status}"
            )


def test_unreachable_base_url_returns_exit_2():
    mod = _import_module()
    # Capture stdout so test output stays clean.
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = mod.main([
            "--base-url", "http://127.0.0.1:1",
            "--timeout", "1",
            "--json",
        ])
    assert rc == 2, f"expected 2, got {rc}; stdout: {buf.getvalue()[:300]}"


@contextmanager
def _live_server(app, host: str = "127.0.0.1", port: int = 0):
    """Bind the FastAPI app on an ephemeral port for one test."""
    config = uvicorn.Config(
        app, host=host, port=port,
        log_level="warning", access_log=False,
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.time() + 10
    try:
        while time.time() < deadline:
            if server.started and server.servers:
                socks = server.servers[0].sockets
                if socks:
                    actual_port = socks[0].getsockname()[1]
                    yield f"http://{host}:{actual_port}"
                    return
            time.sleep(0.1)
        raise RuntimeError("uvicorn server failed to bind in time")
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_in_process_app_exits_zero_with_all_required_passing():
    from api.main import create_app
    mod = _import_module()
    app = create_app()
    with _live_server(app) as base_url:
        report = mod.run(base_url, timeout=30)
    failed = [r for r in report["results"] if not r["ok"]]
    assert report["failed_required"] == 0, f"unexpected failures: {failed}"
    assert report["passed_required"] == report["total"], (
        f"passed_required ({report['passed_required']}) != "
        f"total ({report['total']}); failed: {failed}"
    )
    assert report["passed"] == report["total"]


def test_json_output_has_expected_shape():
    """--json mode must emit total / passed / failed_required / results,
    and each result row must carry the documented per-row shape."""
    mod = _import_module()
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = mod.main([
            "--base-url", "http://127.0.0.1:1",
            "--timeout", "1",
            "--json",
        ])
    assert rc == 2
    payload = json.loads(buf.getvalue())
    for top_key in ("total", "passed", "failed_required", "results"):
        assert top_key in payload, f"missing top-level key: {top_key}"
    assert payload["total"] == len(mod.CHECKS)
    assert isinstance(payload["results"], list)
    assert payload["results"], "results array must not be empty"
    for row in payload["results"]:
        for row_key in (
            "path", "expected_status", "actual_status", "ok", "elapsed_ms",
        ):
            assert row_key in row, f"row missing key: {row_key} in {row}"
        assert isinstance(row["path"], str)
        assert isinstance(row["expected_status"], int)
        assert isinstance(row["ok"], bool)
        assert isinstance(row["elapsed_ms"], (int, float))


def test_render_text_is_bilingual():
    mod = _import_module()
    fake = {
        "schema_version": 1,
        "generated_at": "2026-01-01T00:00:00+00:00",
        "base_url": "http://example",
        "total": 1,
        "passed": 1,
        "passed_required": 1,
        "failed_required": 0,
        "results": [{
            "path": "/health",
            "expected_status": 200,
            "actual_status": 200,
            "ok": True,
            "elapsed_ms": 1.2,
            "required": True,
            "detail": "",
        }],
    }
    text = mod.render_text(fake)
    # Arabic + English headers must both be present (bilingual rule).
    assert "v6 endpoint perimeter check" in text
    assert "محيط" in text  # Arabic for "perimeter"
    assert "PASS" in text
    assert "VERDICT" in text
