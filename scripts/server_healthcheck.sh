#!/usr/bin/env bash
# Health check for self-hosted Dealix Docker deployment.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ENV_FILE="${ENV_FILE:-.env.prod}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE"
  exit 1
fi

echo "=== Docker compose status ==="
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps

echo "=== API internal health ==="
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T api curl -fsS http://localhost:8000/healthz

echo "=== API deep health ==="
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T api curl -fsS 'http://localhost:8000/healthz?deep=1' || true

echo "=== Frontend internal health ==="
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T frontend wget -qO- http://localhost:3000/healthz

echo "=== Resource usage ==="
docker stats --no-stream dealix-api dealix-frontend dealix-postgres dealix-pgbouncer dealix-redis dealix-caddy || true

echo "DEALIX_SERVER_HEALTHCHECK_OK"
