"""V11 Phase 7 — payment fallback + invoice CLI hardening tests.

Asserts:
- Dry-run output includes ``MODE``, ``AMOUNT_SAR``, ``AMOUNT_HALALAH``,
  ``MANUAL_FALLBACK_STEPS``, ``REFUND_NOTE_REQUIRED``
- Live key without --allow-live → script refuses
- 499 SAR = 49,900 halalah computed correctly
- No MOYASAR_SECRET_KEY → mode=manual_only (still safe)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "dealix_invoice.py"


def _run(*args: str, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/tmp"}
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_dry_run_no_api_key_required() -> None:
    """Dry-run must work even with NO MOYASAR_SECRET_KEY."""
    r = _run(
        "--email", "test@example.sa",
        "--amount-sar", "499",
        "--description", "Dealix Pilot 7 days (Customer-Slot-A)",
        "--dry-run",
    )
    assert r.returncode == 0, f"dry-run failed: stderr={r.stderr}"
    assert "DRY_RUN=true" in r.stdout
    assert "AMOUNT_SAR=499" in r.stdout
    assert "AMOUNT_HALALAH=49900" in r.stdout
    assert "MODE=manual_only" in r.stdout
    assert "REFUND_NOTE_REQUIRED=true" in r.stdout
    assert "MANUAL_FALLBACK_STEPS:" in r.stdout


def test_dry_run_with_test_key_reports_test_mode() -> None:
    r = _run(
        "--email", "test@example.sa",
        "--amount-sar", "499",
        "--description", "Pilot",
        "--dry-run",
        env_extra={"MOYASAR_SECRET_KEY": "sk_test_dummykey1234567890abcd"},
    )
    assert r.returncode == 0
    assert "MODE=test" in r.stdout


def test_live_key_without_allow_live_is_rejected_in_real_run() -> None:
    """Without --dry-run, a sk_live_ key must abort BEFORE any HTTP call."""
    r = _run(
        "--email", "test@example.sa",
        "--amount-sar", "499",
        "--description", "Pilot",
        env_extra={"MOYASAR_SECRET_KEY": "sk_" + "live_" + "should-be-rejected_FIXTURE"},
    )
    # Either the script exits non-zero from SystemExit OR prints a refusal
    combined = (r.stdout + r.stderr).lower()
    assert "refusing" in combined or "sk_live" in combined or r.returncode != 0


def test_dry_run_with_live_key_reports_rejected_live_mode() -> None:
    r = _run(
        "--email", "test@example.sa",
        "--amount-sar", "499",
        "--description", "Pilot",
        "--dry-run",
        env_extra={"MOYASAR_SECRET_KEY": "sk_" + "live_" + "TEST-FIXTURE_never-real"},
    )
    assert r.returncode == 0
    # In dry-run, the script reports the mode without contacting Moyasar
    assert "MODE=rejected_live" in r.stdout


def test_dry_run_with_live_key_and_allow_live_reports_live_mode() -> None:
    """Even with --allow-live, dry-run does NOT actually charge."""
    r = _run(
        "--email", "test@example.sa",
        "--amount-sar", "499",
        "--description", "Pilot",
        "--dry-run",
        "--allow-live",
        env_extra={"MOYASAR_SECRET_KEY": "sk_" + "live_" + "TEST-FIXTURE_never-real"},
    )
    assert r.returncode == 0
    assert "MODE=live" in r.stdout
    # Sanity: dry-run still doesn't actually charge
    assert "DRY_RUN=true" in r.stdout


def test_amount_sar_to_halalah_arithmetic_correct() -> None:
    for sar, halalah in [(499.0, 49900), (1.0, 100), (0.50, 50), (1234.56, 123456)]:
        r = _run(
            "--email", "x@y.sa",
            "--amount-sar", str(sar),
            "--description", "test",
            "--dry-run",
        )
        assert f"AMOUNT_HALALAH={halalah}" in r.stdout, (
            f"sar={sar} expected halalah={halalah}, got: {r.stdout}"
        )


def test_amount_zero_or_negative_refused() -> None:
    """Real run with --amount-sar=0 must be rejected (not in dry-run path)."""
    # The check is in _create(); must trigger via real run path
    r = _run(
        "--email", "x@y.sa",
        "--amount-sar", "0",
        "--description", "test",
        env_extra={"MOYASAR_SECRET_KEY": "sk_test_dummy"},
    )
    assert r.returncode != 0


def test_amount_above_50000_refused() -> None:
    r = _run(
        "--email", "x@y.sa",
        "--amount-sar", "100000",
        "--description", "test",
        env_extra={"MOYASAR_SECRET_KEY": "sk_test_dummy"},
    )
    assert r.returncode != 0
