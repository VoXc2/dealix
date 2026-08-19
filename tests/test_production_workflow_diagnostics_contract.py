"""Static and behavioral contracts for production diagnostic workflows.

These tests never call Railway or Dealix production. They prove that the
workflow text preserves attributable evidence, uses one Railway credential
mode at a time, sanitizes environment posture without exposing values, and
keeps Watchdog evidence columns correctly attributed.
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
    for surface in (
        "public-home",
        "public-ar",
        "api-healthz",
        "railway-ar-demo",
        "railway-revenue-os",
    ):
        assert f'check_url "{surface}"' in WATCHDOG
    assert "if [ \"$failures\" -ne 0 ]" in WATCHDOG
    assert "if: always()" in WATCHDOG
    assert "production-watchdog-report/" in WATCHDOG


def test_watchdog_rejects_github_pages_as_canonical_public_frontend() -> None:
    assert 'check_url "public-home" "https://dealix.me/"' in WATCHDOG
    assert 'check_url "public-ar" "https://dealix.me/ar"' in WATCHDOG
    assert '"$report_dir/public-home.headers"' in WATCHDOG
    assert '"${public_server,,}" == *"github.com"*' in WATCHDOG
    assert "github_pages_is_not_canonical_frontend" in WATCHDOG
    assert "PRODUCTION_WATCHDOG_FRONTEND_ORIGIN=FAIL" in WATCHDOG
    assert "PRODUCTION_WATCHDOG_FRONTEND_ORIGIN=PASS" in WATCHDOG


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
    assert "== default logs for exact deployment ==" in RAILWAY
    assert "== error/warning logs for exact deployment ==" in RAILWAY
    assert "railway-terminal-deployment.json" in RAILWAY


def test_terminal_diagnostics_bind_variable_inventory_to_project() -> None:
    """Account/workspace-token diagnostics must select the intended Railway project."""
    assert RAILWAY.count("PROJECT_ID: ${{ vars.RAILWAY_PROJECT_ID }}") == 3
    diagnostics = RAILWAY.split(
        "      - name: Capture exact Railway terminal diagnostics", 1
    )[1].split("      - name: Upload Railway terminal diagnostics", 1)[0]
    variable_command = diagnostics.split(
        '          variable_cmd=(railway variable list --service "$SERVICE" --json)', 1
    )[1].split("          set +e", 1)[0]
    assert 'if [ -n "$PROJECT_ID" ]; then' in variable_command
    assert 'variable_cmd+=(--project "$PROJECT_ID")' in variable_command
    assert 'variable_cmd+=(--environment "$ENVIRONMENT_NAME")' in variable_command
    assert variable_command.index("--project") < variable_command.index("--environment")


def test_terminal_diagnostics_record_only_sanitized_variable_posture() -> None:
    """Read Railway variables but never persist or print their raw values."""
    assert 'railway variable list --service "$SERVICE" --json' in RAILWAY
    assert "railway-terminal-config-posture.json" in RAILWAY
    for field in (
        "variable_inventory_readable",
        "run_railway_pre_deploy_migrate_enabled",
        "database_url_configured",
        "app_secret_key_configured",
        "app_secret_key_valid",
        "jwt_secret_key_configured",
        "jwt_secret_key_valid",
        "api_keys_configured",
        "admin_api_keys_configured",
        "orchestrator_backend",
        "app_env",
        "fresh_db_bootstrap_enabled",
        "alembic_version_widen_enabled",
    ):
        assert field in RAILWAY

    assert 'app_env_raw = (value("APP_ENV") or value("ENVIRONMENT")).lower()' in RAILWAY
    assert 'app_secret = value("APP_SECRET_KEY")' in RAILWAY
    assert 'jwt_secret = value("JWT_SECRET_KEY")' in RAILWAY
    assert '"change-me", "CHANGE_ME_to_64_byte_hex", "changeme"' in RAILWAY
    assert '"change-me" not in jwt_secret and len(jwt_secret) >= 32' in RAILWAY
    assert '"app_secret_key_valid": app_secret_valid' in RAILWAY
    assert '"jwt_secret_key_valid": jwt_secret_valid' in RAILWAY
    assert '"api_keys_configured": bool(value("API_KEYS"))' in RAILWAY
    assert '"admin_api_keys_configured": bool(value("ADMIN_API_KEYS"))' in RAILWAY

    forbidden = (
        "cat /tmp/railway-vars.json",
        "cat \"/tmp/railway-vars.json\"",
        "cp /tmp/railway-vars.json",
        "reports/ci/railway-vars.json",
    )
    for raw_export in forbidden:
        assert raw_export not in RAILWAY


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
