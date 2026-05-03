"""Tests for the launch readiness check."""

from __future__ import annotations

import pytest

from scripts.launch_readiness_check import (
    FLAGS_DEFAULT_FALSE,
    REQUIRED_FILES,
    ReadinessReport,
    StepResult,
    render,
    run_checks,
    step_arch_audit,
    step_env_sanity,
    step_files_exist,
)


def test_readiness_run_skip_pytest() -> None:
    """Run all steps except pytest (avoids self-recursion when invoked under pytest)."""
    report = run_checks(skip_pytest=True)
    assert isinstance(report, ReadinessReport)
    failures = [s for s in report.steps if not s.passed]
    assert report.passed, "readiness check failed:\n" + render(report) + "\nfailures: " + ", ".join(
        f"{s.name}: {s.detail}" for s in failures
    )


def test_readiness_report_shape() -> None:
    report = run_checks(skip_pytest=True)
    assert len(report.steps) == 6  # all steps minus pytest
    for s in report.steps:
        assert isinstance(s, StepResult)
        assert s.name


def test_step_arch_audit_passes() -> None:
    result = step_arch_audit()
    assert result.passed, result.detail


def test_step_env_sanity_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    for flag in FLAGS_DEFAULT_FALSE:
        monkeypatch.setenv(flag.upper(), "false")
    result = step_env_sanity()
    assert result.passed, result.detail


def test_step_files_exist_passes() -> None:
    result = step_files_exist()
    assert result.passed, result.detail


def test_render_includes_go_or_blocked() -> None:
    report = run_checks(skip_pytest=True)
    text = render(report)
    assert "DEALIX_LAUNCH_READINESS" in text
    assert ("GO_PRIVATE_BETA" in text) or ("BLOCKED" in text)


def test_required_files_constant() -> None:
    # Spot-check: the three files we depend on for staging deploy.
    assert "Dockerfile" in REQUIRED_FILES
    assert "railway.json" in REQUIRED_FILES
    assert any("command-center.html" in f for f in REQUIRED_FILES)


def test_flags_default_false_constant() -> None:
    # Always-false flags must be enumerated here.
    assert "whatsapp_allow_live_send" in FLAGS_DEFAULT_FALSE
    assert "linkedin_allow_auto_dm" in FLAGS_DEFAULT_FALSE
    assert "moyasar_allow_live_charge" in FLAGS_DEFAULT_FALSE
    assert "gmail_allow_live_send" in FLAGS_DEFAULT_FALSE
