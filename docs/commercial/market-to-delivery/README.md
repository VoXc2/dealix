# Dealix Market-to-Delivery — execution plan v1

Founder-approved direction, 2026-09-07. Source implementation is separate from deployment, customer permission, commercial approval and proven delivery. This extends the existing Dealix Company Machine; it is not a second CRM, scheduler, Approval Center, consent system, proof system, model router, or permanent agent fleet.

## Product decision

Keep **Dealix — AI Business Operating System**, the D + Forward Signal identity, and the strategic wedge **Revenue + Proof + Command**. Broaden the existing service-catalog interface rather than creating another company/product identity.

The existing `/app/service-catalog` becomes a bilingual research-and-intake workspace. The 8 service arms, 20 sectors and 100 project hypotheses are discovery coverage, **not 100 proven offers**.

Canonical path:

`Need -> Authorized Evidence -> L1 Problem Signal -> Qualification -> Diagnostic -> Discovery -> Customer-Specific Quote -> Existing Commercial Approval -> Verified Payment/Start -> Project Cell -> Delivery -> Independent Acceptance -> Customer Validation -> Proof -> Support/Expansion`

## Commercial arms

1. Automation and system integration.
2. Data, BI and document intelligence.
3. Custom software, portals and APIs.
4. Enterprise AI, knowledge and inbound voice.
5. Cloud, platform and delivery reliability.
6. Governance and security engineering.
7. Industrial and field operations.
8. Managed digital operations.

Delivery route is selected after evidence and capability review: direct build, adapt existing, integrate a third-party product, qualified partner, subcontract under an approved prime, disclosed referral, or decline/defer. A route hypothesis is not dispatch, procurement, partner qualification or commercial authority.

## Canonical owners

- `dealix-pm`: portfolio allocation, policy, risk, approvals and review.
- `dealix-sales`: authorized intake, evidence, qualification, discovery and commercial preparation.
- `dealix-delivery`: scope/start/capacity checks, project cells and acceptance.
- `dealix-engineer`: source, tests, integration, reliability and technical delivery.
- `dealix-content`: drafts derived from permissioned verified evidence.

Temporary specialists are bounded project workloads under these five owners. They do not become permanent agents or inherit broader authority.

## Implemented in this PR

### Research/catalog layer

- Canonical research catalog under the existing `auto_client_acquisition/service_catalog` package.
- 8 service arms, 20 sectors and 100 project hypotheses.
- Every hypothesis remains explicitly unverified until current evidence and capability acceptance exist.
- Explicit public DTO projection excludes buyer lists, research accounts, prices, evidence, tenant data and customer records.

### Diagnostic/commercial preparation

- Deterministic preparation adapter with strict input validation.
- Missing-data questions instead of fabricated baseline/scope/outcomes.
- Diagnostic structure, route hypothesis, quote draft, internal cost-floor calculation, negotiation alternatives and project-cell draft.
- Internal cost floor is **not** a market price or approved quote.
- Admin-protected pure preparation endpoints reuse the existing founder authentication layer; they do not persist, approve, send, charge or provision.

### Canonical durable intake bridge

`POST /api/v1/commercial-intelligence/market-to-delivery/intake`

- Reuses the existing Sales authentication and Commercial Intelligence/Postgres store.
- Tenant identity comes from the authenticated user, not browser input.
- Requires an existing active tenant-bound canonical source.
- Accepts only owned/CRM/email/client-provided/partner/manual source kinds; public-registry/open-data research cannot masquerade as a customer intake.
- Requires authorization to use submitted data for preparation, but **does not infer marketing consent**.
- Persists **only** an `L1_HYPOTHESIS` `CommercialSignalRecord`.
- Does not create relationship, consent, opportunity, quote approval, send authority or project workers.
- Exact request replay is idempotent. A changed payload under the same request identity fails closed with a conflict rather than silently creating another truth record.
- Persistence failure rolls back and fails closed.

This is durable **signal-level intake**, not end-to-end customer qualification. Opportunity creation remains owned by the existing Commercial Intelligence workflow, where evidence, objectives, relationships and current service authority are checked.

### UI

- `/app/service-catalog` is an Arabic/English research workspace.
- Search and sector filtering.
- Project-hypothesis selection with candidate acceptance measure.
- Browser-local JSON draft export only.
- No admin key in the browser, no customer POST from this workspace, no checkout and no public fixed price.

### Verification assets

- Unit tests for deterministic preparation and authority boundaries.
- HTTP tests for admin preparation authentication.
- Intake-bridge tests for tenant isolation, source policy, data authorization, idempotency/conflict behavior, no authority promotion and DB fail-closed behavior.
- Public projection drift check.
- JS syntax check.
- Playwright browser gate for catalog count/filter/search/local export/bilingual behavior/no POST.
- Exact-head source acceptance command: `scripts/commercial/accept_market_to_delivery_v1.sh`.

## What is NOT yet proven

- Current exact-head source acceptance has not been proven merely because these files exist.
- Hosted GitHub jobs that terminate with `steps=[]` and `runner_id=0` are execution-plane failures, not proof that this source passed or failed.
- The browser-local workspace is not yet a public authenticated customer-submission surface.
- An L1 intake signal is not a qualified opportunity.
- Referenced evidence is not independently verified evidence.
- Relationship and channel-purpose consent are separate authorities.
- A prepared quote is not an approved/binding quote.
- A project-cell draft does not provision workers.
- No Production deployment, current release identity, verified cash, delivery or customer proof is claimed by this PR.

## Next integration gates

| Wave | Owner | Next evidence |
| --- | --- | --- |
| Exact-head acceptance | engineer | Run repo-owned acceptance on current PR SHA from isolated worktree; Next build and browser gate where dependencies exist |
| Trust dependencies | engineer/pm | Resolve existing Production Trust, Founder Control, durable consent, Railway API parity and front-door owners without duplicating them |
| Qualification | sales | Convert only evidenced L1 signals through current Commercial Intelligence source/signal/objective/relationship/opportunity contracts |
| Full diagnostic | sales/delivery | Current evidence, baseline, workflow, measurement plan and customer validation of assumptions |
| Commercial authority | pm/sales | Reuse current Finance/Approval flows with action/amount/scope/terms fingerprint, expiry and exception boundaries |
| Delivery cells | delivery/engineer | Verified scope/start, capacity, tenant isolation, accountable human, reviewer, budget/TTL, rollback and exit |
| Release | engineer | Exact deployed identity, migrations, TLS/health, rollback and explicit material action approval |
| Proof/learning | delivery/content | Actual delivery/outcome/customer validation; independent publish permission |

## Project-cell contract

Before any large-project worker provisioning: tenant/project identity, approved scope digest, customer data authorization, verified payment/start authority, accountable human, qualified specialist when needed, independent reviewer, isolated compute/storage/database/credentials, approved region/subprocessors, model and compute spend caps, concurrency cap, expiry/stop rules, acceptance/rollback, retention and exit plan.

Workers must not share customer memory, mount unrestricted production secrets for builds, purchase infrastructure, control safety-critical equipment, or change production without separate authority.

## First 90 days — operating targets, not forecasts

Days 1–14: exact source/runtime trust plus bounded real problem interviews and three starter service packages. Days 15–30: evidence-backed diagnostics and customer-specific proposals; begin a paid bounded engagement only when capability and start/payment truth support it. Days 31–60: deliver, measure, seek customer validation and test maintenance/partner repeatability. Days 61–90: deepen one or two sectors with proven demand, margin and capacity while keeping broad research active.

Measure real interactions, qualified problems, diagnostics, discoveries, approved quotes, collected cash, contribution margin, delivery variance/rework, accepted outcomes, recurring obligations and founder minutes. Account records, quotes, invoices and synthetic fixtures are not revenue.

## Current known trust dependencies

Historical runtime evidence on 2026-09-07 identified actual Founder Control failures `telegram_groups_disabled=false` and `tool_surface_bounded=false`; do not regress to the obsolete “unexposed invariant” diagnosis. Source/runtime state must still be revalidated at the exact current heads. Existing Production Trust, Founder Control, consent, Railway and front-door owners remain authoritative; this PR does not replace them.

## Safety and deployment

This source/PR work performs no merge to main, production deploy, DNS/Production DB/secret mutation, reboot, paid spend, customer send, public publish, live voice activation, legal signature or payment execution. Any later material action must bind the exact accepted SHA/configuration, expected side effects and rollback.
