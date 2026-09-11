from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "deploy/selfhost/compose.yml"
RUNNER = ROOT / "scripts/ops/deploy_selfhosted_canary.sh"


def main() -> int:
    compose = COMPOSE.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")

    required_compose = [
        "127.0.0.1:18000:8000",
        "127.0.0.1:13000:3000",
        'profiles: ["local-db"]',
        "POSTGRES_HOST_AUTH_METHOD: trust",
        "dealix-postgres-canary:/var/lib/postgresql/data",
        "APP_ENV: ${DEALIX_APP_ENV:-development}",
        "DATABASE_URL: ${DEALIX_DATABASE_URL:-postgresql+asyncpg://dealix_canary@postgres:5432/dealix_canary}",
        "EXTERNAL_SEND_ENABLED: \"false\"",
        "PAYMENT_EXECUTION: \"0\"",
        "restart: unless-stopped",
    ]
    required_runner = [
        "DEALIX_EXPECTED_SHA",
        "DEALIX_SELFHOST_LOCAL_DB",
        "exact-head mismatch",
        "DEALIX_ALLOW_FRESH_DB_BOOTSTRAP=1",
        "bootstrap_fresh_database.py --confirm-empty-bootstrap",
        "check_alembic_version_capacity.py",
        "SELFHOST_CANARY=PASS",
        "PUBLIC_CUTOVER=NOT_EXECUTED",
        "LOCAL_POSTGRES=CANARY_ONLY",
    ]

    missing = [x for x in required_compose if x not in compose]
    missing += [x for x in required_runner if x not in runner]
    forbidden = [
        "0.0.0.0:18000:8000",
        "0.0.0.0:13000:3000",
        "15432:5432",
        "docker compose down -v",
        "railway up",
        "railway redeploy",
        "railway variables",
        "RAILWAY_TOKEN",
        "APP_ENV: production",
        "api bash /app/scripts/railway_predeploy.sh",
    ]
    present_forbidden = [x for x in forbidden if x in compose or x in runner]

    if missing or present_forbidden:
        print(f"SELFHOST_VERIFY=FAIL missing={missing} forbidden={present_forbidden}")
        return 1
    print("SELFHOST_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
