# Dealix Product OS — Architecture

> Six product systems composed over the existing API. No new tables. No
> new monolith. Each system is a *view* over deploy-branch routers plus
> the local safety + brain modules added in this PR.

## 1. Dealix Command (CEO / Founder)

| Capability | Source | Status |
| --- | --- | --- |
| Top decisions | `GET /api/v1/v3/command-center/snapshot` `today_decisions` | PROVEN_LIVE |
| Revenue risk | `GET /api/v1/role-briefs/daily?role=ceo` `risk` block | PROVEN_LIVE (ceo, growth_manager, customer_success, compliance, revops); BLOCKER for sales_manager |
| Proof summary | `POST /api/v1/customers/{id}/proof-pack`, `POST /api/v1/command-center/proof-pack` | PROVEN_LIVE |
| Next 3 moves | `POST /api/v1/command-center/next-best-action` | PROVEN_LIVE |
| Safety status | `auto_client_acquisition.safety.classify_intent` + env gates | PROVEN_LOCAL |

## 2. Dealix Sell (Sales)

| Capability | Source | Status |
| --- | --- | --- |
| Pipeline | `GET /api/v1/deals` | PROVEN_LIVE (read), PROVEN_LOCAL (write) |
| Follow-ups | `POST /api/v1/personal-operator/followups/draft` | PROVEN_LIVE |
| Objections | `GET /api/v1/objections/bank` | PROVEN_LIVE |
| Meeting prep | `POST /api/v1/personal-operator/meetings/schedule-draft` | PROVEN_LIVE |
| Close plan | `POST /api/v1/negotiation/build-response` (deploy branch) | CODE_EXISTS_NOT_PROVEN |
| Invoice request | `POST /api/v1/payments/manual-request` | PROVEN_LOCAL |

## 3. Dealix Grow (Growth)

| Capability | Source | Status |
| --- | --- | --- |
| Target segments | `GET /api/v1/business/verticals` | PROVEN_LIVE |
| Channel plan | `POST /api/v1/business/recommend-plan`, `POST /api/v1/channels/policy` | PROVEN_LIVE |
| Message experiments | `POST /api/v1/personal-operator/messages/draft` | PROVEN_LIVE |
| Campaign scorecard | `POST /api/v1/revenue-os/compliance/campaign-risk` | PROVEN_LIVE |
| Safe acquisition plan | `POST /api/v1/operator/chat/message` (deploy) + local classifier | PROVEN_LOCAL (classifier) |

## 4. Dealix Serve (CS / Support)

| Capability | Source | Status |
| --- | --- | --- |
| Onboarding | `POST /api/v1/customers/onboard` | PROVEN_LOCAL |
| Proof delays | `GET /api/v1/delivery/sla-summary` (deploy branch) | CODE_EXISTS_NOT_PROVEN |
| SLA | `GET /api/v1/support/sla` | PROVEN_LIVE |
| Support issues | `POST /api/v1/support/classify`, `POST /api/v1/support/tickets` | PROVEN_LIVE (classify) |
| Renewal risk | `POST /api/v1/customer-success/health/{id}` | PROVEN_LOCAL |
| Upgrade opportunities | `POST /api/v1/business/recommend-plan` | PROVEN_LIVE |

## 5. Dealix Partner (Agency / Channel)

| Capability | Source | Status |
| --- | --- | --- |
| Partner diagnostics | `GET /api/v1/partners/{id}/dashboard` (deploy branch) | CODE_EXISTS_NOT_PROVEN |
| Referral tracking | `POST /api/v1/partners/deal` | CODE_EXISTS_NOT_PROVEN |
| Co-branded proof | `GET /api/v1/proof-ledger/partner/{id}/pack` (deploy branch) | CODE_EXISTS_NOT_PROVEN |
| Partner scorecard | `GET /api/v1/partners/{id}/payouts` | CODE_EXISTS_NOT_PROVEN |

## 6. Dealix Proof (Trust / Audit)

| Capability | Source | Status |
| --- | --- | --- |
| RWUs | `GET /api/v1/proof-ledger/units` (deploy branch) | PROVEN_LIVE — 10 units registered |
| Proof ledger events | `POST /api/v1/proof-ledger/events`, `…/events/batch` | CODE_EXISTS_NOT_PROVEN |
| Proof packs | `…/customers/{id}/proof-pack`, `…/command-center/proof-pack`, `proof-ledger/{customer,partner,session}/.../pack` | PROVEN_LIVE / PROVEN_LOCAL |
| Risk blocked count | derived from `compliance/check-outreach` outputs | PROVEN_LOCAL |
| Financial impact | `POST /api/v1/business/proof-pack/roi-summary` | PROVEN_LIVE |

## Cross-cutting safety floor

Implemented in `auto_client_acquisition/safety/intent_classifier.py`
and verified in 5 test files (95+ asserts). Five action modes:

```
suggest_only · draft_only · approval_required · approved_execute · blocked
```

Default for unknown intent → `approval_required`. Default for cold-WA-
shaped intent (Arabic Saudi, English, mixed) → `blocked` with the
canonical 5 safe alternatives.
