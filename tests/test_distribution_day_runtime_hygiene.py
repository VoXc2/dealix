from pathlib import Path

import scripts.distribution_day as distribution_day


def test_default_report_is_outside_canonical_repo(monkeypatch):
    monkeypatch.delenv("DEALIX_RUNTIME_REPORTS_ROOT", raising=False)
    path = distribution_day._default_report()
    assert path == Path("/opt/dealix/control/reports/distribution/DISTRIBUTION_DAY.md")
    assert distribution_day.ROOT.resolve() not in path.resolve().parents


def test_runtime_root_override_keeps_mutable_output_outside_source(monkeypatch, tmp_path: Path):
    runtime_root = tmp_path / "dealix-runtime"
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(runtime_root))
    assert distribution_day._default_report() == runtime_root / "distribution" / "DISTRIBUTION_DAY.md"


def test_source_does_not_restore_legacy_tracked_default():
    source = (distribution_day.ROOT / "scripts" / "distribution_day.py").read_text(encoding="utf-8")
    assert "ROOT / \"reports\" / \"distribution\" / \"DISTRIBUTION_DAY.md\"" not in source
    assert "external" not in distribution_day._render.__name__.lower()


def test_runtime_root_override_fails_closed_inside_source(monkeypatch):
    monkeypatch.setenv("DEALIX_RUNTIME_REPORTS_ROOT", str(distribution_day.ROOT / "reports" / "runtime"))
    try:
        distribution_day._default_report()
    except ValueError as exc:
        assert "outside the canonical repository" in str(exc)
    else:
        raise AssertionError("runtime root inside canonical repository must fail closed")
