#!/usr/bin/env bash
# scripts/check_alembic_heads.sh
# Refuse deploy if Alembic has more than one head (branch split).
# Use in CI before merging, and at the top of release runbook.
set -euo pipefail

HEADS="$(alembic heads 2>/dev/null | grep -c '(head)' || true)"

if [[ "${HEADS}" -eq 0 ]]; then
  echo "::error::No alembic heads found — is alembic configured?"
  exit 2
fi

if [[ "${HEADS}" -gt 1 ]]; then
  echo "::error::Multiple alembic heads (${HEADS}) — merge branches before deploy:"
  alembic heads
  exit 1
fi

echo "✓ Single alembic head"
alembic heads
