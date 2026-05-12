#!/usr/bin/env bash
# ─────────────────────────────────────────────────────
# dr_restore_drill.sh — quarterly disaster-recovery restore drill
#
# Restores the most recent pg_dump backup produced by `backup_pg.sh` into a
# *scratch* Postgres database, then runs smoke checks against it. Does NOT
# touch production data. Designed to be run by the on-call founder every
# quarter; a dry-run mode prints the plan without executing.
#
# Usage:
#   bash scripts/infra/dr_restore_drill.sh --dry-run     # plan only
#   bash scripts/infra/dr_restore_drill.sh               # execute
#
# Requires:
#   - psql + pg_restore on PATH
#   - $BACKUP_DIR with at least one recent dealix_*.sql.gz (default /var/backups/dealix)
#   - $DR_TARGET_DSN pointing at a SCRATCH Postgres (must not equal production!)
#
# Targets (see docs/sla.md §7):
#   RPO ≤ 24h (we take nightly snapshots)
#   RTO ≤ 4h for SEV-1
# ─────────────────────────────────────────────────────
set -euo pipefail

DRY_RUN="0"
for arg in "$@"; do
  case "$arg" in
    --dry-run|-n) DRY_RUN="1" ;;
    -h|--help)
      sed -n '1,30p' "$0"
      exit 0
      ;;
  esac
done

BACKUP_DIR="${BACKUP_DIR:-/var/backups/dealix}"
DR_TARGET_DSN="${DR_TARGET_DSN:-postgresql://dr_user:dr_pw@127.0.0.1:5432/dealix_dr_scratch}"
PROD_DSN="${DATABASE_URL:-}"

step() { printf '\n\033[1;34m→ %s\033[0m\n' "$1"; }
run()  { if [[ "$DRY_RUN" == "1" ]]; then printf '   [dry-run] %s\n' "$*"; else eval "$@"; fi; }

step "1. Safety check — refuse to target production"
if [[ -n "$PROD_DSN" && "$PROD_DSN" == "$DR_TARGET_DSN" ]]; then
  echo "ABORT: DR_TARGET_DSN must not equal DATABASE_URL. Refusing." >&2
  exit 2
fi
echo "   target: $DR_TARGET_DSN"
echo "   prod:   ${PROD_DSN:-<unset>} (won't be touched)"

step "2. Locate most recent backup"
if [[ ! -d "$BACKUP_DIR" ]]; then
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "   [dry-run] BACKUP_DIR=$BACKUP_DIR missing — in a live run this would abort."
    LATEST=""
  else
    echo "ABORT: BACKUP_DIR=$BACKUP_DIR does not exist." >&2
    exit 3
  fi
else
  LATEST="$(ls -1t "$BACKUP_DIR"/dealix_*.sql.gz 2>/dev/null | head -1 || true)"
fi
if [[ -z "${LATEST:-}" ]]; then
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "   [dry-run] no dealix_*.sql.gz found — live run would abort here."
  else
    echo "ABORT: no dealix_*.sql.gz in $BACKUP_DIR. Run backup_pg.sh first." >&2
    exit 4
  fi
else
  AGE_MIN=$(( ( $(date +%s) - $(stat -c %Y "$LATEST" 2>/dev/null || stat -f %m "$LATEST") ) / 60 ))
  echo "   backup:  $LATEST"
  echo "   age:     ${AGE_MIN}m ($(( AGE_MIN / 60 ))h $(( AGE_MIN % 60 ))m)"
  if (( AGE_MIN > 24 * 60 )); then
    echo "   WARN: backup older than 24h — RPO target violated."
  fi
fi

step "3. Reset scratch database"
run "psql \"$DR_TARGET_DSN\" -c 'DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public;'"

step "4. Restore"
run "gunzip -c \"$LATEST\" | psql \"$DR_TARGET_DSN\""

step "5. Smoke checks"
run "psql \"$DR_TARGET_DSN\" -c 'SELECT 1 AS scratch_ok;'"
run "psql \"$DR_TARGET_DSN\" -c \"SELECT count(*) AS public_tables FROM information_schema.tables WHERE table_schema='public';\""
# Spot-check a couple of business tables — adjust as schema evolves.
run "psql \"$DR_TARGET_DSN\" -c \"SELECT count(*) AS users FROM users;\" || true"
run "psql \"$DR_TARGET_DSN\" -c \"SELECT count(*) AS tenants FROM tenants;\" || true"

step "6. Done"
echo "   Drill complete. Capture timing in docs/ops/dr_drill.md and update the next-due date."
