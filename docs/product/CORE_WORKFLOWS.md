# Dealix — Core Workflows

> **Discipline before scale.** Dealix's backend exposes 100+ routers and 98
> `auto_client_acquisition` subpackages. That is generative capacity, not
> product clarity. This document names the **Top-3 customer-facing
> workflows** that we operate, sell, and measure. Anything outside this
> list is platform infrastructure, internal tooling, or strategic R&D.

The three workflows below are the *only* surface that should appear in:

- Landing-page CTAs.
- Sales decks and proposals.
- Customer onboarding plans.
- SLA-bounded support escalations.
- Quarterly business reviews.

Everything else is a means to support these three.

---

## Workflow 1 — Lead → Qualified Demo Booking

**The promise:** A Saudi business sends us a lead (form, CSV, integration);
within 4 business hours we have qualified, PDPL-scored, sector-matched,
and either booked a discovery call or filed a documented reason for not
booking.

| Step | API surface | Owner |
| --- | --- | --- |
| 1. Capture | `POST /api/v1/public/demo-request` or `POST /api/v1/leads` | customer / partner |
| 2. ICP match + enrich | `auto_client_acquisition.agents` (ICP, pain extractor) called via `/api/v1/leads/{id}/enrich` | platform |
| 3. PDPL compliance gate | `POST /api/v1/compliance/check-outreach` | platform |
| 4. Outreach plan | `POST /api/v1/automation/daily-targeting/run` | platform |
| 5. Booking | `POST /api/v1/sales/book` (Calendly handoff) | platform |
| 6. Founder review | `/api/v1/founder/leads` | founder |

**Acceptance criteria (per customer):**

- ≥ 70 % of inbound leads ICP-classified within 60 minutes.
- 0 outreach rows sent without `allowed_use` set and consent recorded.
- Founder receives a daily digest of new qualified leads by 09:00
  Asia/Riyadh.

**KPIs:**

- Lead-to-qualified rate.
- Qualified-to-booked rate.
- Time from capture to first contact (target: ≤ 4 business hours).

---

## Workflow 2 — Proposal → Signed Contract

**The promise:** Once a demo happens and the prospect signals intent, the
platform drafts a tailored proposal, tracks every revision and approval,
and surfaces the deal in finance with the right pricing tier and ZATCA-
compliant invoice template.

| Step | API surface | Owner |
| --- | --- | --- |
| 1. Draft | `POST /api/v1/drafts/proposal` (uses `agents.proposal`) | platform |
| 2. Approval gate | `POST /api/v1/approval-center/proposal/{id}` | founder |
| 3. Send | `POST /api/v1/email-send/proposal/{id}` | platform |
| 4. Track engagement | `proof_to_market` + `revenue_pipeline` updates | platform |
| 5. Close + invoice | `POST /api/v1/pricing/checkout` (Moyasar handoff) + `zatca.router` | platform |
| 6. Funnel event | `proposal_sent`, `contract_signed` (PostHog) | platform |

**Acceptance criteria:**

- Every outbound proposal carries a unique tracking ID and a documented
  approver.
- Pricing reflects the live `/api/v1/pricing/plans` snapshot — no manual
  quote drift.
- ZATCA-compliant invoice issued within 24 h of contract signature.

**KPIs:**

- Proposal-to-contract conversion.
- Average days from proposal sent to contract signed.
- % of contracts with first-attempt ZATCA validation pass.

---

## Workflow 3 — Onboarded Customer → Healthy / Renewing Customer

**The promise:** A signed customer reaches "first value" inside 14 days,
maintains a green health score, receives a structured monthly review, and
renews — or, if unhealthy, gets a documented intervention before they
churn quietly.

| Step | API surface | Owner |
| --- | --- | --- |
| 1. Trial / onboarding kickoff | `POST /api/v1/trial/start` (see [trial scaffolding](../../api/routers/customer_success.py)) | platform |
| 2. Configuration handoff | `customer_loop` + `customer_company_portal` | customer success |
| 3. Health scoring | `GET /api/v1/cs/health/{tenant_id}` | platform |
| 4. Proactive outreach | `customer_success_os` + `support_journey` | customer success |
| 5. QBR pack | `executive_pack_per_customer` → PDF/JSON | customer success |
| 6. Renewal | `revenue_pipeline.renewal` event + `pricing.checkout` | platform |

**Acceptance criteria:**

- Every customer has a non-null health score within 7 days of contract
  signature.
- Health score < 0.6 triggers an escalation issue on the founder's queue.
- Monthly summary email sent on the first business day of each month with
  data, not vibes.

**KPIs:**

- 30-/60-/90-day activation rates.
- Net Revenue Retention (NRR) on Growth and Scale tiers.
- Churn-warning lead time (days from first amber health score → cancel).

---

## What is explicitly *not* a core workflow

These are valuable, but they are infrastructure or R&D — they do not get
landing-page CTAs of their own:

- Multi-OS narrative (Revenue OS / Partnership OS / CorpDev OS / Expansion
  OS / PMI OS / Trust OS). Real, but composes inside the three workflows
  above.
- v3/v6/v7/v10/v11 versioned surfaces. Frozen; not sold.
- Internal founder tooling (`founder_*`, `executive_command_center`,
  `command_bus`). Power tools, not products.
- LinkedIn cold-open generation. Disabled by default per ToS.

---

## How we use this document

- **Sales:** never pitch a workflow not on this list. If a prospect asks,
  it's a roadmap conversation, not a deliverable.
- **Engineering:** any new router or `auto_client_acquisition` subpackage
  must map to one of these workflows or be tagged `active-internal` /
  `beta` in the inventories.
- **Customer Success:** every customer plan tracks against the KPIs in
  the workflow they signed for.
- **Founder:** if a fourth workflow appears, an existing one gets
  consolidated, frozen, or retired. We do not stack workflows; we earn
  them.
