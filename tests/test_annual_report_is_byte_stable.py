"""The annual-report renderer must be byte-stable.

If identical inputs produce different bytes, the CI drift gate becomes
a noise alarm. This test ensures determinism.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "render_annual_report.py"


def _load():
    spec = importlib.util.spec_from_file_location("annual_report_mod", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_renderer_is_byte_stable_for_same_year():
    mod = _load()
    a = mod.render(year=2026)
    b = mod.render(year=2026)
    assert a == b


def test_renderer_contains_all_ten_sections():
    mod = _load()
    text = mod.render(year=2026)
    for header in (
        "## 1. Overview",
        "## 2. Business Unit Summary",
        "## 3. Capital Allocation Actions",
        "## 4. Verifier State",
        "## 5. Market Motion",
        "## 6. Capital Assets",
        "## 7. Doctrine Discipline",
        "## 8. Risks (qualitative)",
        "## 9. Next Year Theses",
        "## 10. Certifications",
    ):
        assert header in text, f"missing section: {header}"


def test_renderer_writes_to_expected_path(tmp_path, monkeypatch):
    mod = _load()
    monkeypatch.setattr(mod, "OUTPUT_DIR", tmp_path)
    rc = mod.main(["--year", "2026"])
    assert rc == 0
    out = tmp_path / "dealix-group-annual-report-2026.md"
    assert out.exists()
    assert "# Dealix Group — Annual Report `2026`" in out.read_text()


def test_committed_annual_report_matches_current_render():
    """The committed annual-report MD must match what render() produces.
    This is the property that makes the CI drift gate meaningful."""
    mod = _load()
    expected = mod.render(year=2026)
    committed = (REPO_ROOT / "landing" / "assets" / "downloads"
                 / "dealix-group-annual-report-2026.md").read_text(encoding="utf-8")
    assert committed == expected
