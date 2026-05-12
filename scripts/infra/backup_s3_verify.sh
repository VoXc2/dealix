#!/usr/bin/env bash
# ─────────────────────────────────────────────────────
# backup_s3_verify.sh — pull the newest S3 backup, verify gzip
# integrity, and check that the dump's row count matches the
# metadata file produced by backup_pg.sh.
#
# Cron-friendly. Expects:
#   AWS_S3_BUCKET                — bucket name (no s3:// prefix).
#   AWS_S3_PREFIX (optional)     — default `backups/`.
#   BACKUP_TMP_DIR (optional)    — default /tmp/dealix-s3-verify.
#
# Exit codes:
#   0 — backup valid.
#   1 — gzip integrity failed.
#   2 — row-count mismatch with metadata.
#   3 — required tool / env missing.
# ─────────────────────────────────────────────────────
set -euo pipefail

BUCKET="${AWS_S3_BUCKET:-}"
PREFIX="${AWS_S3_PREFIX:-backups/}"
TMP="${BACKUP_TMP_DIR:-/tmp/dealix-s3-verify}"

step() { printf '\n\033[1;34m→ %s\033[0m\n' "$1"; }

step "1. Pre-flight"
if [[ -z "$BUCKET" ]]; then
  echo "ABORT: AWS_S3_BUCKET is unset." >&2
  exit 3
fi
if ! command -v aws >/dev/null 2>&1; then
  echo "ABORT: aws CLI not on PATH." >&2
  exit 3
fi
mkdir -p "$TMP"
cd "$TMP"

step "2. Locate newest snapshot"
LATEST=$(aws s3 ls "s3://${BUCKET}/${PREFIX}" --recursive \
  | awk '/dealix_[0-9]{8}_[0-9]{6}\.sql\.gz$/ {print $4}' \
  | sort | tail -1)
if [[ -z "$LATEST" ]]; then
  echo "ABORT: no dealix_*.sql.gz under s3://${BUCKET}/${PREFIX}" >&2
  exit 3
fi
echo "   latest: s3://${BUCKET}/${LATEST}"

step "3. Download"
aws s3 cp "s3://${BUCKET}/${LATEST}" "$TMP/snapshot.sql.gz" --quiet

step "4. Gzip integrity"
if ! gzip -t "$TMP/snapshot.sql.gz" 2>/dev/null; then
  echo "FAIL: gzip integrity check failed." >&2
  exit 1
fi
echo "   gzip ok"

step "5. Compare row counts with metadata (if present)"
META_KEY="${LATEST%.sql.gz}.metadata.json"
if aws s3 cp "s3://${BUCKET}/${META_KEY}" "$TMP/meta.json" --quiet 2>/dev/null; then
  EXPECTED=$(python -c "import json; print(json.load(open('$TMP/meta.json')).get('row_count_total',0))")
  ACTUAL=$(gunzip -c "$TMP/snapshot.sql.gz" | grep -c "^INSERT INTO" || true)
  echo "   expected: $EXPECTED"
  echo "   actual:   $ACTUAL"
  if [[ "$EXPECTED" != "0" && "$EXPECTED" != "$ACTUAL" ]]; then
    echo "FAIL: row-count mismatch." >&2
    exit 2
  fi
else
  echo "   (no metadata file; skipping row-count check)"
fi

step "Done — backup verified"
