from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "deploy/selfhost/compose.yml"
RUNNER = ROOT / "scripts/ops/deploy_selfhosted_canary.sh"
INGRESS_RUNNER = ROOT / "scripts/ops/verify_selfhosted_ingress_canary.sh"
WEB_HEALTH = ROOT / "apps/web/app/healthz/route.ts"
DOCKERIGNORE = ROOT / ".dockerignore"


def main() -> int:
    compose = COMPOSE.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")
    ingress_runner = INGRESS_RUNNER.read_text(encoding="utf-8")
    web_health = WEB_HEALTH.read_text(encoding="utf-8") if WEB_HEALTH.exists() else ""
    dockerignore = DOCKERIGNORE.read_text(encoding="utf-8") if DOCKERIGNORE.exists() else ""

    required_compose = [
        "127.0.0.1:${DEALIX_SELFHOST_API_PORT:-18000}:8000",
        "127.0.0.1:${DEALIX_SELFHOST_WEB_PORT:-13000}:3000",
        "127.0.0.1:${DEALIX_SELFHOST_INGRESS_PORT:-18081}:80",
        'profiles: ["local-db"]',
        "POSTGRES_HOST_AUTH_METHOD: trust",
        "dealix-postgres-canary:/var/lib/postgresql",
        "APP_ENV: ${DEALIX_APP_ENV:-development}",
        "DATABASE_URL: ${DEALIX_DATABASE_URL:-postgresql+asyncpg://dealix_canary@postgres:5432/dealix_canary}",
        "GIT_SHA: ${DEALIX_GIT_SHA:?set exact DEALIX_GIT_SHA}",
        "APP_SECRET_KEY: ${APP_SECRET_KEY:-}",
        "JWT_SECRET_KEY: ${JWT_SECRET_KEY:-}",
        "API_KEYS: ${API_KEYS:-}",
        "ADMIN_API_KEYS: ${ADMIN_API_KEYS:-}",
        "image: dealix-api:${DEALIX_IMAGE_TAG:?set exact DEALIX_IMAGE_TAG}",
        "image: dealix-web:${DEALIX_IMAGE_TAG:?set exact DEALIX_IMAGE_TAG}",
        "pgvector/pgvector:pg18",
        'profiles: ["public-cutover"]',
        "${DEALIX_PUBLIC_HTTP_BIND:-127.0.0.1:18080}:80",
        "${DEALIX_PUBLIC_HTTPS_BIND:-127.0.0.1:18443}:443",
        "../../ops/caddy/Caddyfile:/etc/caddy/Caddyfile:ro",
        "EXTERNAL_SEND_ENABLED: \"false\"",
        "PAYMENT_EXECUTION: \"0\"",
        "restart: unless-stopped",
    ]
    required_runner = [
        "DEALIX_EXPECTED_SHA",
        "DEALIX_SELFHOST_LOCAL_DB",
        "DEALIX_SELFHOST_API_PORT",
        "DEALIX_SELFHOST_WEB_PORT",
        "BASH_SOURCE[0]",
        'REPO="${DEALIX_REPO:-$DEFAULT_REPO}"',
        'COMPOSE_PROJECT_NAME="dealix-selfhost-${CURRENT_SHA:0:12}"',
        "exact-head mismatch",
        "DEALIX_ALLOW_FRESH_DB_BOOTSTRAP=1",
        "bootstrap_fresh_database.py --confirm-empty-bootstrap",
        "check_alembic_version_capacity.py",
        "CANARY_RELEASE=PASS",
        "dealix-api",
        "dealix-web",
        'data.get("git_sha") != expected',
        "SELFHOST_CANARY=PASS",
        "PUBLIC_CUTOVER=NOT_EXECUTED",
        "LOCAL_POSTGRES=CANARY_ONLY",
    ]
    required_ingress_runner = [
        "DEALIX_EXPECTED_SHA",
        "BASH_SOURCE[0]",
        'REPO="${DEALIX_REPO:-$DEFAULT_REPO}"',
        'COMPOSE_PROJECT_NAME="dealix-selfhost-${EXPECTED_SHA:0:12}"',
        "SELFHOST_INGRESS_CANARY=PASS",
        "DEALIX_SELFHOST_INGRESS_PORT",
        "PUBLIC_PORTS_80_443=NOT_OPENED_BY_THIS_RUNNER",
    ]
    required_web_health = [
        'service: "dealix-web"',
        "DEALIX_RELEASE_SHA",
        "RAILWAY_GIT_COMMIT_SHA",
        "VERCEL_GIT_COMMIT_SHA",
        "NEXT_PUBLIC_GIT_SHA",
        "process.env.GIT_SHA",
        "git_sha: gitSha",
        '"cache-control": "no-store"',
    ]
    required_dockerignore = [
        "**/.venv",
        "**/__pycache__",
        "**/node_modules",
        "**/.next",
        "**/.turbo",
    ]

    missing = [x for x in required_compose if x not in compose]
    missing += [x for x in required_runner if x not in runner]
    missing += [f"ingress:{x}" for x in required_ingress_runner if x not in ingress_runner]
    missing += [f"web_health:{x}" for x in required_web_health if x not in web_health]
    missing += [f"dockerignore:{x}" for x in required_dockerignore if x not in dockerignore]
    forbidden = [
        "0.0.0.0:18000:8000",
        "0.0.0.0:13000:3000",
        "127.0.0.1:18000:8000",
        "127.0.0.1:13000:3000",
        "15432:5432",
        "dealix-postgres-canary:/var/lib/postgresql/data",
        "docker compose down -v",
        "railway up",
        "railway redeploy",
        "railway variables",
        "RAILWAY_TOKEN",
        "APP_ENV: production",
        "api bash /app/scripts/railway_predeploy.sh",
        'DEALIX_REPO:-/opt/dealix/workspace/dealix',
        'name: dealix-selfhost',
        'name: dealix-postgres-canary',
    ]
    all_selfhost_source = compose + runner + ingress_runner
    present_forbidden = [x for x in forbidden if x in all_selfhost_source]

    if missing or present_forbidden:
        print(f"SELFHOST_VERIFY=FAIL missing={missing} forbidden={present_forbidden}")
        return 1
    print("SELFHOST_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
