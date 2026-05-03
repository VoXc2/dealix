# First Customer — Reality Report

> Real, repeatable demo flow run locally on this branch.
> No live external action. No production DB written.

## Demo namespace

```
demo_customer_id    = cust_<auto>
demo_email          = demo.staging@dealix-test.sa
demo_company        = Dealix Staging Demo Company
demo_phone          = +966500000000
```

## Flow run (verified 2026-05-03)

```bash
APP_ENV=test APP_SECRET_KEY=test-secret \
DATABASE_URL=sqlite+aiosqlite:////tmp/dealix_e2e.db \
WHATSAPP_ALLOW_LIVE_SEND=false MOYASAR_MODE=sandbox \
python -m uvicorn api.main:app --host 127.0.0.1 --port 8765
```

```
1. POST /api/v1/leads
   { name, email=demo.staging@dealix-test.sa, company="Dealix Staging Demo Company",
     phone, source="website", sector="saas", message }
   → lead_id = lead_2be6aaae9444  (fit tier C/B)

2. POST /api/v1/deals
   { lead_id, value_sar=499, stage="pilot_offered" }
   → deal_id = deal_14e3ed3697d5405f

3. POST /api/v1/payments/manual-request
   { deal_id, amount_sar=499 }
   → method=bank_transfer, status=payment_requested,
     follow_up_task_id=task_758de3162e87471c
     instruction: "Send invoice to customer via WhatsApp/email with bank IBAN
                   or STC Pay number. Use template in
                   docs/ops/MANUAL_PAYMENT_SOP.md."

4. POST /api/v1/payments/mark-paid
   { deal_id, reference="manual-staging-demo" }
   → customer_id = cust_e49e5bb76d3c4851
     onboarding_task_id auto-created
     celebration string returned

5. POST /api/v1/customers/{customer_id}/proof-pack
   → returns case_study_md_template + testimonial_request_ar + referral_ask_ar

6. POST /api/v1/command-center/proof-pack
   → returns grade=D (no activity yet) + activity_summary +
     pipeline_impact + benchmark_comparison

7. POST /api/v1/compliance/check-outreach
   { to_email, contact_opt_out=true, allowed_use="cold_purchased" }
   → { allowed:false, blocked_reasons:["contact_opt_out_true"] }
```

## Artifacts captured

| Artifact | Value | Source |
| --- | --- | --- |
| prospect_id | `lead_2be6aaae9444` | `leads` |
| deal_id | `deal_14e3ed3697d5405f` | `deals` |
| invoice_request | `task_758de3162e87471c` (manual fallback) | `payments/manual-request` |
| customer_id | `cust_e49e5bb76d3c4851` | `payments/mark-paid` |
| onboarding_task | auto-created | same |
| proof_pack | case_study + testimonial AR + referral AR | `customers/{id}/proof-pack` |
| activity_grade | `D` (expected — no activity yet) | `command-center/proof-pack` |
| compliance_block | `["contact_opt_out_true"]` | `compliance/check-outreach` |

## What was NOT created

- No live Moyasar charge. No checkout URL was used.
- No live WhatsApp send.
- No live email send.
- No prospect record on production DB.
- No HMAC-signed PDF — only Markdown templates.

## Verdict

The flow is **repeatable end-to-end on this branch, locally**. On the
deploy branch, every step has the same surface (with extra polish via
`operator/service/start` and `proof-ledger/customer/{id}/pack`). After
the AsyncSession fix in this branch is deployed, the same flow
should succeed against `https://api.dealix.me` using the demo namespace.

**Status:** PROVEN_LOCAL. To upgrade to PROVEN_STAGING_WRITE_SAFE on
`api.dealix.me` requires:
1. Merge `claude/dealix-staging-readiness-LJOju` → deploy branch (or apply
   the `db/session.py` patch directly).
2. Railway redeploy.
3. Re-run this flow against `BASE_URL=https://api.dealix.me` with the
   demo namespace.

## Blocker for production write-flow today

Without (1) and (2) above, `compliance/check-outreach` and any DB-touching
POST that the deploy branch routes still rely on the buggy
`async_session_factory()` — which 500s on prod today
(see `REAL_CUSTOMER_OPS_TRUTH_REPORT.md` §4).
