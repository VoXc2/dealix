#!/usr/bin/env bash
# scripts/restore_test.sh
# Quarterly restore drill: take the latest hourly backup and restore it to a
# scratch Postgres DB, then verify table row counts against expected baseline.
#
# Required env:
#   BACKUP_FILE              path to .pgdump or .pgdump.enc (latest by default)
#   BACKUP_LOCAL_DIR         where to find backups (default: /var/backups/dealix)
#   BACKUP_ENCRYPTION_KEY    if file is .enc
#   RESTORE_DATABASE_URL     scratch DB for restore (must be empty / disposable!)
#   EXPECTED_MIN_LEADS       minimum lead row count after restore (default: 100)
#
# Exit codes:
#   0  drill passed
#   1  missing env / no backup found
#   2  decryption failed
#   3  pg_restore failed
#   4  data integrity check failed

set -euo pipefail
log() { echo "[restore_test] $(date -Iseconds) $*"; }
die() { log "FATAL: $*"; exit "${2:-1}"; }

: "${RESTORE_DATABASE_URL:?RESTORE_DATABASE_URL is required (must NOT be production)}"
LOCAL_DIR="${BACKUP_LOCAL_DIR:-/var/backups/dealix}"
EXPECTED_MIN_LEADS="${EXPECTED_MIN_LEADS:-100}"

# Safety check — refuse to run against URLs that look like production
case "${RESTORE_DATABASE_URL}" in
  *prod*|*production*|*railway.app*|*neon.tech*)
    die "RESTORE_DATABASE_URL looks like production — refusing to run drill" 1
    ;;
esac

# Locate the latest backup
if [[ -z "${BACKUP_FILE:-}" ]]; then
  BACKUP_FILE="$(ls -t "${LOCAL_DIR}"/dealix-*.pgdump* 2>/dev/null | head -n1 || true)"
fi
[[ -n "${BACKUP_FILE}" && -f "${BACKUP_FILE}" ]] || die "no backup found in ${LOCAL_DIR}" 1
log "drill target backup: ${BACKUP_FILE}"

# Decrypt if needed
WORK_FILE="${BACKUP_FILE}"
if [[ "${BACKUP_FILE}" == *.enc ]]; then
  [[ -n "${BACKUP_ENCRYPTION_KEY:-}" ]] || die "BACKUP_ENCRYPTION_KEY required for .enc" 1
  WORK_FILE="${BACKUP_FILE%.enc}.tmp"
  log "decrypting → ${WORK_FILE}"
  openssl enc -aes-256-cbc -d -pbkdf2 \
    -in "${BACKUP_FILE}" -out "${WORK_FILE}" \
    -pass "pass:${BACKUP_ENCRYPTION_KEY}" || die "decryption failed" 2
fi

PG_URL="$(echo "${RESTORE_DATABASE_URL}" | sed -E 's#postgresql\+asyncpg://#postgresql://#')"

log "restoring → ${PG_URL}"
pg_restore --clean --if-exists --no-owner --no-privileges \
  --dbname="${PG_URL}" "${WORK_FILE}" || die "pg_restore failed" 3

# Cleanup decrypted temp
[[ "${WORK_FILE}" != "${BACKUP_FILE}" ]] && rm -f "${WORK_FILE}"

# Integrity: count rows in key tables
log "verifying row counts"
LEAD_COUNT="$(psql "${PG_URL}" -tAc 'SELECT COUNT(*) FROM accounts;' 2>/dev/null || echo "0")"
log "accounts rows: ${LEAD_COUNT}"

if (( LEAD_COUNT < EXPECTED_MIN_LEADS )); then
  die "expected >= ${EXPECTED_MIN_LEADS} accounts, got ${LEAD_COUNT}" 4
fi

log "DRILL PASSED ✓ — restored backup is usable"
