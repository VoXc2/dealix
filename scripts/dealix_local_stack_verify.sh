#!/usr/bin/env bash
# dealix_local_stack_verify.sh
# ─────────────────────────────────────────────────────────────────────────────
# End-to-end local verification: Docker data plane (Postgres, PgBouncer, Redis,
# Mongo) + Python gates + in-process API smoke + optional real TCP /health
# + Next.js lint/typecheck/unit/build + Playwright smoke.
#
# Usage:
#   bash scripts/dealix_local_stack_verify.sh
#   bash scripts/dealix_local_stack_verify.sh --skip-docker    # gates + frontend only
#   bash scripts/dealix_local_stack_verify.sh --skip-frontend  # faster when Node unused
#   bash scripts/dealix_local_stack_verify.sh --skip-uvicorn   # skip TCP uvicorn probe
#   bash scripts/dealix_local_stack_verify.sh --teardown      # docker compose down at end
#
# Env: PYTHON defaults to python3. Set REDIS_PASSWORD / MONGO_PASSWORD if non-default.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
SKIP_DOCKER=0
SKIP_FRONTEND=0
SKIP_UVICORN=0
TEARDOWN=0

for arg in "$@"; do
  case "$arg" in
    --skip-docker) SKIP_DOCKER=1 ;;
    --skip-frontend) SKIP_FRONTEND=1 ;;
    --skip-uvicorn) SKIP_UVICORN=1 ;;
    --teardown) TEARDOWN=1 ;;
    -h|--help)
      echo "Usage: $0 [--skip-docker] [--skip-frontend] [--skip-uvicorn] [--teardown]"
      exit 0
      ;;
  esac
done

cleanup() {
  if [[ "$TEARDOWN" -eq 1 ]] && [[ "$SKIP_DOCKER" -eq 0 ]]; then
    echo "== docker compose down =="
    docker compose down || true
  fi
}
trap cleanup EXIT

echo "=============================================="
echo "DEALIX LOCAL STACK VERIFY"
echo "ROOT=$ROOT PYTHON=$PYTHON"
echo "skip_docker=$SKIP_DOCKER skip_frontend=$SKIP_FRONTEND skip_uvicorn=$SKIP_UVICORN teardown=$TEARDOWN"
echo "=============================================="

export APP_ENV="${APP_ENV:-test}"
export APP_DEBUG="${APP_DEBUG:-false}"
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-test-anthropic-key}"
export DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY:-test-deepseek-key}"
export GROQ_API_KEY="${GROQ_API_KEY:-test-groq-key}"
export GLM_API_KEY="${GLM_API_KEY:-test-glm-key}"
export GOOGLE_API_KEY="${GOOGLE_API_KEY:-test-google-key}"

RP="${REDIS_PASSWORD:-dev_redis_secret}"
MP="${MONGO_PASSWORD:-dev_mongo_secret}"

if [[ "$SKIP_DOCKER" -eq 0 ]]; then
  command -v docker >/dev/null 2>&1 || {
    echo "ERROR: docker not found. Install Docker or pass --skip-docker."
    exit 1
  }
  echo "== Docker Compose: postgres, pgbouncer, redis, mongo =="
  docker compose up -d postgres pgbouncer redis mongo

  echo "== Wait for Postgres (pg_isready) =="
  ok=0
  for _ in $(seq 1 45); do
    if docker compose exec -T postgres pg_isready -U ai_user -d ai_company >/dev/null 2>&1; then
      ok=1
      break
    fi
    sleep 2
  done
  if [[ "$ok" -ne 1 ]]; then
    echo "ERROR: Postgres did not become ready in time."
    docker compose logs postgres --tail 80 || true
    exit 1
  fi
  echo "postgres: ready"

  echo "== Redis PING =="
  if ! docker compose exec -T redis redis-cli -a "$RP" ping 2>/dev/null | grep -q PONG; then
    echo "ERROR: Redis ping failed"
    docker compose logs redis --tail 40 || true
    exit 1
  fi
  echo "redis: PONG"

  echo "== Mongo admin ping =="
  if ! docker compose exec -T mongo mongosh "mongodb://mongo_user:${MP}@127.0.0.1:27017/admin" --quiet --eval "db.adminCommand('ping').ok" 2>/dev/null | grep -q 1; then
    echo "ERROR: Mongo ping failed"
    docker compose logs mongo --tail 40 || true
    exit 1
  fi
  echo "mongo: ok"

  export DATABASE_URL="${DATABASE_URL:-postgresql+asyncpg://ai_user:ai_password@127.0.0.1:5432/ai_company}"
  export REDIS_URL="${REDIS_URL:-redis://:${RP}@127.0.0.1:6379/0}"
  export MONGODB_URI="${MONGODB_URI:-mongodb://mongo_user:${MP}@127.0.0.1:27017/ai_company?authSource=admin}"
else
  export DATABASE_URL="${DATABASE_URL:-postgresql+asyncpg://ai_user:ai_password@127.0.0.1:5432/ai_company}"
fi

echo "== revenue_os_master_verify =="
bash scripts/revenue_os_master_verify.sh

echo "== business_readiness_verify =="
bash scripts/business_readiness_verify.sh

echo "== audit_orphan_endpoints =="
$PYTHON scripts/audit_orphan_endpoints.py --quiet

echo "== smoke_inprocess (ASGI transport) =="
$PYTHON scripts/smoke_inprocess.py

echo "== pytest quick regression bundle =="
$PYTHON -m pytest \
  tests/test_pg_event_store.py \
  tests/test_model_router.py \
  tests/test_integrations.py \
  tests/test_v5_layers.py \
  tests/unit/test_compliance_os.py \
  -q --no-cov

if [[ "$SKIP_UVICORN" -eq 0 ]] && [[ "$SKIP_DOCKER" -eq 0 ]]; then
  echo "== TCP uvicorn + curl /health =="
  PORT="${VERIFY_PORT:-18888}"
  $PYTHON -m uvicorn api.main:app --host 127.0.0.1 --port "$PORT" &
  UV_PID=$!
  tcp_ok=0
  for _ in $(seq 1 45); do
    if curl -sf "http://127.0.0.1:${PORT}/health" >/dev/null; then
      tcp_ok=1
      break
    fi
    if ! kill -0 "$UV_PID" 2>/dev/null; then
      echo "ERROR: uvicorn exited early"
      wait "$UV_PID" || true
      exit 1
    fi
    sleep 1
  done
  kill "$UV_PID" 2>/dev/null || true
  wait "$UV_PID" 2>/dev/null || true
  if [[ "$tcp_ok" -ne 1 ]]; then
    echo "ERROR: /health not reachable on port $PORT"
    exit 1
  fi
  echo "tcp /health: ok"
elif [[ "$SKIP_UVICORN" -eq 0 ]]; then
  echo "== TCP uvicorn + curl /health (skipped: use full run without --skip-docker) =="
fi

if [[ "$SKIP_FRONTEND" -eq 0 ]]; then
  echo "== frontend: npm ci, lint, typecheck, unit, build =="
  (cd frontend && npm ci && npm run lint && npm run typecheck && npm test && npm run build)
  echo "== frontend: Playwright e2e (Chromium) =="
  (cd frontend && npx playwright install --with-deps chromium && CI=true npm run test:e2e)
fi

echo "=============================================="
echo "DEALIX_LOCAL_STACK_VERIFY=OK"
echo "=============================================="
