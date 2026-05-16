#!/usr/bin/env bash
# dealix_local_stack_verify.sh
# ─────────────────────────────────────────────────────────────────────────────
# End-to-end local verification: Docker data plane (Postgres, PgBouncer, Redis,
# Mongo) + Python gates + in-process API smoke + optional real TCP /health
# + Next.js lint/typecheck/build + Playwright Tier-1 smoke.
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
LANDING_HTTP_PID=""
DOCKER_COMPOSE=(docker compose)

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
  if [[ -n "${LANDING_HTTP_PID:-}" ]]; then
    kill "$LANDING_HTTP_PID" 2>/dev/null || true
  fi
  if [[ "$TEARDOWN" -eq 1 ]] && [[ "$SKIP_DOCKER" -eq 0 ]]; then
    echo "== docker compose down =="
    "${DOCKER_COMPOSE[@]}" down || true
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
export REDIS_PASSWORD="${REDIS_PASSWORD:-dev_redis_secret}"
export MONGO_PASSWORD="${MONGO_PASSWORD:-dev_mongo_secret}"

RP="$REDIS_PASSWORD"
MP="$MONGO_PASSWORD"

if [[ "$SKIP_DOCKER" -eq 0 ]]; then
  command -v docker >/dev/null 2>&1 || {
    echo "ERROR: docker not found. Install Docker or pass --skip-docker."
    exit 1
  }

  if ! docker info >/dev/null 2>&1; then
    if command -v sudo >/dev/null 2>&1 && sudo -n docker info >/dev/null 2>&1; then
      DOCKER_COMPOSE=(sudo --preserve-env=REDIS_PASSWORD,MONGO_PASSWORD docker compose)
      echo "docker socket requires sudo; using sudo docker compose."
    else
      echo "ERROR: docker daemon unavailable or current user lacks docker socket permissions."
      echo "Try: sudo service docker start && sudo usermod -aG docker $USER"
      echo "Or rerun with --skip-docker if external services are already reachable."
      exit 1
    fi
  fi

  echo "== Docker Compose: postgres, pgbouncer, redis, mongo =="
  "${DOCKER_COMPOSE[@]}" up -d --force-recreate postgres pgbouncer redis mongo

  echo "== Wait for Postgres (pg_isready) =="
  ok=0
  for _ in $(seq 1 45); do
    if "${DOCKER_COMPOSE[@]}" exec -T postgres pg_isready -U ai_user -d ai_company >/dev/null 2>&1; then
      ok=1
      break
    fi
    sleep 2
  done
  if [[ "$ok" -ne 1 ]]; then
    echo "ERROR: Postgres did not become ready in time."
    "${DOCKER_COMPOSE[@]}" logs postgres --tail 80 || true
    exit 1
  fi
  echo "postgres: ready"

  echo "== Redis PING =="
  ok=0
  for _ in $(seq 1 45); do
    if "${DOCKER_COMPOSE[@]}" exec -T redis redis-cli -a "$RP" ping 2>/dev/null | grep -q PONG; then
      ok=1
      break
    fi
    sleep 2
  done
  if [[ "$ok" -ne 1 ]]; then
    echo "ERROR: Redis ping failed"
    "${DOCKER_COMPOSE[@]}" logs redis --tail 40 || true
    exit 1
  fi
  echo "redis: PONG"

  echo "== Mongo admin ping =="
  ok=0
  for _ in $(seq 1 45); do
    if "${DOCKER_COMPOSE[@]}" exec -T mongo mongosh "mongodb://mongo_user:${MP}@127.0.0.1:27017/admin" --quiet --eval "db.adminCommand('ping').ok" 2>/dev/null | grep -q 1; then
      ok=1
      break
    fi
    sleep 2
  done
  if [[ "$ok" -ne 1 ]]; then
    echo "ERROR: Mongo ping failed"
    "${DOCKER_COMPOSE[@]}" logs mongo --tail 40 || true
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
if ! bash scripts/business_readiness_verify.sh; then
  echo "business readiness policy flags present (non-blocking for local stack runtime checks)."
fi

echo "== audit_orphan_endpoints =="
if ! $PYTHON scripts/audit_orphan_endpoints.py --quiet; then
  echo "frontend/backend wiring drift detected (non-blocking for local stack runtime checks)."
fi

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
  echo "== frontend: npm ci, lint, typecheck, build =="
  FRONTEND_HAS_ESLINT_CONFIG=0
  for eslint_cfg in \
    ".eslintrc" \
    ".eslintrc.js" \
    ".eslintrc.cjs" \
    ".eslintrc.json" \
    "eslint.config.js" \
    "eslint.config.mjs" \
    "eslint.config.cjs"; do
    if [[ -f "$ROOT/frontend/$eslint_cfg" ]]; then
      FRONTEND_HAS_ESLINT_CONFIG=1
      break
    fi
  done

  (
    cd frontend
    npm ci
    if [[ "$FRONTEND_HAS_ESLINT_CONFIG" -eq 1 ]]; then
      npm run lint
    else
      echo "frontend lint skipped: no ESLint config file found."
    fi
    npm run typecheck
    npm run build
  )

  echo "== Playwright Tier-1 smoke (landing served statically) =="
  PW_PORT="${PLAYWRIGHT_PORT:-8765}"
  $PYTHON -m http.server "$PW_PORT" --directory landing >/dev/null 2>&1 &
  LANDING_HTTP_PID=$!
  sleep 2
  (cd tests/playwright \
    && npm install \
    && npx playwright install --with-deps chromium \
    && PLAYWRIGHT_BASE_URL="http://localhost:${PW_PORT}" CI=true \
       npx playwright test --config playwright.config.js)
  kill "$LANDING_HTTP_PID" 2>/dev/null || true
  LANDING_HTTP_PID=""
fi

echo "=============================================="
echo "DEALIX_LOCAL_STACK_VERIFY=OK"
echo "=============================================="
