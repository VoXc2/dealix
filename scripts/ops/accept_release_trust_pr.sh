#!/usr/bin/env bash
# Canonical exact-head acceptance for Dealix P0 release-trust PRs.
# Read/test only: no merge, deploy, production mutation, network configuration,
# external send, payment, DB mutation, or secret mutation.
set -Eeuo pipefail
umask 077

SCRIPT_DIR="$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
cd "$ROOT"

EXPECTED_HEAD="${DEALIX_ACCEPT_EXPECTED_HEAD:-}"
EXPECTED_BASE="${DEALIX_ACCEPT_EXPECTED_BASE:-}"
FULL_PYTEST="${DEALIX_ACCEPT_FULL_PYTEST:-0}"
GATE="$ROOT/scripts/ops/fail_closed_gate.sh"
PY="${DEALIX_ACCEPT_PYTHON:-$ROOT/.venv/bin/python}"
NODE_IMAGE="${DEALIX_ACCEPT_NODE_IMAGE:-node:22-bookworm}"

# Acceptance must never inherit a production application/database context from
# the VPS. Tests that need another backend may override these values explicitly
# with monkeypatch, but the process-level baseline is always isolated test mode.
PYTEST_ENV=(
  env
  APP_ENV=test
  ENVIRONMENT=test
  APP_DEBUG=false
  DATABASE_URL=sqlite+aiosqlite:///:memory:
  DEALIX_APPROVAL_STORE_BACKEND=memory
  DEALIX_APPROVAL_DATABASE_URL=
  DEALIX_APPROVAL_ALLOW_SQLITE_TEST_BACKEND=1
)

log() { printf '[release-trust] %s\n' "$*"; }
fail_env() { printf 'BLOCKED_ENVIRONMENT=%s\n' "$1" >&2; exit 3; }
run_gate() { bash "$GATE" "$@"; }
run_pytest_gate() { ( umask 027; run_gate "$@" ); }

START_HEAD="$(git rev-parse HEAD)"
START_BRANCH="$(git branch --show-current || true)"
log "START_HEAD=$START_HEAD"
log "START_BRANCH=${START_BRANCH:-DETACHED}"

if [[ -n "$EXPECTED_HEAD" && "$START_HEAD" != "$EXPECTED_HEAD" ]]; then
  printf 'EXACT_HEAD=FAIL expected=%s actual=%s\n' "$EXPECTED_HEAD" "$START_HEAD" >&2
  exit 10
fi
printf 'EXACT_HEAD=PASS sha=%s\n' "$START_HEAD"

if [[ -n "$EXPECTED_BASE" ]]; then
  if ! git cat-file -e "${EXPECTED_BASE}^{commit}" 2>/dev/null; then
    printf 'EXPECTED_BASE_PRESENT=FAIL sha=%s\n' "$EXPECTED_BASE" >&2
    exit 11
  fi
  merge_base="$(git merge-base "$EXPECTED_BASE" "$START_HEAD")"
  if [[ "$merge_base" != "$EXPECTED_BASE" ]]; then
    printf 'EXPECTED_BASE_ANCESTRY=FAIL expected_base=%s merge_base=%s\n' "$EXPECTED_BASE" "$merge_base" >&2
    exit 12
  fi
  printf 'EXPECTED_BASE_ANCESTRY=PASS sha=%s\n' "$EXPECTED_BASE"
fi

[[ -f "$GATE" ]] || fail_env "missing_fail_closed_gate"
[[ -x "$PY" ]] || fail_env "missing_accept_python:$PY"
command -v shellcheck >/dev/null 2>&1 || fail_env "shellcheck_not_installed"
command -v actionlint >/dev/null 2>&1 || fail_env "actionlint_not_installed"
printf 'PYTHON_RUNTIME=PASS path=%s\n' "$PY"
printf 'PYTEST_ISOLATION=PASS app_env=test environment=test database=sqlite_memory approval_store=memory\n'

WEB_NODE_MODE=""
host_node_major=0
if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
  host_node_major="$(node -p 'Number(process.versions.node.split(".")[0])' 2>/dev/null || printf '0')"
fi

# Web production currently builds/runs on Node 22 (apps/web/Dockerfile). Use
# host tooling only when it is production-equivalent; otherwise isolate Node 22
# in Docker instead of mutating host Node/npm.
if [[ "$host_node_major" == "22" ]]; then
  WEB_NODE_MODE="HOST_PRODUCTION_NODE22"
  printf 'NODE_RUNTIME=PASS mode=%s version=%s\n' "$WEB_NODE_MODE" "$(node -v)"
elif command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  WEB_NODE_MODE="DOCKER_NODE22"
  if ! docker image inspect "$NODE_IMAGE" >/dev/null 2>&1; then
    run_gate WEB_NODE22_PULL docker pull "$NODE_IMAGE"
  fi
  run_gate WEB_NODE22_RUNTIME docker run --rm "$NODE_IMAGE" node -e '
    const major = Number(process.versions.node.split(".")[0]);
    if (major !== 22) process.exit(13);
    console.log(process.version);
  '
  printf 'NODE_RUNTIME=PASS mode=%s image=%s\n' "$WEB_NODE_MODE" "$NODE_IMAGE"
else
  printf 'NODE_RUNTIME=BLOCKED host_version=%s required="production Node 22 or Docker Node 22" docker_available=false\n' \
    "$(node -v 2>/dev/null || printf 'missing')" >&2
  fail_env "production_equivalent_node22_unavailable"
fi

if [[ -n "$EXPECTED_BASE" ]]; then
  run_gate GIT_DIFF_CHECK git diff --check "$EXPECTED_BASE"...HEAD
else
  run_gate GIT_DIFF_CHECK git diff --check HEAD~1..HEAD
fi

# The canonical trust gate owns the complete shell surface used to repair and
# accept PR #1600. Wrapper scripts must not escape ShellCheck simply because a
# higher-level VPS driver happens to lint them separately.
run_gate SHELLCHECK shellcheck \
  scripts/ops/fail_closed_gate.sh \
  scripts/ops/living_fleet_dispatch.sh \
  scripts/ops/accept_release_trust_pr.sh \
  scripts/ops/repair_verify_catalog_exact_head.sh \
  scripts/ops/run_pr1600_exact_focused.sh \
  scripts/ops/run_pr1600_live_focused_acceptance.sh \
  scripts/ops/run_pr1600_live_full_acceptance.sh

# Keep the focused gate broad enough to cover every release-trust root cause
# changed by this PR, but bounded enough to iterate before the 9k+ full suite.
TARGET_TESTS=(
  tests/test_fail_closed_gate.py
  tests/test_release_trust_acceptance_script.py
  tests/test_pr1600_exact_focused_runner.py
  tests/test_pr1600_candidate_acceptance_safety.py

  tests/test_living_fleet_shell_safety.py
  tests/test_living_fleet_guards.py
  tests/test_living_fleet_acceptance_v4.py
  tests/test_living_fleet_concurrency_v1.py
  tests/test_living_fleet_terminal_crash_recovery_v1.py

  tests/test_wave6_pilot_brief.py
  tests/test_delivery_workspace_created.py
  tests/test_delivery_requires_acceptance_criteria.py
  tests/test_proof_pack_generated.py
  tests/test_ai_workforce_policy.py
  tests/test_ai_workforce_orchestrator.py
  tests/test_active_operator_commercial_authority.py

  tests/test_billing_router_mounted.py
  tests/test_billing_moyasar_safety.py
  tests/test_pricing_plans_endpoint.py
  tests/test_checkout_idempotency.py
  tests/test_commercial_map.py
  tests/test_service_catalog.py
  tests/test_service_setup.py
  tests/test_sector_intel.py
  tests/test_business_strategy.py
  tests/test_wave15_customer_journey_e2e.py
  tests/integration/test_full_customer_journey.py

  tests/test_distribution_api.py
  tests/test_distribution_os_doctrine.py
  tests/test_distribution_os_proposal_payment.py
  tests/test_distribution_os_followup_metrics.py
  tests/test_dealix_operating_system.py

  tests/test_apps_web_launch_truth.py
  tests/test_customer_portal_contract_final.py
  tests/test_customer_portal_empty_states_final.py
  tests/test_customer_portal_full_ops.py
  tests/test_frontend_professional_polish.py
  tests/test_public_launch_truth.py
  tests/test_railway_canonical_contract.py
  tests/test_canonical_daily_workflow_contract.py
  tests/test_canonical_ceo_doctrine_v3_truth.py

  tests/test_approval_center_postgres_cutover.py
  tests/test_durable_consent_migration_graph.py
  tests/test_market_signal_sources_v3.py
  tests/test_capability_frontier_v2_registry.py
  tests/test_v7_secret_leakage_guard.py
  tests/test_openclaw_local_memory_guard.py
  tests/test_vps_command_control_guards.py
  tests/test_vps_automation_runtime.py
  tests/test_verify_catalog.py
)
run_pytest_gate TARGETED_PYTHON "${PYTEST_ENV[@]}" "$PY" -m pytest -q "${TARGET_TESTS[@]}"

# Deterministic source-of-truth projections/verifiers. These are intentionally
# direct gates as well as pytest coverage so stale generated artifacts cannot be
# hidden by test selection or import order.
run_gate PUBLIC_SERVICE_CATALOG "$PY" scripts/dealix_export_service_catalog_json.py --check
run_gate MARKET_SIGNAL_SOURCES_V3 "$PY" scripts/ops/verify_market_signal_sources_v3.py
run_gate VERIFY_SCRIPT_CATALOG "$PY" scripts/ops/build_verify_catalog.py --check
run_gate BRAND_IDENTITY_V2 "$PY" scripts/ops/verify_brand_identity_v2.py
run_gate ACTIONLINT env SHELLCHECK_OPTS=--severity=warning actionlint

if [[ "$WEB_NODE_MODE" == "HOST_PRODUCTION_NODE22" ]]; then
  (
    cd apps/web
    run_gate WEB_NPM_CI npm ci
    run_gate WEB_ACCEPTANCE npm run verify
  )
else
  run_gate WEB_NPM_CI docker run --rm \
    --user "$(id -u):$(id -g)" \
    -e HOME=/tmp \
    -e npm_config_cache=/tmp/.npm \
    -v "$ROOT:/work" \
    -w /work/apps/web \
    "$NODE_IMAGE" \
    bash -lc 'npm ci'

  run_gate WEB_ACCEPTANCE docker run --rm \
    --user "$(id -u):$(id -g)" \
    -e HOME=/tmp \
    -e npm_config_cache=/tmp/.npm \
    -v "$ROOT:/work" \
    -w /work/apps/web \
    "$NODE_IMAGE" \
    bash -lc 'npm run verify'
fi

if [[ "$FULL_PYTEST" == "1" ]]; then
  run_pytest_gate PYTHON_FULL "${PYTEST_ENV[@]}" "$PY" -m pytest -q
else
  printf 'PYTHON_FULL=SKIPPED_BY_MODE set_DEALIX_ACCEPT_FULL_PYTEST=1_for_full_suite\n'
fi

END_HEAD="$(git rev-parse HEAD)"
if [[ "$END_HEAD" != "$START_HEAD" ]]; then
  printf 'HEAD_STABILITY=FAIL start=%s end=%s\n' "$START_HEAD" "$END_HEAD" >&2
  exit 14
fi
printf 'HEAD_STABILITY=PASS sha=%s\n' "$END_HEAD"
printf 'RELEASE_TRUST_ACCEPTANCE=PASS\n'