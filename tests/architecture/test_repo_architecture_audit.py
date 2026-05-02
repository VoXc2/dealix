"""Tests for the repo architecture audit script.

These tests verify two things:
  1. The audit currently passes against HEAD.
  2. The audit's individual checks correctly detect violations
     when intentionally tripped (regression guard for the guard).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from scripts.repo_architecture_audit import (
    ALLOWED_CONTEXT_MARKERS,
    AuditReport,
    CheckResult,
    FORBIDDEN_PATTERNS,
    check_autonomy_mode_integrity,
    check_forbidden_patterns,
    check_pdpl_gates_per_agent,
    check_required_tests,
    check_routers_registered,
    check_safety_flags_discoverable,
    check_whatsapp_buttons_rule,
    render,
    run_audit,
)


def test_audit_passes_on_head() -> None:
    report = run_audit()
    failures = [c for c in report.checks if not c.passed]
    assert report.passed, "audit failed:\n" + render(report) + "\n\nfailures: " + ", ".join(
        f"{c.name}: {c.detail}" for c in failures
    )


def test_audit_report_shape() -> None:
    report = run_audit()
    assert isinstance(report, AuditReport)
    assert len(report.checks) == 9
    for c in report.checks:
        assert isinstance(c, CheckResult)
        assert c.name
        assert isinstance(c.passed, bool)


def test_render_includes_pass_fail_and_result() -> None:
    report = run_audit()
    text = render(report)
    assert "DEALIX_ARCH_AUDIT" in text
    assert "RESULT:" in text
    assert "SUMMARY:" in text


def test_routers_registered_returns_pass() -> None:
    result = check_routers_registered()
    assert result.passed, result.detail


def test_whatsapp_buttons_rule_detects_missing_guard(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """If the ≤3 guard disappears from whatsapp_cards.py, the check must fail."""
    fake_repo = tmp_path
    (fake_repo / "auto_client_acquisition" / "personal_operator").mkdir(parents=True)
    target = fake_repo / "auto_client_acquisition" / "personal_operator" / "whatsapp_cards.py"
    target.write_text("def build():\n    return {'buttons': []}\n", encoding="utf-8")

    import scripts.repo_architecture_audit as audit_mod
    monkeypatch.setattr(audit_mod, "_REPO", fake_repo)

    result = audit_mod.check_whatsapp_buttons_rule()
    assert not result.passed
    assert "guard" in result.detail.lower()


def test_whatsapp_buttons_rule_passes_with_guard_present() -> None:
    result = check_whatsapp_buttons_rule()
    assert result.passed


def test_required_tests_detect_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake_repo = tmp_path
    import scripts.repo_architecture_audit as audit_mod
    monkeypatch.setattr(audit_mod, "_REPO", fake_repo)

    result = audit_mod.check_required_tests()
    assert not result.passed
    assert "missing" in result.detail


def test_safety_flags_discoverable_passes() -> None:
    result = check_safety_flags_discoverable()
    assert result.passed, result.detail


def test_pdpl_gates_per_agent_passes() -> None:
    result = check_pdpl_gates_per_agent()
    assert result.passed, result.detail


def test_autonomy_mode_integrity_passes() -> None:
    result = check_autonomy_mode_integrity()
    assert result.passed, result.detail


def test_forbidden_patterns_allows_documented_intent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A line documenting avoidance (`avoid = [...]`) should NOT trip the check."""
    fake_repo = tmp_path
    pkg = fake_repo / "auto_client_acquisition" / "policy"
    pkg.mkdir(parents=True)
    (pkg / "policy_doc.py").write_text(
        '"""policy doc"""\n'
        'avoid = ["cold_whatsapp_broadcasts"]\n'
        'restricted_actions = {"cold_whatsapp": True}\n',
        encoding="utf-8",
    )

    import scripts.repo_architecture_audit as audit_mod
    monkeypatch.setattr(audit_mod, "_REPO", fake_repo)

    result = audit_mod.check_forbidden_patterns()
    assert result.passed, result.detail


def test_forbidden_patterns_flags_active_use(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A line that *uses* a forbidden identifier without policy markers must fail."""
    fake_repo = tmp_path
    pkg = fake_repo / "auto_client_acquisition" / "evil"
    pkg.mkdir(parents=True)
    (pkg / "bad.py").write_text(
        'def cold_whatsapp(x):\n'
        '    return x\n'
        'cold_whatsapp("hi")\n',
        encoding="utf-8",
    )

    import scripts.repo_architecture_audit as audit_mod
    monkeypatch.setattr(audit_mod, "_REPO", fake_repo)

    result = audit_mod.check_forbidden_patterns()
    assert not result.passed
    assert "cold_whatsapp" in result.detail


def test_allowed_context_markers_constant_well_formed() -> None:
    assert isinstance(ALLOWED_CONTEXT_MARKERS, tuple)
    assert all(isinstance(m, str) and m for m in ALLOWED_CONTEXT_MARKERS)
    assert "restricted_actions" in ALLOWED_CONTEXT_MARKERS


def test_forbidden_patterns_constant() -> None:
    assert "cold_whatsapp" in FORBIDDEN_PATTERNS
    assert "linkedin_auto_dm" in FORBIDDEN_PATTERNS
    # Must NOT include an over-broad substring that would catch labels.
    assert "linkedin_scrape" not in FORBIDDEN_PATTERNS


def test_no_print_in_production_passes() -> None:
    from scripts.repo_architecture_audit import check_no_print_in_production
    result = check_no_print_in_production()
    assert result.passed, result.detail


def test_secrets_hygiene_passes() -> None:
    from scripts.repo_architecture_audit import check_secrets_hygiene
    result = check_secrets_hygiene()
    # In CI (shallow checkout) git ls-files always works; locally too.
    assert result.passed, result.detail


def test_render_handles_empty_report() -> None:
    report = AuditReport()
    text = render(report)
    assert "RESULT: PASS" in text  # vacuously true when no checks
    assert re.search(r"SUMMARY: 0 passed, 0 failed", text)
