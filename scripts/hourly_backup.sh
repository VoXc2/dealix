#!/usr/bin/env bash
# scripts/hourly_backup.sh
# Hourly Postgres backup → encrypted archive → S3 (or local fallback).
# Designed to run as a cron job: `0 * * * * /app/scripts/hourly_backup.sh`
#
# Required env:
#   DATABASE_URL              postgres://user:pass@host:5432/db
#   BACKUP_S3_BUCKET          s3 bucket name (optional; if absent, local-only)
#   BACKUP_S3_PREFIX          prefix inside bucket (default: dealix/hourly)
#   BACKUP_LOCAL_DIR          local fallback dir (default: /var/backups/dealix)
#   BACKUP_ENCRYPTION_KEY     32-byte hex key for openssl AES-256 encryption
#   BACKUP_RETENTION_HOURS    keep N hourly backups locally (default: 48)
#   AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION  (for s3)
#
# Exit codes:
#   0  success
#   1  missing required env
#   2  pg_dump failed
#   3  encryption failed
#   4  upload failed (non-fatal — local copy still kept)

set -euo pipefail

log() { echo "[hourly_backup] $(date -Iseconds) $*"; }
die() { log "FATAL: $*"; exit "${2:-1}"; }

: "${DATABASE_URL:?DATABASE_URL is required}"

LOCAL_DIR="${BACKUP_LOCAL_DIR:-/var/backups/dealix}"
RETENTION_HOURS="${BACKUP_RETENTION_HOURS:-48}"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
BASENAME="dealix-${TS}.pgdump"
LOCAL_PATH="${LOCAL_DIR}/${BASENAME}"
ENC_PATH="${LOCAL_PATH}.enc"

mkdir -p "${LOCAL_DIR}"

# Normalize asyncpg URL to libpq form for pg_dump
PG_URL="$(echo "${DATABASE_URL}" | sed -E 's#postgresql\+asyncpg://#postgresql://#')"

log "starting pg_dump → ${LOCAL_PATH}"
if ! pg_dump --format=custom --no-owner --no-privileges --file="${LOCAL_PATH}" "${PG_URL}"; then
  die "pg_dump failed" 2
fi

SIZE_BYTES="$(stat -c%s "${LOCAL_PATH}" 2>/dev/null || stat -f%z "${LOCAL_PATH}")"
log "pg_dump ok size=${SIZE_BYTES}"

# Encrypt if a key is provided
if [[ -n "${BACKUP_ENCRYPTION_KEY:-}" ]]; then
  log "encrypting → ${ENC_PATH}"
  if ! openssl enc -aes-256-cbc -salt -pbkdf2 -in "${LOCAL_PATH}" -out "${ENC_PATH}" -pass "pass:${BACKUP_ENCRYPTION_KEY}"; then
    die "encryption failed" 3
  fi
  rm -f "${LOCAL_PATH}"
  ARTIFACT="${ENC_PATH}"
else
  log "BACKUP_ENCRYPTION_KEY not set — storing unencrypted (NOT recommended for production)"
  ARTIFACT="${LOCAL_PATH}"
fi

# Upload to S3 if configured
if [[ -n "${BACKUP_S3_BUCKET:-}" ]]; then
  PREFIX="${BACKUP_S3_PREFIX:-dealix/hourly}"
  S3_KEY="${PREFIX}/$(basename "${ARTIFACT}")"
  log "uploading → s3://${BACKUP_S3_BUCKET}/${S3_KEY}"
  if command -v aws >/dev/null 2>&1; then
    if ! aws s3 cp "${ARTIFACT}" "s3://${BACKUP_S3_BUCKET}/${S3_KEY}" \
         --storage-class STANDARD_IA --only-show-errors; then
      log "WARN: s3 upload failed — local copy retained at ${ARTIFACT}"
      exit 4
    fi
    log "s3 upload ok"
  else
    log "WARN: aws CLI not installed — skipping s3 upload"
  fi
fi

# Local retention: keep last N hours
log "pruning local backups older than ${RETENTION_HOURS}h in ${LOCAL_DIR}"
find "${LOCAL_DIR}" -maxdepth 1 -type f -name 'dealix-*.pgdump*' \
  -mmin "+$((RETENTION_HOURS * 60))" -print -delete || true

log "done"
