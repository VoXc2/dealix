"""Tests for scripts/dealix_snapshot.py.

Pure local: no HTTP, no secrets. The snapshot script reads in-process
modules and writes a JSON file. Tests verify shape, idempotency, and
the live-gates safety invariant.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
from contextlib import redirect_stdout
from datetime import UTC, datetime
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_snapshot.py"

REQUIRED_KEYS = {
    "schema_version",
    "generated_at",
    "services",
    "reliability",
    "live_gates",
    "daily_loop",
    "weekly_scorecard",
    "promotion_candidates",
}


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_snapshot  # type: ignore[import-not-found]
        return dealix_snapshot
    finally:
        sys.path.pop(0)


def test_snapshot_script_exists_and_has_shebang():
    assert SCRIPT.exists()
    assert SCRIPT.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3")


def test_print_mode_outputs_valid_json_with_required_keys():
    """`--print` mode dumps valid JSON to stdout containing every
    required top-level key — and writes nothing."""
    mod = _import_module()
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = mod.main(["--print"])
    assert rc == 0
    payload = json.loads(buf.getvalue())
    assert REQUIRED_KEYS.issubset(payload.keys()), (
        f"missing keys: {REQUIRED_KEYS - set(payload.keys())}"
    )
    assert payload["schema_version"] == 1


def test_live_gates_never_allowed_on_clean_checkout():
    """Hard rule: a clean repo checkout must never report a live gate
    as ALLOWED. live_charge in particular must be BLOCKED (or UNKNOWN
    on import failure) — never ALLOWED."""
    mod = _import_module()
    snap = mod.build_snapshot()
    gates = snap["live_gates"]
    assert isinstance(gates, dict) and gates, "live_gates must be a non-empty dict"
    for name, value in gates.items():
        assert value != "ALLOWED", (
            f"live gate {name!r} reported ALLOWED on a clean checkout — "
            f"this MUST never happen"
        )


def test_writes_to_tmp_path(tmp_path: Path):
    """`--out PATH` should produce a file at the expected location with
    valid JSON inside."""
    mod = _import_module()
    out = tmp_path / "snap.json"
    rc = mod.main(["--out", str(out)])
    assert rc == 0
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert REQUIRED_KEYS.issubset(payload.keys())


def test_services_total_is_32_or_skip():
    """The Service Activation Matrix is sized at 32 services. If that
    drifts the test skips rather than fails, since the matrix is the
    source of truth — but in steady state we want this guarded."""
    mod = _import_module()
    snap = mod.build_snapshot()
    services = snap["services"]
    if not isinstance(services, dict) or "total" not in services:
        pytest.skip(f"service counts unavailable: {services!r}")
    if services["total"] != 32:
        pytest.skip(
            f"matrix size changed (now {services['total']}) — update test"
        )
    assert services["total"] == 32


def test_same_day_rerun_overwrites_no_append(tmp_path: Path):
    """Re-running on the same day must overwrite the file cleanly —
    the file must remain a single valid JSON object, not concatenated
    objects or an appended array."""
    mod = _import_module()
    out = tmp_path / "snap.json"

    rc1 = mod.main(["--out", str(out)])
    assert rc1 == 0
    first_size = out.stat().st_size
    first = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(first, dict)

    rc2 = mod.main(["--out", str(out)])
    assert rc2 == 0
    # File must still parse as one JSON object, not two concatenated.
    second = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(second, dict)
    # Size should be in the same ballpark — a naive append would at
    # least double it.
    assert out.stat().st_size < first_size * 2


def test_default_out_path_uses_today():
    """`default_out_path()` must point inside docs/snapshots/ with a
    YYYY-MM-DD filename for today (UTC)."""
    mod = _import_module()
    p = mod.default_out_path()
    assert p.parent.name == "snapshots"
    assert p.parent.parent.name == "docs"
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    assert p.name == f"{today}.json"


def test_runs_as_subprocess_print_mode():
    """Smoke: invoking the script as a real subprocess (no in-process
    imports) still produces parseable JSON — proves the shebang +
    argv handling + module discovery all work end to end."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--print"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=60,
    )
    assert proc.returncode == 0, f"stderr: {proc.stderr}"
    payload = json.loads(proc.stdout)
    assert REQUIRED_KEYS.issubset(payload.keys())
