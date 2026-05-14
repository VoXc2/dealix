"""Post-Merge Smoke — Wave 19+ Operational Closure.

Verifies `scripts/post_merge_smoke.py` runs to completion in --local
mode (TestClient against the live FastAPI app), reports the expected
18 endpoint checks, and exits 0 when all green.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_post_merge_smoke_script_imports_cleanly():
    script = REPO / "scripts" / "post_merge_smoke.py"
    assert script.exists()
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(script)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr


def test_post_merge_smoke_local_mode_all_green():
    """Run against in-process TestClient; all 18 endpoints (14 public +
    4 admin) must pass shape checks."""
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "post_merge_smoke.py"),
         "--local", "--json"],
        capture_output=True, text=True, check=False, cwd=str(REPO), timeout=180,
        env={**__import__("os").environ, "ADMIN_API_KEYS": "test_post_merge_smoke_local"},
    )
    assert result.returncode == 0, (
        f"smoke exit={result.returncode}\nstdout:\n{result.stdout[-2000:]}\nstderr:\n{result.stderr[-1000:]}"
    )
    payload = json.loads(result.stdout)
    summary = payload["summary"]
    assert summary["total"] == 18, f"expected 18 endpoints, got {summary['total']}"
    assert summary["all_green"] is True, (
        f"expected all green; failed: {[r for r in payload['results'] if not r['ok']]}"
    )
    # Every endpoint must report a duration (proves we actually called it)
    for r in payload["results"]:
        assert "duration_ms" in r
        assert r["duration_ms"] >= 0


def test_post_merge_smoke_local_mode_includes_wave_19_endpoints():
    """Ensure the smoke target list includes every Wave 19 public surface."""
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "post_merge_smoke.py"),
         "--local", "--json"],
        capture_output=True, text=True, check=False, cwd=str(REPO), timeout=180,
        env={**__import__("os").environ, "ADMIN_API_KEYS": "test_post_merge_smoke_paths"},
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    paths = {r["path"] for r in payload["results"]}
    for must in (
        "/healthz",
        "/api/v1/dealix-promise",
        "/api/v1/doctrine",
        "/api/v1/commercial-map",
        "/api/v1/gcc-markets",
        "/api/v1/capital-assets/public",
        "/api/v1/founder/launch-status/public",
        "/api/v1/founder/command-center/public",
        "/api/v1/founder/command-center",
        "/api/v1/capital-assets",
    ):
        assert must in paths, f"smoke target list missing {must!r}"


def test_post_merge_smoke_local_mode_no_shape_errors():
    """Shape checks must catch a regression — if any endpoint changed shape,
    the smoke MUST report a shape_error."""
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "post_merge_smoke.py"),
         "--local", "--json"],
        capture_output=True, text=True, check=False, cwd=str(REPO), timeout=180,
        env={**__import__("os").environ, "ADMIN_API_KEYS": "test_post_merge_smoke_shape"},
    )
    payload = json.loads(result.stdout)
    shape_errors = [
        r for r in payload["results"] if r.get("shape_error") is not None
    ]
    assert shape_errors == [], (
        f"shape regressions detected: {shape_errors}"
    )
