"""Static and behavioral contracts for production diagnostic workflows.

These tests never call Railway or Dealix production. They prove that the
workflow text preserves attributable evidence, uses one Railway credential
mode at a time, and keeps Watchdog evidence columns correctly attributed.
"""

from __future__ import annotations

import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCHDOG_PATH = ROOT / ".github" / "workflows" / "production-watchdog.yml"
RAILWAY_PATH = ROOT / ".github" / "workflows" / "railway_deploy.yml"
WATCHDOG = WATCHDOG_PATH.read_text(encoding="utf-8")
RAILWAY = RAILWAY_PATH.read_text(encoding="utf-8")


def test_watchdog_tsv_empty_field_preserves_column_identity() -> None:
    sample = (
        "name\turl\thttp_status\tcontent_type\tbytes\tcurl_exit\n"
        "tls-failure\thttps://example.invalid\t000\t\t0\t6\n"
    )
    row = next(csv.DictReader(io.StringIO(sample), delimiter="\t"))
    assert row == {
        "name": "tls-failure",
        "url": "https://example.invalid",
        "http_status": "000",
        "content_type": "",
        "bytes": "0",
        "curl_exit": "6",
    }


def test_watchdog_uses_csv_parser_not_whitespace_splitting() -> None:
    assert "csv.DictReader" in WATCHDOG
    assert 'delimiter="\\t"' in WATCHDOG
    assert "while IFS=$'\\t' read" not in WATCHDOG
    assert "PRODUCTION_WATCHDOG_TSV_EMPTY_FIELD_CONTRACT=PASS" in WATCHDOG
    assert "content_type = (row.get(\"content_type\") or \"<missing>\")" in WATCHDOG


def test_watchdog_records_each_surface_before_failing() -> None:
    for surface in ("api-healthz", "railway-ar-demo", "railway-revenue-os"):
        assert f'check_url "{surface}"' in WATCHDOG
    assert "if [ \"$failures\" -ne 0 ]" in WATCHDOG
    assert "if: always()" in WATCHDOG
    assert "production-watchdog-report/" in WATCHDOG


def test_workflow_only_merge_does_not_auto_deploy() -> None:
    """Merging diagnostics must not consume the separate deployment approval gate."""
    push_trigger = RAILWAY.split("  workflow_dispatch:", 1)[0]
    assert '".github/workflows/railway_deploy.yml"' not in push_trigger
    for runtime_surface in ('"api/**"', '"core/**"', '"railway.toml"'):
        assert runtime_surface in push_trigger
    assert "  workflow_dispatch:" in RAILWAY


def test_railway_credentials_fail_closed_and_remain_mutually_exclusive() -> None:
    assert 'if [ -n "$RAILWAY_TOKEN" ] && [ -n "$RAILWAY_API_TOKEN" ]; then' in RAILWAY
    assert "token_mode=conflict" in RAILWAY
    assert "Configure exactly one Railway credential mode, not both." in RAILWAY

    project_only = (
        "RAILWAY_TOKEN: ${{ steps.check_token.outputs.token_mode == "
        "'project' && secrets.RAILWAY_TOKEN || '' }}"
    )
    account_only = (
        "RAILWAY_API_TOKEN: ${{ steps.check_token.outputs.token_mode == "
        "'account_or_workspace' && secrets.RAILWAY_API_TOKEN || '' }}"
    )
    assert RAILWAY.count(project_only) == 3
    assert RAILWAY.count(account_only) == 3

    assert RAILWAY.count('[ -n "$RAILWAY_TOKEN" ] && [ -z "$RAILWAY_API_TOKEN" ]') == 3
    assert RAILWAY.count('[ -z "$RAILWAY_TOKEN" ] && [ -n "$RAILWAY_API_TOKEN" ]') == 3


def test_railway_diagnostics_are_bound_to_exact_deployment() -> None:
    assert "deployment_id=$deployment_id" in RAILWAY
    assert "TARGET_DEPLOYMENT_ID: ${{ steps.railway_deploy.outputs.deployment_id }}" in RAILWAY
    assert 'item.get("id") == os.environ["TARGET_DEPLOYMENT_ID"]' in RAILWAY
    assert 'railway logs "$TARGET_DEPLOYMENT_ID"' in RAILWAY
    assert "--build || true" in RAILWAY
    assert "--deployment || true" in RAILWAY
    assert "railway-terminal-deployment.json" in RAILWAY


def test_railway_smoke_waits_for_exact_deployment_success() -> None:
    required_condition = (
        "if: steps.railway_deploy.outcome == 'success' "
        "&& steps.railway_wait.outcome == 'success'"
    )
    assert required_condition in RAILWAY
    assert "id: healthz" in RAILWAY
    assert "if: steps.healthz.outcome == 'success'" in RAILWAY
    assert "Post-deploy smoke pack" in RAILWAY


def test_diagnostics_do_not_echo_secret_values() -> None:
    forbidden = (
        'echo "$RAILWAY_TOKEN"',
        'echo "${RAILWAY_TOKEN}"',
        'echo "$RAILWAY_API_TOKEN"',
        'echo "${RAILWAY_API_TOKEN}"',
        'cat "$RAILWAY_TOKEN"',
        'cat "$RAILWAY_API_TOKEN"',
    )
    for token_echo in forbidden:
        assert token_echo not in RAILWAY
