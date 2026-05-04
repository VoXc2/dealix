# API Reality Matrix

> Sources:
> - prod `https://api.dealix.me/openapi.json` → **306 paths**
> - local `scripts/print_routes.py` → **260 paths** (this branch)

## System-by-system

| System | Endpoints | Public/Staging | Auth | R/W | Tested | Status |
| --- | --- | --- | --- | --- | --- | --- |
| **Public surface** | `GET /`, `/health`, `/healthz`, `/ready`, `/live`, `/docs`, `/openapi.json`, `/redoc` | live | open | R | smoke 22/22 | PROVEN_LIVE |
| **Operator** (deploy branch) | `POST /api/v1/operator/chat/message`, `POST /api/v1/operator/service/start` | live | open | R/W | 14-scenario battery: 10 pass, 4 fail | **PROVEN_LIVE w/ 3 SAFETY MISSES** |
| **Services Tower** (deploy branch) | `GET /api/v1/services/catalog`, `GET /api/v1/services/{bundle_id}`, `GET /api/v1/services/{bundle_id}/intake-questions` | live | open | R | 6/6 bundles return 200 | PROVEN_LIVE |
| **Prospects** | `POST /api/v1/leads`, `GET /api/v1/leads/...`, `POST /api/v1/prospect/route`, `POST /api/v1/prospect/inbound/{whatsapp,form,email,sms,linkedin,handle}` | live | open | R/W | local E2E pass | PROVEN_LIVE (read), PROVEN_LOCAL (write) |
| **Deals** | `POST /api/v1/deals`, `PATCH /api/v1/deals/{id}` | live | open | R/W | local E2E pass | PROVEN_LOCAL |
| **Payments** | `POST /api/v1/payments/manual-request`, `POST /api/v1/payments/mark-paid`, `POST /api/v1/checkout`, `POST /api/v1/webhooks/moyasar` | live | webhook signed | R/W | manual fallback verified locally; webhook 401 verified live | PROVEN_LIVE (webhook), PROVEN_LOCAL (manual flow) |
| **Proof Ledger** (deploy branch) | `GET /api/v1/proof-ledger/units`, `POST /api/v1/proof-ledger/events`, `GET /api/v1/proof-ledger/customer/{id}/pack`, `GET /api/v1/proof-ledger/partner/{id}/pack`, `GET /api/v1/proof-ledger/session/{id}/pack` | live | open | R/W | units verified live; events not exercised | PROVEN_LIVE (units), CODE_EXISTS_NOT_PROVEN (events) |
| **Proof Pack** | `GET /api/v1/business/proof-pack/demo`, `POST /api/v1/business/proof-pack/roi-summary`, `POST /api/v1/customers/{id}/proof-pack`, `POST /api/v1/command-center/proof-pack` | live | open | R/W | demo + customer proof verified | PROVEN_LIVE |
| **Role Briefs** (deploy branch) | `GET /api/v1/role-briefs/daily?role=*`, `GET /api/v1/role-briefs/roles` | live | open | R | 5/8 roles work, sales_manager has DB-schema error | **PROVEN_LIVE w/ BLOCKER on sales_manager** |
| **WhatsApp Briefs** (deploy branch) | `GET /api/v1/whatsapp/brief?role=*`, `POST /api/v1/whatsapp/brief/send-internal`, `GET/POST /api/v1/webhooks/whatsapp` | live | webhook signed | R/W | growth_manager 200; sales_manager + ceo 500 | **BLOCKER** (DB schema) |
| **Compliance** | `POST /api/v1/compliance/check-outreach`, `POST /api/v1/revenue-os/compliance/{contactability,campaign-risk,dsr}`, `GET /api/v1/revenue-os/compliance/ropa` | live | open | R/W | check-outreach **500 on prod** (AsyncSession bug — fixed on this branch); campaign-risk live OK | **BLOCKER on prod (compliance/check-outreach)** |
| **Support** (deploy branch) | `GET /api/v1/support/sla`, `POST /api/v1/support/classify`, `POST/GET /api/v1/support/tickets`, `GET /api/v1/support/tickets/{id}` | live | open | R/W | sla + classify verified | PROVEN_LIVE (sla, classify), CODE_EXISTS_NOT_PROVEN (tickets) |
| **Partners portal** (deploy branch) | `GET /api/v1/partners/me`, `GET /api/v1/partners/{id}/{customers,dashboard,mrr-trend,payouts,playbook}` | live | unauthed read here | R | not exercised | CODE_EXISTS_NOT_PROVEN |
| **Customers / CompanyBrain** | `POST /api/v1/companies/intake`, `POST /api/v1/customers/onboard`, `POST /api/v1/customers/{id}/proof-pack`, `POST /api/v1/customer-success/health/{id}` | live | open | R/W | local E2E intake + onboard + proof | PROVEN_LIVE (intake), PROVEN_LOCAL (write chain) |
| **Delivery sessions** (deploy branch) | `GET/POST /api/v1/delivery/sessions`, `GET /api/v1/delivery/sessions/{id}`, `POST /…/qa`, `POST /…/transition`, `GET /api/v1/delivery/sla-summary` | live | open | R/W | not exercised | CODE_EXISTS_NOT_PROVEN |
| **Founder ops** (deploy branch) | `GET /api/v1/founder/today`, `GET /api/v1/founder/week` | live | open | R | not exercised | CODE_EXISTS_NOT_PROVEN |
| **Daily ops cron** (deploy branch) | `POST /api/v1/daily-ops/run`, `GET /api/v1/daily-ops/{history,windows}` | live | open | R/W | not exercised | CODE_EXISTS_NOT_PROVEN |
| **Self-growth experiments** (deploy branch) | `GET /api/v1/self-growth/{today,experiments,weekly-learning}` | live | open | R | not exercised | CODE_EXISTS_NOT_PROVEN |
| **Cards / decisions** (deploy branch) | `GET /api/v1/cards/feed`, `GET /api/v1/cards/roles`, `POST /api/v1/cards/{id}/decision` | live | open | R/W | not exercised | CODE_EXISTS_NOT_PROVEN |
| **Calls** (deploy branch) | `POST /api/v1/calls/dial-live`, `POST /api/v1/calls/recommend`, `GET /api/v1/calls/{id}/script` | live | open | R/W | dial-live gate not verified here | **CODE_EXISTS_NOT_PROVEN — verify gate** |
| **Negotiation** (deploy branch) | `POST /api/v1/negotiation/{respond,classify,build-response,events}` | live | open | R/W | not exercised | CODE_EXISTS_NOT_PROVEN |
| **Observability** (deploy branch) | `GET /api/v1/observability/{costs/runs,costs/summary,quality}`, `POST /api/v1/observability/unsafe/{record,summary}` | live | open | R/W | not exercised | CODE_EXISTS_NOT_PROVEN |
| **Auth / magic-link** (deploy branch) | `POST /api/v1/auth/magic-link/{send,verify}`, `GET /api/v1/auth/me`, `POST /api/v1/auth/logout` | live | self | R/W | not exercised | CODE_EXISTS_NOT_PROVEN |
| **Safety / gates** | `WHATSAPP_ALLOW_LIVE_SEND`, `MOYASAR_WEBHOOK_SECRET`, `gmail_configured`, no LinkedIn automation route | live | env-driven | n/a | all verified blocked / signed | PROVEN_LIVE |

## Local-only routers (this branch)

This branch has the same minus operator/services/role-briefs/whatsapp_briefs/
proof_ledger/support/etc. — those are deploy-branch only. After the
AsyncSession fix lands on the deploy branch, the BLOCKER routes (above)
will turn green.

## Bottom line

- 22/22 read-side smoke green on prod.
- Real-prod blockers: `automation/status`, `compliance/check-outreach`,
  `whatsapp/brief?role=ceo|sales_manager`, `role-briefs/daily?role=sales_manager`,
  operator-chat-Saudi-Arabic-cold-WA-blocker.
- Local: 516 tests, full E2E flow.
