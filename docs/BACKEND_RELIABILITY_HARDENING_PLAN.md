# Backend Reliability Hardening Plan (Phase 11 Wave 5)

**Date:** 2026-05-07

The backend rules every Wave 5 router follows. Tests in
`tests/test_backend_reliability_hardening.py` enforce each rule.

---

## Rules

### 1. Status endpoint consistency
Every new router exposes `GET /<prefix>/status` returning:
- `service`: machine name
- `version`: semver
- `hard_gates`: dict[str, bool]
- (optional) feature-specific extras

### 2. Degraded response schema
When a sub-system is missing, return a degraded fragment matching
`auto_client_acquisition.integration_upgrade.schemas.DegradedSection`:
- `degraded: True`
- `severity: "low" | "medium" | "high" | "critical"`
- `reason_ar` + `reason_en`
- `next_fix_ar` + `next_fix_en`

### 3. Route registration audit
- No `/{param}` route shadows `/status` or any other static path
- New routers register in `api/main.py` AFTER existing ones (additive)
- Test `test_integration_router_registration.py` verifies via OpenAPI

### 4. Performance budgets (advisory, soft-tested)
- `/api/v1/customer-portal/{handle}` < 2s warm
- `/api/v1/executive-command-center/{handle}` < 2s warm
- `/api/v1/full-ops-radar/score` < 500ms warm
- `/api/v1/.../status` < 300ms warm
- Slow paths return degraded fragment, NEVER 500

### 5. Idempotency
- Read endpoints (GET) MUST be idempotent
- Write endpoints (POST) on payment_ops/service_sessions/approval_center
  enforce state-machine validity (transitions tested)

### 6. No broad exception leaking
- Routers MUST NOT return `__cause__`, `__traceback__`, `stacktrace`,
  or full exception messages to customer-facing endpoints
- Use `auto_client_acquisition.integration_upgrade.adapters.safe_call`
  for cross-module calls — its degraded shape never includes traceback

### 7. Safe cache for heavy dashboards
- Wave 4 ECC composer + Wave 5 LeadOps Reliability are read-only and
  recomputed every call (acceptable until first paid customer)
- Future: add `@functools.lru_cache(maxsize=128)` on the public
  `compute_*` functions when load justifies

### 8. Runtime path resolver
- Modules use `os.path.join("data", ...)` for JSONL persistence
- The `data/` directory is auto-created by every persist call
  (`os.makedirs(..., exist_ok=True)`)

### 9. CORS / API base mismatch detection
- LeadOps Reliability `/debug-trace` includes a check for `cors_api_base_mismatch`
- Future: dynamic check with frontend `window.DEALIX_API_BASE` round-trip

### 10. No 500 on missing subsystem
- Every router catches at the entrypoint (FastAPI exception handlers
  in `api/main.py`)
- Sub-system failures from `safe_call` return degraded; never raise

---

## Testing checklist

`tests/test_backend_reliability_hardening.py` asserts:
- every Wave 5 router has `/status` with `service` + `version` + `hard_gates`
- no Wave 5 endpoint returns 500 on minimal payload
- degraded fragments use the correct schema
- no stacktrace strings in any response payload
- API base + CORS check is reachable
