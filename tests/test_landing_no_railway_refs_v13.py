"""V13 — assert landing/* + critical workflows never reference the
old Railway URL or the dead ``/healthz`` endpoint.

The canonical production URL is ``https://api.dealix.me`` and the
canonical health endpoint is ``/health``. This test is the perimeter
that prevents a regression.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
LANDING_DIR = REPO_ROOT / "landing"


_FORBIDDEN_PATTERNS: tuple[tuple[str, str], ...] = (
    ("web-dealix.up.railway.app", "old Railway URL — use api.dealix.me"),
    ("/healthz", "old health endpoint name — use /health"),
)


def _scan(path: Path, patterns: tuple[tuple[str, str], ...]) -> list[str]:
    """Return list of `<path>: <pattern>: <reason>` violations."""
    out: list[str] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for pat, reason in patterns:
        if pat in text:
            out.append(f"{path.name}: '{pat}' — {reason}")
    return out


def test_landing_html_files_have_no_railway_or_healthz() -> None:
    violations: list[str] = []
    for html in sorted(LANDING_DIR.glob("*.html")):
        violations.extend(_scan(html, _FORBIDDEN_PATTERNS))
    assert not violations, "frontend regression:\n  " + "\n  ".join(violations)


def test_landing_script_js_has_no_railway_or_healthz() -> None:
    js = LANDING_DIR / "script.js"
    assert js.exists(), "landing/script.js missing"
    violations = _scan(js, _FORBIDDEN_PATTERNS)
    assert not violations, "script.js regression:\n  " + "\n  ".join(violations)


def test_dealix_live_demo_html_exists() -> None:
    """V13 ships a live-demo page consuming the V12 OS status APIs."""
    page = LANDING_DIR / "dealix-live-demo.html"
    assert page.exists(), "landing/dealix-live-demo.html missing"
    text = page.read_text(encoding="utf-8")
    assert "api.dealix.me" in text
    assert "support-os" in text
    assert "growth-os" in text
    assert "full-ops" in text


def test_deploy_pages_workflow_exists() -> None:
    """V13 ships an auto-deploy workflow for landing/ to GitHub Pages."""
    wf = REPO_ROOT / ".github" / "workflows" / "deploy-pages.yml"
    assert wf.exists(), ".github/workflows/deploy-pages.yml missing"
    text = wf.read_text(encoding="utf-8")
    assert "github-pages" in text
    assert "landing/**" in text
    assert "actions/deploy-pages" in text


def test_operational_state_doc_points_to_canonical_urls() -> None:
    """The high-traffic ops doc must reflect production URLs."""
    doc = REPO_ROOT / "DEALIX_COMPANY_OPERATIONAL_STATE.md"
    if not doc.exists():
        pytest.skip("DEALIX_COMPANY_OPERATIONAL_STATE.md not in this snapshot")
    text = doc.read_text(encoding="utf-8")
    assert "web-dealix.up.railway.app" not in text
    assert "/healthz" not in text or "/health" in text
    assert "api.dealix.me" in text


def test_dashboard_endpoints_table_uses_health_not_healthz() -> None:
    """The dashboard.html ENDPOINTS table is what the page actually
    pings; ``/healthz`` would silently return 404 in production."""
    dash = LANDING_DIR / "dashboard.html"
    if not dash.exists():
        pytest.skip("dashboard.html not present")
    text = dash.read_text(encoding="utf-8")
    # url field uses /health (not /healthz)
    assert re.search(r"url:\s*'/health'", text), "/health endpoint missing in dashboard table"
    assert not re.search(r"url:\s*'/healthz'", text), "stale /healthz still in dashboard table"
