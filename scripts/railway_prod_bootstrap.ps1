# Legacy Railway production bootstrap is intentionally fail-closed.
# Production DB/seed/API mutations require a separate one-shot executor
# with exact action-bound L5 approval; persistent env flags are never authority.
$ErrorActionPreference = "Stop"

Write-Error "RAILWAY_BOOTSTRAP: HOLD - legacy bootstrap material effects are disabled" -ErrorAction Continue
Write-Error "RAILWAY_BOOTSTRAP: migration, seed, and API mutation require a separate one-shot executor with exact environment, payload/revision, expiry, idempotency key, authority source, and ACTION_HASH" -ErrorAction Continue
exit 75
