#!/usr/bin/env bash
# Official launch gate — company ready + go-live + GTM stack + optional prod health + FE build.
# Usage:
#   bash scripts/official_launch_verify.sh
#   bash scripts/official_launch_verify.sh --api-base https://api.dealix.me --admin-key "$KEY"
#   bash scripts/official_launch_verify.sh --skip-fe-build
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

SKIP_FE=0
SKIP_GO_LIVE=0
API_BASE="${DEALIX_API_BASE:-}"
ADMIN_KEY="${DEALIX_ADMIN_API_KEY:-}"
for arg in "$@"; do
  case "$arg" in
    --skip-fe-build) SKIP_FE=1 ;;
    --skip-go-live) SKIP_GO_LIVE=1 ;;
    --api-base=*) API_BASE="${arg#*=}" ;;
    --admin-key=*) ADMIN_KEY="${arg#*=}" ;;
  esac
done
# Also accept positional-style from env after loop
for arg in "$@"; do
  if [[ "$arg" == --api-base ]] && [[ $# -gt 0 ]]; then API_BASE="${2:-}"; fi
done

FAIL=0
PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
fi

echo "== Official Launch Verify =="
echo "  api_base: ${API_BASE:-<local only>}"
echo ""

echo "== 1/5 company_ready_verify =="
if bash "${ROOT}/scripts/company_ready_verify.sh" $([[ "$SKIP_GO_LIVE" -eq 1 ]] && echo --skip-go-live); then
  echo "  company_ready: PASS"
else
  echo "  company_ready: FAIL"
  FAIL=1
fi
echo ""

if [[ "$SKIP_GO_LIVE" -eq 0 ]]; then
  echo "== 2/5 founder_go_live_verify =="
  if bash "${ROOT}/scripts/founder_go_live_verify.sh"; then
    echo "  go_live: PASS"
  else
    echo "  go_live: FAIL (use --skip-go-live to ignore)"
    FAIL=1
  fi
  echo ""
else
  echo "== 2/5 founder_go_live: skipped =="
fi

echo "== 3/5 GTM commercial stack pytest =="
if $PYTHON_BIN -m pytest tests/test_gtm_commercial_stack.py tests/test_official_launch_verify.py -q --no-cov; then
  echo "  gtm_tests: PASS"
else
  echo "  gtm_tests: FAIL"
  FAIL=1
fi
echo ""

if [[ "$SKIP_FE" -eq 0 ]] && [[ -f "${ROOT}/frontend/package.json" ]]; then
  echo "== 4/5 Frontend production build =="
  if command -v npm >/dev/null 2>&1; then
  (
    cd "${ROOT}/frontend"
    if npm run build --silent; then
      echo "  fe_build: PASS"
    else
      echo "  fe_build: FAIL"
      FAIL=1
    fi
  )
  else
    echo "  fe_build: SKIP (npm not found)"
  fi
else
  echo "== 4/5 Frontend build: skipped =="
fi
echo ""

echo "== 5/5 Production API smoke =="
if [[ -n "$API_BASE" ]]; then
  if command -v curl >/dev/null 2>&1; then
    if curl -fsS "${API_BASE%/}/health" >/dev/null 2>&1; then
      echo "  health: PASS"
    else
      echo "  health: FAIL"
      FAIL=1
    fi
    if [[ -n "$ADMIN_KEY" ]]; then
      for path in \
        "/api/v1/ops-autopilot/marketing/social-today" \
        "/api/v1/ops-autopilot/war-room/today-pack" \
        "/api/v1/ops-autopilot/founder/daily-pack"; do
        code=$(curl -sS -o /dev/null -w "%{http_code}" \
          "${API_BASE%/}${path}" -H "X-Admin-API-Key: ${ADMIN_KEY}" || echo "000")
        if [[ "$code" == "200" ]]; then
          echo "  ${path}: PASS"
        else
          echo "  ${path}: FAIL (http ${code})"
          FAIL=1
        fi
      done
    else
      echo "  ops endpoints: SKIP (set DEALIX_ADMIN_API_KEY)"
    fi
  else
    echo "  api_smoke: SKIP (curl missing)"
  fi
else
  echo "  api_smoke: SKIP (set DEALIX_API_BASE or --api-base)"
fi
echo ""

echo "== Founder launch checklist (manual) =="
echo "  [ ] GitHub secrets: DEALIX_API_BASE, DEALIX_API_KEY, DEALIX_ADMIN_API_KEY"
echo "  [ ] Railway: MOYASAR live + webhook"
echo "  [ ] kpi_founder_commercial_import.yaml from CRM"
echo "  [ ] agency_accounts_seed.csv warm names (not placeholders)"
echo "  [ ] First 10 approved touches + evidence row today"
echo "  Doc: docs/company/DEALIX_COMPANY_READY_MASTER_AR.md"
echo ""

if [[ "$FAIL" -eq 0 ]]; then
  echo "OFFICIAL_LAUNCH_VERDICT=PASS"
  exit 0
fi
echo "OFFICIAL_LAUNCH_VERDICT=FAIL"
exit 1
