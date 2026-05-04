"""Lock the technical-SEO perimeter for the static landing site.

This test wraps ``scripts/seo_audit.py`` so CI fails the moment a page
loses its required SEO elements (title, meta description, viewport,
``<html lang>`` / ``dir``). Advisory items (canonical, OG, Twitter
card) are tracked separately and shrunk over time as the founder
approves OG copy per page.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "seo_audit.py"
REPORT = REPO / "docs" / "SEO_AUDIT_REPORT.json"

# Per-page advisory exemptions. As the founder approves OG/canonical
# copy on each page, remove its entry here. New pages must either
# include those tags or be added to this list with a reason.
ADVISORY_EXEMPT = {
    "academy.html",
    "autopilot.html",
    "case-study.html",
    "command-center.html",
    "community.html",
    "copilot.html",
    "customer-portal.html",
    "dashboard.html",
    "founder.html",
    "market-radar.html",
    "marketers.html",
    "partners.html",
    "pay-per-result.html",
    "personal-operator.html",
    "pricing.html",
    "pulse.html",
    "roi.html",
    "simulator.html",
    "trust-center.html",
    "trust.html",
    "verticals.html",
    # status.html and launch-readiness.html are intentionally NOT here:
    # status.html has canonical + OG + twitter:card (we authored it).
    # launch-readiness.html is in the script's ADVISORY_ONLY_PAGES set
    # so its advisory checks are skipped entirely.
}


def _run_audit() -> dict:
    res = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(REPO), capture_output=True, text=True,
    )
    # Exit code 1 only means required-gap > 0; we still want the report.
    assert REPORT.exists(), res.stderr
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_no_page_has_required_gap():
    """Every audited landing page must have title, meta description,
    viewport, html lang and html dir. New pages without these fail.
    """
    report = _run_audit()
    offenders = [
        (p["path"], p["missing_required"])
        for p in report["pages"] if p["missing_required"]
    ]
    assert not offenders, (
        "pages with missing required SEO elements:\n" +
        "\n".join(f"  {p}: {m}" for p, m in offenders)
    )


def test_advisory_exemptions_match_known_set():
    """The advisory-exempt allowlist must match exactly the pages that
    currently have advisory gaps. If a page picks up advisory tags,
    drop it from ADVISORY_EXEMPT to keep the perimeter tight. If a new
    page is added without advisory tags, decide explicitly: fix the
    page or extend the allowlist.
    """
    report = _run_audit()
    pages_with_advisory_gap = {
        p["path"] for p in report["pages"] if p["missing_advisory"]
    }
    new_offenders = pages_with_advisory_gap - ADVISORY_EXEMPT
    stale_exemptions = ADVISORY_EXEMPT - pages_with_advisory_gap

    msgs: list[str] = []
    if new_offenders:
        msgs.append(
            "new pages with advisory SEO gaps not in ADVISORY_EXEMPT: "
            + ", ".join(sorted(new_offenders))
        )
    if stale_exemptions:
        msgs.append(
            "ADVISORY_EXEMPT has stale entries (pages now have the tags): "
            + ", ".join(sorted(stale_exemptions))
        )
    assert not msgs, "\n".join(msgs)


def test_audit_report_is_committed_and_fresh():
    """The committed report must reflect the current page state. CI
    runs the audit again and the regenerated file must be byte-equal.
    """
    before = REPORT.read_text(encoding="utf-8") if REPORT.exists() else ""
    _run_audit()
    after = REPORT.read_text(encoding="utf-8")
    assert before == after, (
        "docs/SEO_AUDIT_REPORT.json is stale relative to the current "
        "landing/*.html state. Re-run scripts/seo_audit.py and commit."
    )
