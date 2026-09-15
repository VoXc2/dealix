"""Converged self-host/Railway-exit cutover contract.

Single source authority after #2026 + #2030 convergence:

- ``deploy/selfhost/compose.yml`` is the ONLY runnable self-host plane.
- ``docker-compose.prod.yml`` and legacy ``scripts/server_*.sh`` entrypoints
  are retired non-authoritative history and must fail closed.
- #2026 proven controls are preserved on the canonical plane:
  exact full GIT_SHA source/build/running parity, custom-format backup +
  checksum + TOC, isolated pgvector restore rehearsal, fail-closed migration
  with no inferred publication consent, application-only rollback (never the
  database), explicit L5 cutover flag, no production secrets in repo.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
files = {
    "retired_compose": ROOT / "docker-compose.prod.yml",
    "legacy_deploy": ROOT / "scripts/server_deploy.sh",
    "legacy_backup": ROOT / "scripts/server_backup.sh",
    "legacy_health": ROOT / "scripts/server_healthcheck.sh",
    "canonical_compose": ROOT / "deploy/selfhost/compose.yml",
    "backup_runner": ROOT / "scripts/ops/backup_postgres_snapshot.sh",
    "restore": ROOT / "scripts/restore_test.sh",
    "migrate": ROOT / "scripts/ops/migrate_railway_backup_to_selfhost.py",
    "rollback": ROOT / "scripts/ops/selfhost_release_rollback.sh",
    "env": ROOT / ".env.prod.example",
    "plane": ROOT / "docs/ops/SELFHOSTED_PRODUCTION_PLANE.md",
    "cutover": ROOT / "scripts/ops/selfhost_public_cutover.sh",
}
text = {k: p.read_text(encoding="utf-8") for k, p in files.items()}

required = {
    # One canonical runnable plane only; the retired stack stays history.
    "retired_compose": [
        "HISTORICAL_REFERENCE_NON_AUTHORITATIVE",
        "canonical_compose: deploy/selfhost/compose.yml",
        "services: {}",
    ],
    "legacy_deploy": ["SELFHOST_LEGACY_ENTRYPOINT=HOLD", "exit 78"],
    "legacy_backup": ["SELFHOST_LEGACY_ENTRYPOINT=HOLD", "exit 78"],
    "legacy_health": ["SELFHOST_LEGACY_ENTRYPOINT=HOLD", "exit 78"],
    # Canonical plane: loopback-only canary + PG18/pgvector parity + SHA identity.
    "canonical_compose": [
        "127.0.0.1:${DEALIX_SELFHOST_API_PORT",
        "127.0.0.1:${DEALIX_SELFHOST_WEB_PORT",
        "127.0.0.1:${DEALIX_SELFHOST_INGRESS_PORT",
        "pgvector/pgvector:pg18",
        "GIT_SHA: ${DEALIX_GIT_SHA:?set exact DEALIX_GIT_SHA}",
        'profiles: ["public-cutover"]',
        "${DEALIX_PUBLIC_HTTP_BIND:-127.0.0.1:18080}:80",
        "${DEALIX_PUBLIC_HTTPS_BIND:-127.0.0.1:18443}:443",
        "image: dealix-api:${DEALIX_IMAGE_TAG:?set exact DEALIX_IMAGE_TAG}",
        "image: dealix-web:${DEALIX_IMAGE_TAG:?set exact DEALIX_IMAGE_TAG}",
    ],
    # Canonical backup runner: custom format + checksum + TOC, secret-file input.
    "backup_runner": [
        "pg_dump -Fc",
        "sha256sum",
        "pg_restore --list",
        "DEALIX_DATABASE_URL_FILE",
    ],
    # Isolated restore rehearsal with pgvector.
    "restore": [
        "pgvector/pgvector:pg18",
        "pg_restore --exit-on-error",
        "host_ports=none",
    ],
    # Fail-closed migration: explicit flag, lossless archive, no consent inference.
    "migrate": [
        "DEALIX_DB_MIGRATION",
        "operational_event_streams",
        "consent_for_publication",
        "publication_consent_inferred=false",
    ],
    # Application-only rollback: exact SHA, parity proof, never the database.
    "rollback": [
        "database_rollback=NEVER",
        "CONFIRM",
        "database_rollback=NOT_EXECUTED",
        "[0-9a-f]{40}",
        "deploy/selfhost/compose.yml",
        "DEALIX_GIT_SHA",
        "DEALIX_IMAGE_TAG",
    ],
    # Fail-closed production env template.
    "env": [
        "APP_ENV=production",
        "EXTERNAL_SEND_ENABLED=false",
        "WHATSAPP_ALLOW_LIVE_SEND=false",
        "PAYMENT_EXECUTION=0",
        "CHANGE_ME",
    ],
    # Explicit L5 cutover boundary on the canonical runbook.
    "plane": ["L5", "deploy/selfhost/compose.yml", "PRODUCTION_GREEN=NOT_PROVEN"],
    "cutover": ["--preflight", "--stage", "--cutover", "DEALIX_STAGE_PRODUCTION", "DEALIX_PUBLIC_CUTOVER", "CONFIRM_SHA", "0.0.0.0:80", "0.0.0.0:443", "DNS_MUTATION=NOT_EXECUTED", "PRODUCTION_GREEN=NOT_PROVEN"],
}
missing = [
    f"{name}:{needle}"
    for name, needles in required.items()
    for needle in needles
    if needle not in text[name]
]
forbidden = {
    # Retired files must not be revivable as a parallel runnable stack.
    "retired_compose": ['"80:80"', '"443:443"', "postgres:16", "container_name: dealix"],
    "legacy_deploy": ["docker compose"],
    "legacy_backup": ["docker compose"],
    "legacy_health": ["docker compose"],
    # Canonical canary must never bind public ingress ports itself.
    "canonical_compose": ['"80:80"', '"443:443"', "image: postgres:16"],
    "cutover": ["railway up", "railway redeploy", "cloudflare", "aws route53"],
    # Backup must never leak the DB password through env/config/args.
    "backup_runner": ["-e PGPASSWORD"],
    # Rollback must never mutate the database.
    "rollback": ["git reset --hard", "alembic downgrade", "pg_restore"],
}
present = [
    f"{name}:{needle}"
    for name, needles in forbidden.items()
    for needle in needles
    if needle in text[name]
]
if missing or present:
    print(f"SELFHOST_CUTOVER_CONTRACT=FAIL missing={missing} forbidden={present}")
    raise SystemExit(1)
print("SELFHOST_CUTOVER_CONTRACT=PASS")
