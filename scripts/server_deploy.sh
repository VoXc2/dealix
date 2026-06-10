#!/usr/bin/env bash
# Deploy Dealix on a Docker host from an already-cloned repository.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ENV_FILE="${ENV_FILE:-.env.prod}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE. Copy .env.prod.example to $ENV_FILE and fill real values."
  exit 1
fi

export GIT_SHA="${GIT_SHA:-$(git rev-parse --short HEAD 2>/dev/null || echo local)}"
export IMAGE_TAG="${IMAGE_TAG:-$GIT_SHA}"

echo "=== Dealix deploy ==="
echo "GIT_SHA=$GIT_SHA"
echo "IMAGE_TAG=$IMAGE_TAG"

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" build
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d --remove-orphans
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps

echo "=== Health checks ==="
sleep 8
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T api curl -fsS http://localhost:8000/healthz
if docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps frontend >/dev/null 2>&1; then
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T frontend wget -qO- http://localhost:3000/healthz >/dev/null
fi

echo "DEALIX_SERVER_DEPLOY_OK"
