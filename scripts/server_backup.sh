#!/usr/bin/env bash
set -Eeuo pipefail

cat >&2 <<'EOF'
SELFHOST_LEGACY_ENTRYPOINT=HOLD
scripts/server_backup.sh depended on the retired docker-compose.prod.yml stack and is not current backup authority.
Do not infer a production database from stale Compose names.
Canonical snapshot runner: scripts/ops/backup_postgres_snapshot.sh (read-only DB, secret-file input, checksum + pg_restore list).
Current Railway exit additionally requires an isolated pgvector restore drill before explicit DB cutover authority.
Canonical production-plane runbook: docs/ops/SELFHOSTED_PRODUCTION_PLANE.md
EOF
exit 78
