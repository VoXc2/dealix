#!/usr/bin/env bash
# Legacy Railway production bootstrap is intentionally fail-closed.
# Production DB/seed/API mutations require a separate one-shot executor
# with exact action-bound L5 approval; persistent env flags are never authority.
set -euo pipefail

echo "RAILWAY_BOOTSTRAP: HOLD - legacy bootstrap material effects are disabled" >&2
echo "RAILWAY_BOOTSTRAP: migration, seed, and API mutation require a separate one-shot executor with exact environment, payload/revision, expiry, idempotency key, authority source, and ACTION_HASH" >&2
exit 75
