# Dealix Observability & Audit Spec

> Goal: every revenue-impacting decision is traceable. No secrets in logs.

## Already implemented

| Surface | Source | Status |
| --- | --- | --- |
| Per-request `request_id` | `api/middleware.py` `RequestIDMiddleware` | PROVEN_LOCAL |
| Structured `request_completed` log | `core/logging` + structlog | PROVEN_LOCAL |
| Sentry hook (optional) | `dealix.observability` lazy init | PROVEN_LOCAL |
| Rate limit | `api.security.setup_rate_limit` | PROVEN_LIVE |
| Cost / quality endpoints (deploy branch) | `/api/v1/observability/costs/*`, `/quality` | CODE_EXISTS_NOT_PROVEN |
| Unsafe-action recorder (deploy branch) | `/api/v1/observability/unsafe/{record,summary}` | CODE_EXISTS_NOT_PROVEN |

## Minimum log fields per operator request

```
request_id        : str
caller_id         : str (api key id or session id)
company_id        : str | null
role              : str | null  (sales_manager / growth_manager / …)
intent            : str  (cold_or_blast_outreach_request / want_more_customers / …)
language          : "ar" | "en" | "mixed"
service_recommendation : str | null  (bundle id)
action_mode       : "suggest_only" | "draft_only" | "approval_required" | "approved_execute" | "blocked"
tool_called       : str | null
safety_result     : "ok" | "blocked"
blocked_reasons   : list[str]
approval_status   : "pending" | "approved" | "rejected" | null
proof_event_id    : str | null
error_type        : str | null
latency_ms        : int
```

## Never log

- secrets (`*_SECRET_KEY`, `*_TOKEN`, `*_KEY`)
- raw card numbers / payment details (Dealix never captures cards anyway)
- raw private message bodies for customer-facing surfaces unless explicitly required for an approval flow
- full IP addresses without redaction policy

## Audit invariants (testable)

The hot-path classifier `classify_intent` is deterministic — same input,
same output. This is verified in
`tests/test_operator_saudi_safety.py::test_blocked_response_is_deterministic`.

## BACKLOG (not blockers for first customer)

- Wire `safety_result` and `blocked_reasons` into the deploy branch's
  `/api/v1/observability/unsafe/record` so blocked attempts produce
  audit rows.
- Emit `proof_ledger.events` with the matching `request_id` to make
  every Proof Pack tamper-traceable to source events.
- Add HMAC signature on Proof Pack JSON.
- Periodic export of `unsafe/summary` to a Saudi-resident object store.
