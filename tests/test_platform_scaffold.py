"""Consolidated guard for the Enterprise Agentic Infrastructure scaffold.

Verifies the /platform operating-model layer is intact and its readiness
model runs. Per-system self-checks live in each system's own tests/ dir.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_scaffold_check_passes():
    result = subprocess.run(
        [sys.executable, "scripts/build_platform_scaffold.py", "--check"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_readiness_model_runs_and_produces_verdict():
    spec = importlib.util.spec_from_file_location(
        "readiness_model", REPO / "platform" / "readiness_model.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    dims, systems = mod.parse_manifest(
        (REPO / "platform" / "readiness_manifest.yaml").read_text(encoding="utf-8")
    )
    assert len(dims) == 10
    assert len(systems) == 34
    result = mod.score(dims, systems)
    assert result["verdict"] in ("ARRIVED", "ON_TRACK", "EARLY")
    assert set(result["dimensions"]) == set(dims)


def test_seven_phases_present():
    for path in ("platform", "agents", "workflows", "governance", "memory",
                 "continuous_improvement", "releases", "changelogs", "versions"):
        assert (REPO / path).is_dir(), f"missing top-level scaffold dir: {path}"
    assert (REPO / "platform" / "ENTERPRISE_MATURITY_OS.md").exists()
