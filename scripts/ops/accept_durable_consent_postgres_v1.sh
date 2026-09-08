#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CANONICAL_REPO="${DEALIX_CANONICAL_REPO:-/opt/dealix/workspace/dealix}"
EXPECTED="${1:-${DEALIX_EXPECTED_SHA:-}}"
POSTGRES_IMAGE="${DEALIX_POSTGRES_IMAGE:-postgres:16-alpine}"

if [[ -n "${DEALIX_AUTOMATION_PYTHON:-}" ]]; then
  PY="$DEALIX_AUTOMATION_PYTHON"
elif [[ -x "$CANONICAL_REPO/.venv/bin/python" ]]; then
  PY="$CANONICAL_REPO/.venv/bin/python"
else
  PY="python3"
fi

git_safe() {
  git -c "safe.directory=$ROOT" -C "$ROOT" "$@"
}

if [[ -z "$EXPECTED" ]]; then
  echo "DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED"
  exit 2
fi

ACTUAL="$(git_safe rev-parse HEAD)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "EXPECTED_SHA=$EXPECTED"
  echo "ACTUAL_SHA=$ACTUAL"
  echo "DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_SHA_MISMATCH"
  exit 3
fi

command -v docker >/dev/null 2>&1 || {
  echo "DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_DOCKER_REQUIRED"
  exit 4
}

docker info >/dev/null 2>&1 || {
  echo "DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_DOCKER_UNAVAILABLE"
  exit 5
}

# Acceptance must never inherit material/live authority from the host.
export APP_ENV=test
export PYTHONNOUSERSITE=1
export DEALIX_EXTERNAL_SEND=0
export DEALIX_EMAIL_LIVE_SEND=0
export DEALIX_WHATSAPP_OUTBOUND=0
export DEALIX_PUBLIC_PUBLISH=0
export DEALIX_PAID_SPEND=0
export DEALIX_PAYMENT_EXECUTION=0
export DEALIX_PRODUCTION_MUTATION=0
export DEALIX_DNS_MUTATION=0
export DEALIX_DB_MUTATION=0
export DEALIX_SECRET_MUTATION=0
export DEALIX_IDENTITY_MUTATION=0
export DEALIX_AGENT_SELF_AUTHORITY=0
export DEALIX_AUTONOMY_LEVEL=4
export DEALIX_MODE=draft-only
export EXTERNAL_SEND_ENABLED=false
export EMAIL_SEND_ENABLED=false
export EMAIL_LIVE_SEND=0
export WHATSAPP_SEND_ENABLED=false
export WHATSAPP_ALLOW_LIVE_SEND=false
export WHATSAPP_OUTBOUND=0
export SMS_SEND_ENABLED=false
export OUTBOUND_MODE=draft_only
export PUBLIC_PUBLISH=0
export PAID_SPEND=0
export PAYMENT_EXECUTION=0
export PRODUCTION_MUTATION=0
export DNS_MUTATION=0
export DB_MUTATION=0
export SECRET_MUTATION=0
export IDENTITY_MUTATION=0
export VOICE_AI_ENABLED=false
export VOICE_OUTBOUND_ENABLED=false
export VOICE_RECORDING_ENABLED=false
export DEALIX_SUPPRESSION_ALLOW_REMOVE=false

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
SAFE_SUFFIX="$(printf '%s-%s' "$STAMP" "$$" | tr -cd 'A-Za-z0-9-')"
CONTAINER="dealix-consent-pg-${SAFE_SUFFIX}"
PG_USER="dealix_accept"
PG_DB="dealix_accept"
PG_PASSWORD="$(openssl rand -hex 24 2>/dev/null || "$PY" - <<'PY'
import secrets
print(secrets.token_hex(24))
PY
)"

cleanup() {
  set +e
  unset DATABASE_URL DEALIX_CONSENT_BACKEND DEALIX_SUPPRESSION_BACKEND
  unset DEALIX_ALLOW_FRESH_DB_BOOTSTRAP
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

cd "$ROOT"

# This database is disposable and isolated from Production by construction.
docker run -d --rm \
  --name "$CONTAINER" \
  -e POSTGRES_USER="$PG_USER" \
  -e POSTGRES_PASSWORD="$PG_PASSWORD" \
  -e POSTGRES_DB="$PG_DB" \
  -p 127.0.0.1::5432 \
  "$POSTGRES_IMAGE" >/dev/null

READY=0
for _ in $(seq 1 60); do
  if docker exec "$CONTAINER" pg_isready -U "$PG_USER" -d "$PG_DB" >/dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 1
done

if [[ "$READY" -ne 1 ]]; then
  echo "DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_POSTGRES_NOT_READY"
  exit 6
fi

HOST_PORT="$(docker port "$CONTAINER" 5432/tcp | tail -n 1 | awk -F: '{print $NF}')"
[[ "$HOST_PORT" =~ ^[0-9]+$ ]] || {
  echo "DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_POSTGRES_PORT"
  exit 7
}

export DATABASE_URL="postgresql+asyncpg://${PG_USER}:${PG_PASSWORD}@127.0.0.1:${HOST_PORT}/${PG_DB}"
export DEALIX_CONSENT_BACKEND=postgres
export DEALIX_SUPPRESSION_BACKEND=postgres
unset DEALIX_CONSENT_DEFAULT_TENANT || true

# Historical Dealix Alembic roots predate a formal baseline and begin with
# ALTER operations. They are not a valid fresh-database bootstrap path. Use the
# repository-owned canonical bootstrap for a genuinely empty disposable DB;
# it creates the complete current schema, proves no schema drift, and stamps
# exactly the checkout's Alembic heads. Production is never involved here.
"$PY" scripts/check_alembic_single_head.py
export DEALIX_ALLOW_FRESH_DB_BOOTSTRAP=1
"$PY" scripts/ops/bootstrap_fresh_database.py --confirm-empty-bootstrap
unset DEALIX_ALLOW_FRESH_DB_BOOTSTRAP

# Prove the exact durable behavior against the real disposable PostgreSQL.
"$PY" - <<'PY'
from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

import psycopg

from app.outbound import consent, suppression


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def must_raise_runtime_error(fn, label: str) -> None:
    try:
        fn()
    except RuntimeError:
        return
    raise AssertionError(label)


require(consent.consent_backend_kind() == "postgres", "consent_backend_not_postgres")
require(suppression.suppression_backend_kind() == "postgres", "suppression_backend_not_postgres")
require(consent.persistent_consent_ready(), "consent_backend_not_ready")
require(suppression.persistent_suppression_ready(), "suppression_backend_not_ready")

base = datetime(2026, 9, 8, 2, 30, tzinfo=UTC)
contact_a = {
    "tenant_id": "accept-tenant-a",
    "contact_id": "accept-contact-a",
    "email": "alpha.accept@example.invalid",
    "whatsapp": "+966500000001",
    "phone": "+966500000001",
}
contact_b = {
    "tenant_id": "accept-tenant-b",
    "contact_id": "accept-contact-b",
    "email": "alpha.accept@example.invalid",
    "whatsapp": "+966500000001",
    "phone": "+966500000001",
}

# Unknown state begins fail-closed.
require(not consent.has_consent("email", contact_a, "direct_marketing"), "unknown_state_not_fail_closed")

# Grant and exact replay must be idempotent.
consent.record_consent(
    "email",
    contact_a,
    source="isolated_acceptance",
    purpose="direct_marketing",
    evidence_ref="acceptance://grant-a",
    evidence_digest="grant-a",
    policy_version="acceptance-v1",
    occurred_at=base,
    event_id="accept-grant-a-v1",
)
require(consent.has_consent("email", contact_a, "direct_marketing"), "grant_not_effective")

consent.record_consent(
    "email",
    contact_a,
    source="isolated_acceptance",
    purpose="direct_marketing",
    evidence_ref="acceptance://grant-a",
    evidence_digest="grant-a",
    policy_version="acceptance-v1",
    occurred_at=base,
    event_id="accept-grant-a-v1",
)
require(consent.has_consent("email", contact_a, "direct_marketing"), "exact_replay_changed_state")

# Same event key with different authority content must be rejected.
must_raise_runtime_error(
    lambda: consent.record_consent(
        "email",
        contact_b,
        source="isolated_acceptance",
        purpose="direct_marketing",
        evidence_ref="acceptance://conflict",
        evidence_digest="conflict",
        policy_version="acceptance-v1",
        occurred_at=base,
        event_id="accept-grant-a-v1",
    ),
    "conflicting_event_key_not_rejected",
)

# Tenant, channel, and purpose isolation.
require(not consent.has_consent("email", contact_b, "direct_marketing"), "tenant_isolation_failed")
require(not consent.has_consent("whatsapp", contact_a, "direct_marketing"), "channel_isolation_failed")
require(not consent.has_consent("email", contact_a, "support"), "purpose_isolation_failed")

# Withdrawal must override the prior grant immediately.
consent.withdraw_consent(
    "email",
    contact_a,
    purpose="direct_marketing",
    source="isolated_acceptance",
    evidence_ref="acceptance://withdraw-a",
    evidence_digest="withdraw-a",
    policy_version="acceptance-v1",
    occurred_at=base + timedelta(seconds=10),
    event_id="accept-withdraw-a-v1",
)
require(not consent.has_consent("email", contact_a, "direct_marketing"), "withdrawal_not_fail_closed")

# Later explicit re-consent is allowed and auditable.
consent.record_consent(
    "email",
    contact_a,
    source="isolated_acceptance",
    purpose="direct_marketing",
    evidence_ref="acceptance://regrant-a",
    evidence_digest="regrant-a",
    policy_version="acceptance-v1",
    occurred_at=base + timedelta(seconds=20),
    event_id="accept-regrant-a-v1",
)
require(consent.has_consent("email", contact_a, "direct_marketing"), "reconsent_not_effective")

# Suppression is an independent gate and must survive consent changes.
suppression.add_suppression(contact_a["email"], channel="email", reason="isolated_acceptance")
require(suppression.is_suppressed(contact_a["email"], "email"), "suppression_not_effective")
require(consent.has_consent("email", contact_a, "direct_marketing"), "suppression_mutated_consent")

consent.record_consent(
    "email",
    contact_a,
    source="isolated_acceptance",
    purpose="direct_marketing",
    evidence_ref="acceptance://post-suppression-regrant",
    evidence_digest="post-suppression-regrant",
    policy_version="acceptance-v1",
    occurred_at=base + timedelta(seconds=30),
    event_id="accept-regrant-a-v2",
)
require(suppression.is_suppressed(contact_a["email"], "email"), "reconsent_cleared_suppression")

must_raise_runtime_error(
    lambda: suppression.remove_suppression(contact_a["email"], "email"),
    "durable_suppression_removal_was_not_authority_gated",
)

# Append-only ledger proof: exact replay did not duplicate; conflict did not insert.
dsn = os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")
with psycopg.connect(dsn, connect_timeout=3) as conn, conn.cursor() as cur:
    cur.execute(
        """
        SELECT event_key, state
          FROM outbound_consent_events
         WHERE tenant_scope = %s
           AND recipient = %s
           AND channel = 'email'
           AND purpose = 'direct_marketing'
         ORDER BY occurred_at, created_at, id
        """,
        (contact_a["tenant_id"], contact_a["email"]),
    )
    rows = cur.fetchall()

require(
    rows == [
        ("accept-grant-a-v1", "granted"),
        ("accept-withdraw-a-v1", "withdrawn"),
        ("accept-regrant-a-v1", "granted"),
        ("accept-regrant-a-v2", "granted"),
    ],
    f"append_only_ledger_unexpected:{rows!r}",
)

# Database uncertainty must fail closed for both consent and suppression.
good_url = os.environ["DATABASE_URL"]
os.environ["DATABASE_URL"] = "postgresql://invalid:invalid@127.0.0.1:1/invalid"
try:
    require(not consent.persistent_consent_ready(), "consent_uncertainty_reported_ready")
    require(not consent.has_consent("email", contact_a, "direct_marketing"), "consent_uncertainty_allowed_send")
    require(not suppression.persistent_suppression_ready(), "suppression_uncertainty_reported_ready")
    require(suppression.is_suppressed(contact_a["email"], "email"), "suppression_uncertainty_failed_open")
finally:
    os.environ["DATABASE_URL"] = good_url

print("DURABLE_CONSENT_GRANT=PASS")
print("DURABLE_CONSENT_WITHDRAW=PASS")
print("DURABLE_CONSENT_RECONSENT=PASS")
print("DURABLE_CONSENT_TENANT_ISOLATION=PASS")
print("DURABLE_CONSENT_CHANNEL_ISOLATION=PASS")
print("DURABLE_CONSENT_PURPOSE_ISOLATION=PASS")
print("DURABLE_CONSENT_REPLAY_IDEMPOTENCY=PASS")
print("DURABLE_CONSENT_CONFLICT_REJECTION=PASS")
print("DURABLE_CONSENT_DB_UNCERTAINTY_FAIL_CLOSED=PASS")
print("DURABLE_SUPPRESSION_INDEPENDENCE=PASS")
PY

if [[ -n "$(git_safe status --porcelain)" ]]; then
  echo "DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_DIRTY_WORKTREE"
  exit 8
fi

if [[ "$(git_safe rev-parse HEAD)" != "$EXPECTED" ]]; then
  echo "DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=BLOCKED_HEAD_MOVED"
  exit 9
fi

cat <<EOF
EXACT_SHA=$EXPECTED
ISOLATED_POSTGRES_IMAGE=$POSTGRES_IMAGE
ALEMBIC_SINGLE_HEAD=PASS
FRESH_DB_BOOTSTRAP=PASS
ISOLATED_POSTGRES_SCHEMA=PASS
DURABLE_CONSENT_REAL_POSTGRES_BEHAVIOR=PASS
DURABLE_SUPPRESSION_REAL_POSTGRES_BEHAVIOR=PASS
PRODUCTION_DATABASE_USED=false
PRODUCTION_MIGRATION=NOT_RUN
CONTROLLED_LIVE=NOT_ENABLED
EXTERNAL_SEND=0
PUBLIC_PUBLISH=0
PAYMENT_EXECUTION=0
PRODUCTION_MUTATION=0
L5_EXECUTED=NONE
DEALIX_DURABLE_CONSENT_POSTGRES_ACCEPTANCE=PASS
EOF
