#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pass() { printf "✅ %s\n" "$1"; }
fail() { printf "❌ %s\n" "$1"; exit 1; }
warn() { printf "⚠️ %s\n" "$1"; }

run_step() {
  local name="$1"
  shift
  printf "\n▶ %s\n" "$name"
  if "$@"; then
    pass "$name"
  else
    fail "$name"
  fi
}

cd "$ROOT_DIR"

run_step "Python available" python --version
run_step "Node available" node --version
run_step "Docker available" docker --version

run_step "Infra up (postgres+redis)" docker compose up -d postgres redis

run_step "Revenue OS master verify" bash scripts/revenue_os_master_verify.sh

run_step "Backend quick regression" \
  pytest tests/test_pg_event_store.py tests/test_model_router.py tests/test_integrations.py tests/test_v5_layers.py tests/unit/test_compliance_os.py -q --no-cov

if [ -d frontend ]; then
  pushd frontend >/dev/null

  if [ ! -d node_modules ]; then
    warn "frontend/node_modules not found; running npm ci"
    npm ci
  fi

  run_step "Frontend lint" npm run lint
  run_step "Frontend typecheck" npm run typecheck
  run_step "Frontend build" npm run build

  popd >/dev/null
else
  warn "Frontend directory not found; skipping frontend checks"
fi

pass "Enterprise readiness checks completed"
