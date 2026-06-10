#!/usr/bin/env bash
# Railway production bootstrap — migrations + GTM seed (run once after deploy).
# Usage:
#   export DATABASE_URL=postgresql+asyncpg://...
#   export DEALIX_API_BASE=https://api.dealix.me
#   bash scripts/railway_prod_bootstrap.sh
#   bash scripts/railway_prod_bootstrap.sh --seed-only
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SEED_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --seed-only) SEED_ONLY=1 ;;
  esac
done

PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "RAILWAY_BOOTSTRAP: FAIL — python3 not found"
  exit 1
fi

echo "== Railway production bootstrap =="
echo ""
echo "== Required env (set in Railway + GitHub Secrets) =="
echo "  API: DATABASE_URL, APP_SECRET_KEY, ENVIRONMENT=production, CORS_ORIGINS"
echo "  API: DEALIX_ADMIN_API_KEY (or API_KEYS) for /ops-autopilot/*"
echo "  API: MOYASAR_SECRET_KEY, MOYASAR_WEBHOOK_SECRET (payments)"
echo "  FE:  NEXT_PUBLIC_API_URL, NEXT_PUBLIC_DEALIX_ADMIN_API_KEY"
echo "  CI:  DEALIX_API_BASE, DEALIX_API_KEY, DEALIX_ADMIN_API_KEY"
echo ""

if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "RAILWAY_BOOTSTRAP: SKIP migrations/seed — DATABASE_URL not set"
  echo "  Set DATABASE_URL then re-run."
  exit 0
fi

if [[ "$SEED_ONLY" -eq 0 ]]; then
  echo "== Alembic upgrade head =="
  if command -v alembic >/dev/null 2>&1; then
    alembic upgrade head
  else
    $PYTHON_BIN -m alembic upgrade head
  fi
  echo ""
fi

echo "== Seed revenue-machine candidates (gtm_seed_*) =="
$PYTHON_BIN "${ROOT}/scripts/seed_revenue_machine_candidates.py"
echo ""

if [[ -n "${DEALIX_API_BASE:-}" ]]; then
  echo "== War Room import from default CSV (optional) =="
  ADMIN="${DEALIX_ADMIN_API_KEY:-}"
  if [[ -n "$ADMIN" ]] && command -v curl >/dev/null 2>&1; then
    curl -fsS -X POST "${DEALIX_API_BASE%/}/api/v1/ops-autopilot/war-room/import-targets" \
      -H "Content-Type: application/json" \
      -H "X-Admin-API-Key: ${ADMIN}" \
      -d '{"use_default_csv": true}' || echo "  (import skipped — check admin key)"
  else
    echo "  Set DEALIX_ADMIN_API_KEY + curl to import war-room targets via API"
  fi
fi

echo ""
echo "RAILWAY_BOOTSTRAP: OK"
echo "Next: bash scripts/official_launch_verify.sh --api-base \${DEALIX_API_BASE}"
