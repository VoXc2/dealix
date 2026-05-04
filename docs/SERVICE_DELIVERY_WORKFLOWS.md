# Service Delivery Workflows

> Verified-or-mapped delivery flow per public bundle. Each step lists the
> exact API call (or human action) used today.

## Growth Starter (499 SAR pilot, 7 days)

| # | Step | Tool / Endpoint | Status |
| - | --- | --- | --- |
| 1 | Intake | `POST /api/v1/operator/service/start { bundle_id:"growth_starter", company_name, sector, ideal_customer, avg_deal_sar, current_channels }` | PROVEN_LIVE |
| 2 | ICP clarification | follow-up via `personal-operator/messages/draft` | PROVEN_LIVE |
| 3 | Segment selection | `POST /api/v1/business/verticals/recommend` | PROVEN_LIVE |
| 4 | Opportunity creation (×10) | `POST /api/v1/leads` + `POST /api/v1/prospect/route` | PROVEN_LOCAL E2E |
| 5 | Message drafts (×6) | `POST /api/v1/personal-operator/messages/draft` | PROVEN_LIVE |
| 6 | Risk review | `POST /api/v1/compliance/check-outreach` per draft | PROVEN_LOCAL (BLOCKER on prod until redeploy) |
| 7 | Follow-up plan (×3) | `POST /api/v1/personal-operator/followups/draft` | PROVEN_LIVE |
| 8 | Proof Pack | `POST /api/v1/customers/{id}/proof-pack` + `POST /api/v1/command-center/proof-pack` | PROVEN_LIVE / PROVEN_LOCAL |
| 9 | Upsell recommendation | `POST /api/v1/business/recommend-plan` | PROVEN_LIVE |

## Data to Revenue (1,500 SAR, 10 days)

| # | Step | Tool / Endpoint | Status |
| - | --- | --- | --- |
| 1 | List source check | intake form via `POST /api/v1/operator/service/start { bundle_id:"data_to_revenue", … }` | PROVEN_LIVE |
| 2 | Consent check | `POST /api/v1/compliance/check-outreach` per row | PROVEN_LOCAL |
| 3 | Data import | `POST /api/v1/data/import` | PROVEN_LIVE |
| 4 | Cleaning + dedupe | `POST /api/v1/data/import/{id}/dedupe` | PROVEN_LIVE |
| 5 | Enrichment | `POST /api/v1/data/import/{id}/enrich` | PROVEN_LIVE |
| 6 | Normalize | `POST /api/v1/data/import/{id}/normalize` | PROVEN_LIVE |
| 7 | Ranking + report | `GET /api/v1/data/import/{id}/report` | PROVEN_LIVE |
| 8 | Channel recommendation | `POST /api/v1/channels/policy` | PROVEN_LIVE |
| 9 | Drafts + approval | `POST /api/v1/outreach/queue` → `…/approve` | PROVEN_LIVE |
| 10 | Risk blocks | `compliance/check-outreach` enforced | PROVEN_LOCAL |
| 11 | Proof Pack | as above | PROVEN_LIVE |

## Partnership Growth (3,000-7,500 SAR, 30 days)

| # | Step | Tool / Endpoint | Status |
| - | --- | --- | --- |
| 1 | Partner type | intake | PROVEN_LIVE |
| 2 | Partner criteria | follow-up | PROVEN_LIVE |
| 3 | Partner shortlist | `POST /api/v1/partners/intake` | CODE_EXISTS_NOT_PROVEN |
| 4 | Partner scorecard | `GET /api/v1/partners/{id}/dashboard` | CODE_EXISTS_NOT_PROVEN |
| 5 | Intro script | `POST /api/v1/partners/outreach` | CODE_EXISTS_NOT_PROVEN |
| 6 | Meeting brief | `POST /api/v1/personal-operator/meetings/schedule-draft` | PROVEN_LIVE |
| 7 | Co-sell proposal | `POST /api/v1/partners/deal` | CODE_EXISTS_NOT_PROVEN |
| 8 | Proof Pack | `GET /api/v1/proof-ledger/partner/{id}/pack` | CODE_EXISTS_NOT_PROVEN |

## Executive Growth OS (2,999 SAR / month)

| # | Step | Tool / Endpoint | Status |
| - | --- | --- | --- |
| 1 | Weekly goals | intake + `personal-operator/launch-readiness` | PROVEN_LIVE |
| 2 | Daily role briefs | `GET /api/v1/role-briefs/daily?role=*` | PROVEN_LIVE for 5/8 roles, BLOCKER for sales_manager |
| 3 | Pipeline hygiene | `POST /api/v1/automation/score-tuner/run` | PROVEN_LIVE |
| 4 | Growth experiments | `GET /api/v1/self-growth/experiments` | CODE_EXISTS_NOT_PROVEN |
| 5 | Proof Pack (weekly) | `POST /api/v1/command-center/proof-pack` | PROVEN_LIVE |
| 6 | Monthly review | manual (Founder) | n/a |

## Full Growth Control Tower (custom, monthly)

Enterprise / sales-led. Qualification rules:
- Prospect must have ≥1 prior Proof Pack with grade ≥ B.
- Prospect must agree to a 60-day rollout window.
- `safe_policy_ar` documented in catalog: `support.html#contact`.

Status: PROVEN_LIVE catalog entry, BACKLOG sales motion.

## Definition of Done — common floor

- All deliverables produced.
- All risks documented in proof pack `what_was_protected`.
- Customer signs off (manual `payments/mark-paid` + onboarding task created).
- Proof Pack file path/url returned (Markdown today, HMAC-signed PDF in BACKLOG).
- Upsell recommendation explicitly attached.
