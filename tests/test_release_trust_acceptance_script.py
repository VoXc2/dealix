from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ops" / "accept_release_trust_pr.sh"


def _text() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_acceptance_runner_is_fail_closed_and_exact_head_bound() -> None:
    text = _text()
    assert "set -Eeuo pipefail" in text
    assert "DEALIX_ACCEPT_EXPECTED_HEAD" in text
    assert "EXACT_HEAD=FAIL" in text
    assert "HEAD_STABILITY=FAIL" in text
    assert "RELEASE_TRUST_ACCEPTANCE=PASS" in text
    assert "run_pytest_gate TARGETED_PYTHON" in text
    assert "run_gate WEB_ACCEPTANCE" in text
    assert "run_gate BRAND_IDENTITY_V2" in text


def test_acceptance_runner_resolves_repo_from_script_location_not_caller_cwd() -> None:
    text = _text()
    assert 'BASH_SOURCE[0]' in text
    assert 'SCRIPT_DIR=' in text
    assert "CDPATH='' cd --" in text
    assert 'CDPATH= cd --' not in text
    assert 'git -C "$SCRIPT_DIR" rev-parse --show-toplevel' in text
    assert 'ROOT="$(git rev-parse --show-toplevel)"' not in text


def test_acceptance_runner_requires_production_equivalent_node22_or_isolated_node22() -> None:
    text = _text()
    assert 'required="production Node 22 or Docker Node 22"' in text
    assert 'host_node_major" == "22"' in text
    assert 'WEB_NODE_MODE="HOST_PRODUCTION_NODE22"' in text
    assert 'WEB_NODE_MODE="DOCKER_NODE22"' in text
    assert 'DEALIX_ACCEPT_NODE_IMAGE' in text
    assert 'node:22-bookworm' in text
    assert 'if (major !== 22) process.exit(13);' in text
    assert 'run_gate WEB_NODE22_RUNTIME docker run --rm' in text
    assert 'fail_env "production_equivalent_node22_unavailable"' in text
    assert 'host_node_major >= 22' not in text
    assert 'host_node_major" == "20"' not in text


def test_actionlint_is_required_and_keeps_warning_shell_findings_blocking() -> None:
    text = _text()
    assert 'command -v actionlint >/dev/null 2>&1 || fail_env "actionlint_not_installed"' in text
    assert "run_gate ACTIONLINT" in text
    assert "SHELLCHECK_OPTS=--severity=warning" in text
    assert "actionlint -shellcheck=" not in text
    assert "ACTIONLINT=SKIPPED_ENVIRONMENT" not in text


def test_pytest_is_forced_into_isolated_test_environment() -> None:
    text = _text()
    for token in (
        'DEALIX_PYTHON_BIN="$PY"',
        "APP_ENV=test",
        "ENVIRONMENT=test",
        "DATABASE_URL=sqlite+aiosqlite:///:memory:",
        "DEALIX_APPROVAL_STORE_BACKEND=memory",
        "DEALIX_APPROVAL_DATABASE_URL=",
        "DEALIX_APPROVAL_ALLOW_SQLITE_TEST_BACKEND=1",
        "PYTEST_ISOLATION=PASS",
    ):
        assert token in text
    assert 'run_pytest_gate TARGETED_PYTHON "${PYTEST_ENV[@]}" "$PY" -m pytest -q' in text
    assert 'run_pytest_gate PYTHON_FULL "${PYTEST_ENV[@]}" "$PY" -m pytest -q' in text
    assert 'run_gate TARGETED_PYTHON "${PYTEST_ENV[@]}" "$PY" -m pytest -q' not in text
    assert 'run_gate PYTHON_FULL "${PYTEST_ENV[@]}" "$PY" -m pytest -q' not in text


def test_canonical_shellcheck_owns_every_pr1600_trust_runner() -> None:
    text = _text()
    required_shell_scripts = (
        "scripts/ops/fail_closed_gate.sh",
        "scripts/ops/living_fleet_dispatch.sh",
        "scripts/ops/accept_release_trust_pr.sh",
        "scripts/ops/repair_verify_catalog_exact_head.sh",
        "scripts/ops/run_pr1600_exact_focused.sh",
        "scripts/ops/run_pr1600_live_focused_acceptance.sh",
        "scripts/ops/run_pr1600_live_full_acceptance.sh",
    )
    assert "run_gate SHELLCHECK shellcheck" in text
    for path in required_shell_scripts:
        assert path in text


def test_docker_web_fallback_is_fail_closed_and_does_not_mutate_host_node() -> None:
    text = _text()
    assert 'run_gate WEB_NPM_CI docker run --rm' in text
    assert 'run_gate WEB_ACCEPTANCE docker run --rm' in text
    assert "nvm install" not in text
    assert "apt install" not in text
    assert "npm install -g" not in text


def test_targeted_acceptance_covers_every_high_risk_contract_changed_in_pr() -> None:
    text = _text()
    required_targets = (
        "tests/test_fail_closed_gate.py",
        "tests/test_release_trust_acceptance_script.py",
        "tests/test_living_fleet_shell_safety.py",
        "tests/test_living_fleet_guards.py",
        "tests/test_wave6_pilot_brief.py",
        "tests/test_delivery_workspace_created.py",
        "tests/test_delivery_requires_acceptance_criteria.py",
        "tests/test_proof_pack_generated.py",
        "tests/test_ai_workforce_policy.py",
        "tests/test_active_operator_commercial_authority.py",
        "tests/test_billing_router_mounted.py",
        "tests/test_billing_moyasar_safety.py",
        "tests/test_pricing_plans_endpoint.py",
        "tests/test_apps_web_launch_truth.py",
        "tests/test_commercial_map.py",
        "tests/test_service_catalog.py",
        "tests/test_customer_portal_contract_final.py",
        "tests/test_customer_portal_empty_states_final.py",
        "tests/test_customer_portal_full_ops.py",
        "tests/test_frontend_professional_polish.py",
        "tests/test_public_launch_truth.py",
        "tests/test_railway_canonical_contract.py",
        "tests/test_canonical_daily_workflow_contract.py",
    )
    for target in required_targets:
        assert target in text


def test_acceptance_runner_contains_no_material_execution_verbs() -> None:
    text = _text().lower()
    forbidden_commands = (
        "git merge ",
        "gh pr merge",
        "railway up",
        "railway redeploy",
        "railway variables set",
        "kubectl apply",
    )
    for token in forbidden_commands:
        assert token not in text


def test_full_pytest_is_explicit_mode_and_still_fail_closed() -> None:
    text = _text()
    assert "DEALIX_ACCEPT_FULL_PYTEST" in text
    assert 'run_pytest_gate PYTHON_FULL "${PYTEST_ENV[@]}" "$PY" -m pytest -q' in text
    assert "PYTHON_FULL=SKIPPED_BY_MODE" in text
