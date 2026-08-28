"""Regression tests for current Dealix proposal authority."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RETIRED_OUTPUT_MARKERS = (
    "499 sar",
    "499 ريال",
    "7-day sprint",
    "7-day revenue",
    "18,000 sar",
    "35,000 sar",
    "25,000 sar",
    "12,000 sar",
    "payment_url",
    "money-back",
)


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _combined(proc: subprocess.CompletedProcess[str]) -> str:
    return (proc.stdout + "\n" + proc.stderr).lower()


def test_canonical_diagnostic_is_free_non_committing_and_current_path() -> None:
    proc = _run(
        "scripts/render_diagnostic_proposal.py",
        "--company",
        "Example Co",
        "--contact",
        "Decision Owner",
        "--dry-run",
    )
    assert proc.returncode == 0, proc.stderr
    payload = _combined(proc)

    assert "free mini diagnostic" in payload
    assert "qualified discovery" in payload
    assert "customer-specific quote" in payload
    assert "revenue command pilot — 30 days" in payload
    assert "draft_not_sent" in payload
    assert "no public/fixed pilot price" in payload

    for marker in RETIRED_OUTPUT_MARKERS:
        assert marker not in payload


def test_legacy_proposal_command_ignores_retired_tier_and_renders_diagnostic_only() -> None:
    proc = _run(
        "scripts/dealix_proposal_generator.py",
        "--company",
        "Example Co",
        "--contact",
        "Decision Owner",
        "--sector",
        "b2b_services",
        "--tier",
        "sprint",
        "--dry-run",
    )
    assert proc.returncode == 0, proc.stderr
    payload = _combined(proc)

    assert "retired_tier_ignored:sprint" in payload
    assert "free mini diagnostic" in payload
    assert "customer-specific quote" in payload
    assert "30 days" in payload
    for marker in RETIRED_OUTPUT_MARKERS:
        assert marker not in payload


def test_legacy_list_sectors_cannot_emit_fixed_price_recommendations() -> None:
    proc = _run("scripts/dealix_proposal_generator.py", "--list-sectors")
    assert proc.returncode == 0, proc.stderr
    payload = _combined(proc)
    assert "legacy_sector_tier_recommendation=retired" in payload
    assert "public_fixed_pilot_price_allowed=false" in payload
    for marker in RETIRED_OUTPUT_MARKERS:
        assert marker not in payload


def test_pilot_brief_is_non_binding_30_day_scope_draft() -> None:
    proc = _run(
        "scripts/dealix_pilot_brief.py",
        "--company",
        "Example Co",
        "--sector",
        "b2b_services",
        "--quote-evidence-id",
        "quote-example-001",
        "--dry-run",
    )
    assert proc.returncode == 0, proc.stderr
    payload = _combined(proc)

    assert "revenue command pilot — 30 days" in payload
    assert '"duration_days": 30' in payload
    assert '"price_sar": null' in payload
    assert '"payment_terms": null' in payload
    assert '"refund_policy": null' in payload
    assert '"external_send_allowed": false' in payload
    assert '"execution_allowed": false' in payload
    assert "quote-example-001" in payload
    for marker in RETIRED_OUTPUT_MARKERS:
        assert marker not in payload


def test_pilot_brief_rejects_direct_amount() -> None:
    proc = _run(
        "scripts/dealix_pilot_brief.py",
        "--company",
        "Example Co",
        "--sector",
        "b2b_services",
        "--quote-evidence-id",
        "quote-example-001",
        "--amount-sar",
        "499",
        "--dry-run",
    )
    assert proc.returncode == 2
    assert "PRICE_NOT_AUTHORIZED_BY_PILOT_BRIEF" in proc.stderr
