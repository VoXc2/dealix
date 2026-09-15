"""Regression: generated daily content artifacts must not mutate tracked source.

Canonical runtime-output contract (see scripts/dealix_content_factory_daily.py):
generated daily artifacts default to an untracked runtime location
(`reports/runtime/...`, or `$DEALIX_RUNTIME_REPORTS_ROOT/...` outside the
worktree — the same env contract the commercial runners use). The historical
tracked `reports/company_os/daily/CONTENT_DRAFTS_TODAY.md` stays a read-only
fixture/reference and must not be overwritten by normal runtime.

Draft-only / no-external-publish semantics are preserved.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import dealix_content_factory_daily as factory
from scripts import dealix_launch_engine as engine

ROOT = Path(__file__).resolve().parents[1]
TRACKED_FIXTURE = ROOT / "reports" / "company_os" / "daily" / "CONTENT_DRAFTS_TODAY.md"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tracked_is_clean() -> bool:
    """No staged/unstaged modification of the tracked daily fixture."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", str(TRACKED_FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and result.stdout.strip() == ""


def _is_ignored(path: Path) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", str(path)],
        cwd=str(ROOT),
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def test_default_out_dir_is_untracked_runtime_not_tracked_fixture():
    out = factory._default_out_dir()
    assert out != factory.LEGACY_TRACKED_DIR
    assert factory.LEGACY_TRACKED_DIR not in out.parents
    # In-repo fallback honors the existing gitignored reports/runtime/ convention.
    assert _is_ignored(out / factory.MD_FILENAME), (
        f"default runtime output must be gitignored: {out}"
    )


def test_env_override_routes_outside_worktree(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(tmp_path))
    out = factory._default_out_dir()
    assert Path(str(out)).is_relative_to(tmp_path)


def test_generator_emits_markdown_and_dated_json_without_touching_tracked(tmp_path):
    before = _sha(TRACKED_FIXTURE)
    fixed = date(2026, 9, 15)

    rc = factory.main(on_date=fixed, out_dir=tmp_path)
    assert rc == 0

    md = tmp_path / factory.MD_FILENAME
    payload = tmp_path / f"content_drafts_{fixed.isoformat()}.json"
    assert md.exists()
    assert payload.exists()

    # Draft-only / no-external-publish semantics preserved.
    text = md.read_text(encoding="utf-8")
    assert "Draft-only. No external publish/send was executed by this runner." in text
    data = json.loads(payload.read_text(encoding="utf-8"))
    assert data["external_publish_executed"] is False
    assert data["customer_send_executed"] is False
    assert data["paid_spend_executed"] is False
    assert data["governance"] == "DRAFT_ONLY_APPROVAL_FIRST"
    assert len(data["drafts"]) > 0

    # Tracked fixture/reference is byte-identical and git-clean.
    assert _sha(TRACKED_FIXTURE) == before
    assert _tracked_is_clean()


def test_generator_default_run_stays_ignored_and_tracked_clean(monkeypatch, tmp_path):
    """No explicit out-dir: output lands in the ignored runtime default."""
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(tmp_path / "control-reports"))
    before = _sha(TRACKED_FIXTURE)

    rc = factory.main(on_date=date(2026, 9, 15))
    assert rc == 0

    out = tmp_path / "control-reports" / "content_factory" / "daily"
    assert (out / factory.MD_FILENAME).exists()
    assert (out / "content_drafts_2026-09-15.json").exists()
    assert _sha(TRACKED_FIXTURE) == before
    assert _tracked_is_clean()


def test_launch_engine_content_step_uses_explicit_runtime_out_dir(tmp_path, monkeypatch):
    """The launch-engine path passes/reads an explicit out-dir (no tracked mutation)."""
    before = _sha(TRACKED_FIXTURE)

    # Subprocess generators import from the repo root; mirror a normal shell env.
    monkeypatch.setenv("PYTHONPATH", str(ROOT), prepend=":")
    monkeypatch.setenv("APP_ENV", "test")

    bundle = tmp_path / "daily_ops" / "2026-09-15"
    bundle.mkdir(parents=True)
    warm_csv = tmp_path / "warm_list.csv"
    warm_csv.write_text(
        "name,role,company,sector,relationship,city,linkedin_url,notes\n"
        "Sami,COO,Acme,b2b_services,warm,Riyadh,,met at LEAP\n",
        encoding="utf-8",
    )

    results = engine.run_generators(bundle, warm_csv)
    content = next(item for item in results if item["name"] == "Content drafts")
    assert content["status"] == engine.PASS, content

    # Explicit runtime output holds markdown + dated JSON; bundle copy exists.
    assert (bundle / "content_factory" / factory.MD_FILENAME).exists()
    assert (bundle / "content_factory" / "content_drafts_2026-09-15.json").exists()
    assert (bundle / "04_content_drafts.md").exists()

    # Tracked fixture/reference untouched by the whole launch path.
    assert _sha(TRACKED_FIXTURE) == before
    assert _tracked_is_clean()


def test_launch_engine_no_longer_targets_tracked_daily_dir():
    """Static guard: the caller must not read the tracked fixture as its source."""
    source = (ROOT / "scripts" / "dealix_launch_engine.py").read_text(encoding="utf-8")
    assert "--out-dir" in source
    assert 'reports" / "company_os" / "daily" / "CONTENT_DRAFTS_TODAY.md' not in source


@pytest.mark.parametrize("forbidden", ["reports/company_os/daily"])
def test_no_parallel_state_architecture(forbidden):
    """No new parallel state tree: reuse reports/runtime + env-override contract."""
    out = factory._default_out_dir()
    assert forbidden not in str(out.relative_to(ROOT))
    assert str(out.relative_to(ROOT)).startswith("reports/runtime")


def test_script_is_directly_runnable_without_pythonpath(tmp_path):
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["DEALIX_RUNTIME_REPORTS_ROOT"] = str(tmp_path / "runtime")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "dealix_content_factory_daily.py"), "--date", "2026-09-15"],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "DEALIX_CONTENT_FACTORY_DAILY=PASS" in result.stdout
    assert (tmp_path / "runtime" / "content_factory" / "daily" / factory.MD_FILENAME).exists()
