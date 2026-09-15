from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from scripts.commercial import run_revenue_lab_daily as runner


def test_default_revenue_lab_output_uses_control_plane(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEALIX_RUNTIME_REPORTS_ROOT", raising=False)
    out = runner._default_output_dir(now=datetime(2026, 9, 15, tzinfo=UTC))
    assert out == Path("/opt/dealix/control/reports/revenue_lab/2026-09-15")
    assert runner.ROOT.resolve() not in out.resolve(strict=False).parents


def test_runtime_reports_override_stays_external(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(tmp_path / "reports"))
    out = runner._default_output_dir(now=datetime(2026, 9, 15, tzinfo=UTC))
    assert out == (tmp_path / "reports" / "revenue_lab" / "2026-09-15").resolve()


def test_runtime_reports_override_inside_repo_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(runner.ROOT / "reports" / "runtime"))
    with pytest.raises(RuntimeError, match="outside canonical repository"):
        runner._default_output_dir(now=datetime(2026, 9, 15, tzinfo=UTC))


def test_explicit_output_dir_remains_authoritative(tmp_path: Path) -> None:
    explicit = tmp_path / "explicit"
    assert runner.resolve_output_dir(explicit) == explicit
