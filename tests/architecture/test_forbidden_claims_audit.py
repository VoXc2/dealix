"""Tests for the forbidden claims audit script (PR-FE-1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.forbidden_claims_audit import (
    AuditReport,
    CheckResult,
    FORBIDDEN_CLAIMS,
    IN_SCOPE_FILES,
    NEGATIVE_MARKERS,
    REQUIRED_HEAD_TAGS,
    _has_negative_marker,
    check_forbidden_claims,
    check_head_tags,
    check_html_attrs,
    check_required_links,
    check_required_text,
    render,
    run_audit,
)


# ── Smoke: audit passes on HEAD ────────────────────────────────────

def test_audit_passes_on_head() -> None:
    report = run_audit()
    failures = [c for c in report.checks if not c.passed]
    assert report.passed, "forbidden_claims audit failed:\n" + render(report) + \
        "\nfailures: " + ", ".join(f"{c.file}::{c.name}: {c.detail}" for c in failures)


def test_audit_covers_all_in_scope_files() -> None:
    report = run_audit()
    files_audited = {Path(c.file).name for c in report.checks}
    for required in IN_SCOPE_FILES:
        assert required in files_audited, f"{required} not audited"


def test_audit_returns_at_least_n_checks_per_file() -> None:
    """Each file gets ≥7 checks (forbidden + 2 links + 1 text + 2 attrs + 2 head)."""
    report = run_audit()
    by_file: dict[str, list[CheckResult]] = {}
    for c in report.checks:
        by_file.setdefault(c.file, []).append(c)
    for fname, checks in by_file.items():
        assert len(checks) >= 7, f"{fname} has only {len(checks)} checks"


# ── Constants sanity ─────────────────────────────────────────────

def test_forbidden_claims_constant_well_formed() -> None:
    assert isinstance(FORBIDDEN_CLAIMS, tuple)
    assert all(isinstance(c, str) and c for c in FORBIDDEN_CLAIMS)
    assert "نضمن" in FORBIDDEN_CLAIMS
    assert "scraping" in FORBIDDEN_CLAIMS
    assert "cold whatsapp" in FORBIDDEN_CLAIMS
    assert "auto-dm" in FORBIDDEN_CLAIMS


def test_negative_markers_constant_well_formed() -> None:
    assert isinstance(NEGATIVE_MARKERS, tuple)
    assert any("لا" in m for m in NEGATIVE_MARKERS)
    assert any("✗" in m for m in NEGATIVE_MARKERS)
    assert any("forbidden" in m for m in NEGATIVE_MARKERS)


def test_in_scope_includes_pr_fe_1_pages() -> None:
    expected = {
        "companies.html", "services.html", "private-beta.html",
        "growth-os.html", "agency-partner.html", "operator.html",
        "targeting.html", "proof-pack.html", "support.html",
    }
    assert expected.issubset(set(IN_SCOPE_FILES))


# ── Negative-context detection ────────────────────────────────────

def test_negative_marker_detection_arabic() -> None:
    assert _has_negative_marker("✗ لا نُرسل واتساب بارد")
    assert _has_negative_marker("نمنع scraping من LinkedIn")
    assert _has_negative_marker("بدون cold WhatsApp")
    assert _has_negative_marker("Dealix لا يستخدم scraping")


def test_negative_marker_detection_english() -> None:
    assert _has_negative_marker("we do not allow scraping")
    assert _has_negative_marker("forbidden practice: cold whatsapp")
    assert _has_negative_marker("✗ never use mass send")


def test_negative_marker_absent_in_neutral_claim() -> None:
    """A line that just promotes a forbidden claim must NOT match a negative marker."""
    assert not _has_negative_marker("نضمن لك زيادة 200% في المبيعات")
    assert not _has_negative_marker("Use our scraping engine for fast results")


# ── check_forbidden_claims behavior ───────────────────────────────

def test_check_forbidden_claims_flags_active_claim(tmp_path: Path) -> None:
    page = tmp_path / "bad.html"
    page.write_text(
        '<html lang="ar" dir="rtl"><head><title>x</title></head>'
        '<body><h1>نضمن لك زيادة 200%!</h1></body></html>',
        encoding="utf-8",
    )
    # Patch _REPO so relative_to works
    import scripts.forbidden_claims_audit as mod
    orig = mod._REPO
    mod._REPO = tmp_path
    try:
        results = check_forbidden_claims(page, page.read_text())
    finally:
        mod._REPO = orig
    assert any(not r.passed for r in results)


def test_check_forbidden_claims_allows_documented_avoidance(tmp_path: Path) -> None:
    page = tmp_path / "good.html"
    page.write_text(
        '<html lang="ar" dir="rtl"><body>'
        '<p>✗ لا نُرسل واتساب بارد.</p>'
        '<p>Dealix لا يستخدم scraping أبداً.</p>'
        '</body></html>',
        encoding="utf-8",
    )
    import scripts.forbidden_claims_audit as mod
    orig = mod._REPO
    mod._REPO = tmp_path
    try:
        results = check_forbidden_claims(page, page.read_text())
    finally:
        mod._REPO = orig
    assert all(r.passed for r in results), [r.detail for r in results if not r.passed]


# ── check_html_attrs / check_head_tags ────────────────────────────

def test_html_attrs_pass_on_rtl_arabic(tmp_path: Path) -> None:
    page = tmp_path / "p.html"
    page.write_text('<html lang="ar" dir="rtl"><head></head><body></body></html>', encoding="utf-8")
    import scripts.forbidden_claims_audit as mod
    orig = mod._REPO
    mod._REPO = tmp_path
    try:
        results = check_html_attrs(page, page.read_text())
    finally:
        mod._REPO = orig
    assert all(r.passed for r in results)


def test_html_attrs_fail_when_lang_missing(tmp_path: Path) -> None:
    page = tmp_path / "p.html"
    page.write_text('<html dir="rtl"><head></head><body></body></html>', encoding="utf-8")
    import scripts.forbidden_claims_audit as mod
    orig = mod._REPO
    mod._REPO = tmp_path
    try:
        results = check_html_attrs(page, page.read_text())
    finally:
        mod._REPO = orig
    assert any(not r.passed for r in results)


def test_required_head_tags_constant() -> None:
    assert any("description" in t for t in REQUIRED_HEAD_TAGS)
    assert any("canonical" in t for t in REQUIRED_HEAD_TAGS)


# ── Integration: render output ─────────────────────────────────────

def test_render_produces_summary_line() -> None:
    report = run_audit()
    text = render(report, only_failures=False)
    assert "DEALIX_FORBIDDEN_CLAIMS_AUDIT" in text
    assert "SUMMARY:" in text
    assert "RESULT:" in text


def test_render_handles_empty_report() -> None:
    report = AuditReport()
    text = render(report, only_failures=False)
    assert "RESULT: PASS" in text  # vacuously true with 0 checks
    assert "SUMMARY: 0 passed, 0 failed" in text
