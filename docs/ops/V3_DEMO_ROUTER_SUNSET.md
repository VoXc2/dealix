# v3 demo router sunset (internal)

## Current state

- [`api/routers/v3.py`](../../api/routers/v3.py) exposes `/api/v1/v3/*` with response header `X-Dealix-Deprecated: true`.
- These routes are **demo-only** and must not be used for external integrations.

## Production spine (keep and extend)

- Decision Passport: `/api/v1/decision-passport/*`
- Revenue OS catalog and gates: `/api/v1/revenue-os/*`
- Leads intake: `POST /api/v1/leads`
- Personal Operator: `/api/v1/personal-operator/*`
- Approvals: `/api/v1/approvals/*`
- Draft-first outreach: `/api/v1/gmail/*`, `/api/v1/linkedin/*` (via [`api/routers/drafts.py`](../../api/routers/drafts.py))

## Migration checklist for internal consumers

1. Replace `GET /api/v1/v3/command-center/snapshot` with Founder/Executive surfaces backed by `approval_center`, `revenue_os/catalog`, and `personal-operator/daily-brief`.
2. Replace any `GET /api/v1/v3/stack` usage with static docs plus `GET /api/v1/revenue-os/catalog`.
3. Track remaining callers via repo search for `/api/v1/v3` before deleting the router.

## Removal gate

- Zero references in `frontend/`, `api/`, and `tests/` to `/api/v1/v3/` outside `v3.py` itself.
- Smoke tests green for golden chain ([`tests/test_revenue_os_golden_chain_smoke.py`](../../tests/test_revenue_os_golden_chain_smoke.py)).
