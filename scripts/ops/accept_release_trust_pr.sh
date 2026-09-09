#!/usr/bin/env bash
# Canonical exact-head acceptance for Dealix P0 release-trust PRs.
# Read/test only: no merge, deploy, production mutation, network configuration,
# external send, payment, DB mutation, or secret mutation.
set -Eeuo pipefail
umask 077

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

EXPECTED_HEAD="${DEALIX_ACCEPT_EXPECTED_HEAD:-}"
EXPECTED_BASE="${DEALIX_ACCEPT_EXPECTED_BASE:-}"
FULL_PYTEST="${DEALIX_ACCEPT_FULL_PYTEST:-0}"
GATE="$ROOT/scripts/ops/fail_closed_gate.sh"
PY="$ROOT/.venv/bin/python"

log() { printf '[release-trust] %s\n' "$*"; }
fail_env() { printf 'BLOCKED_ENVIRONMENT=%s\n' "$1" >&2; exit 3; }
run_gate() { bash "$GATE" "$@"; }

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
[[ -x "$PY" ]] || fail_env "missing_repo_venv_python"
command -v shellcheck >/dev/null 2>&1 || fail_env "shellcheck_not_installed"
command -v node >/dev/null 2>&1 || fail_env "node_not_installed"
command -v npm >/dev/null 2>&1 || fail_env "npm_not_installed"

node_major="$(node -p 'Number(process.versions.node.split(".")[0])')"
if [[ "$node_major" != "20" && "$node_major" -lt 22 ]]; then
  printf 'NODE_RUNTIME=FAIL version=%s required="20 || >=22"\n' "$(node -v)" >&2
  exit 13
fi
printf 'NODE_RUNTIME=PASS version=%s\n' "$(node -v)"

if [[ -n "$EXPECTED_BASE" ]]; then
  run_gate GIT_DIFF_CHECK git diff --check "$EXPECTED_BASE"...HEAD
else
  run_gate GIT_DIFF_CHECK git diff --check HEAD~1..HEAD
fi

run_gate SHELLCHECK shellcheck \
  scripts/ops/fail_closed_gate.sh \
  scripts/ops/living_fleet_dispatch.sh \
  scripts/ops/accept_release_trust_pr.sh

TARGET_TESTS=(
  tests/test_fail_closed_gate.py
  tests/test_living_fleet_shell_safety.py
  tests/test_living_fleet_guards.py
  tests/test_wave6_pilot_brief.py
  tests/test_delivery_workspace_created.py
  tests/test_delivery_requires_acceptance_criteria.py
  tests/test_proof_pack_generated.py
  tests/test_ai_workforce_policy.py
  tests/test_active_operator_commercial_authority.py
  tests/test_billing_router_mounted.py
  tests/test_billing_moyasar_safety.py
  tests/test_pricing_plans_endpoint.py
)
run_gate TARGETED_PYTHON "$PY" -m pytest -q "${TARGET_TESTS[@]}"

run_gate BRAND_IDENTITY_V2 "$PY" scripts/ops/verify_brand_identity_v2.py

if command -v actionlint >/dev/null 2>&1; then
  run_gate ACTIONLINT actionlint
else
  printf 'ACTIONLINT=SKIPPED_ENVIRONMENT reason=not_installed\n'
fi

(
  cd apps/web
  run_gate WEB_NPM_CI npm ci
  run_gate WEB_ACCEPTANCE npm run verify
)

if [[ "$FULL_PYTEST" == "1" ]]; then
  run_gate PYTHON_FULL "$PY" -m pytest -q
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
