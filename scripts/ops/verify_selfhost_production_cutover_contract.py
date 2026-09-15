from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
files = {
    "compose": ROOT / "docker-compose.prod.yml",
    "deploy": ROOT / "scripts/server_deploy.sh",
    "backup": ROOT / "scripts/server_backup.sh",
    "restore": ROOT / "scripts/restore_test.sh",
    "migrate": ROOT / "scripts/ops/migrate_railway_backup_to_selfhost.py",
    "rollback": ROOT / "scripts/ops/selfhost_release_rollback.sh",
    "env": ROOT / ".env.prod.example",
}
text = {k: p.read_text(encoding="utf-8") for k, p in files.items()}
required = {
    "compose": ["pgvector/pgvector:pg18", "postgres18_data", "GIT_SHA: ${GIT_SHA:?set exact GIT_SHA}", "ACME_EMAIL:", "DEALIX_ENV_FILE"],
    "deploy": ["--preflight", "--stage", "--cutover", "DEALIX_EXPECTED_SHA", "DEALIX_PUBLIC_CUTOVER", "PUBLIC_CUTOVER=NOT_EXECUTED", "export DEALIX_ENV_FILE"],
    "backup": ["pg_dump -Fc", "pg_restore --list", "sha256sum", "DEALIX_EXPECTED_SHA", "export DEALIX_ENV_FILE"],
    "restore": ["pgvector/pgvector:pg18", "pg_restore --exit-on-error", "host_ports=none"],
    "migrate": ["DEALIX_DB_MIGRATION", "operational_event_streams", "consent_for_publication", "publication_consent_inferred=false"],
    "rollback": ["database_rollback=NEVER", "--no-build api web", "CONFIRM", "database_rollback=NOT_EXECUTED", "export DEALIX_ENV_FILE"],
    "env": ["APP_ENV=production", "EXTERNAL_SEND_ENABLED=false", "WHATSAPP_ALLOW_LIVE_SEND=false", "PAYMENT_EXECUTION=0"],
}
missing = [f"{name}:{needle}" for name, needles in required.items() for needle in needles if needle not in text[name]]
forbidden = {
    "compose": ["image: postgres:16-alpine", "- postgres_data:/var/lib/postgresql/data"],
    "deploy": ["ps frontend", "exec -T frontend"],
    "backup": ["postgres.sql"],
    "rollback": ["git reset --hard", "alembic downgrade", "pg_restore"],
}
present = [f"{name}:{needle}" for name, needles in forbidden.items() for needle in needles if needle in text[name]]
if missing or present:
    print(f"SELFHOST_CUTOVER_CONTRACT=FAIL missing={missing} forbidden={present}")
    raise SystemExit(1)
print("SELFHOST_CUTOVER_CONTRACT=PASS")
