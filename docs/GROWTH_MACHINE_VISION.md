# Dealix Growth Machine — Vision & Build Sequence

> رؤية ماكينة النمو — لا تبنِ منتجاً فقط، ابنِ شبكة مكائن تشتغل يومياً
> وتترك للمؤسس قرارات الموافقة والإغلاق والعلاقات والجودة.

## Context

Dealix is positioned as a **Governed Revenue & AI Operations Company** —
not a chatbot vendor or an AI agency. The internal path is
`Diagnostic → Sprint → Retainer → Playbooks → Platform`.

This document captures the founder's "Revenue Operating Machine" vision:
a network of machines, each running daily, each with the same skeleton —
`Input → Automation → Agent → Approval Gate → Output → KPI → Evidence Event`.

**The golden rule:** everything automates *up to the moment of risk*. At the
moment of risk — an external send, an invoice, a discount, a security claim,
a final diagnosis, a case study, a promised outcome — a human approval gate
takes over. This is consistent with the 11 non-negotiables already enforced
by the doctrine tests (`tests/test_no_*.py`).

This is a multi-quarter program. It is delivered **incrementally**, one
machine at a time, mapped onto the existing
`docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`. Nothing here changes the offer
ladder in `docs/OFFER_LADDER_AND_PRICING.md`.

## The 12 Machines

| # | Machine | Purpose | Status |
|---|---------|---------|--------|
| 1 | Sales Autopilot | Lead → score → offer-match → meeting brief → scope/invoice drafts (approval-gated) | Partial — `sales_os`, `leads`, `outreach` routers exist |
| 2 | Customer Support Autopilot | Source-bound ticket answering, risk scoring, escalation, knowledge-gap capture | Partial — `support_os`, `knowledge_v10` routers exist |
| 3 | Content Factory | Market signal → angles → posts/video/carousel/newsletter, policy-checked | Planned |
| 4 | Media / Authority Machine | Category creation: LinkedIn, X, newsletter, webinars, PR, founder voice | Planned |
| 5 | Customer Referral Machine | Existing paying tenant refers a prospect for non-cash subscription credit | **Built** — `referral_program` router + `referral_store` |
| 6 | Affiliate / Partner Commission Machine | External partners earn **cash** commission, gated on `invoice_paid`, 30-day clawback | **Built — this branch** (see below) |
| 7 | Webinar Machine | Monthly governed-revenue workshops → diagnostic CTA | Planned |
| 8 | Newsletter Machine | Weekly "Governed Growth Notes" with segmented sequences | Planned |
| 9 | SEO Machine | Governance/RevOps keyword pages, templates, glossary | Planned |
| 10 | Retargeting Machine | Re-engage proof-pack viewers, risk-score takers, webinar attendees | Planned |
| 11 | Upsell / Expansion Machine | Diagnostic → Sprint → Retainer → Data Pack progression | Partial — `expansion_engine` exists |
| 12 | Governance Machine | Claim checking, approval gates, evidence ledger, agent bounds — spans all of the above | **Built** — `governance`, `trust`, `contracts`, doctrine tests |

## Build Sequence

The founder's recommended order, mapped to the 90-day plan phases:

1. **Diagnostic funnel + Sales Autopilot** (Phase 1–2) — capture and convert
   the demand that already exists.
2. **Support KB** (Phase 2) — make every answer source-bound before volume
   grows.
3. **Affiliate / Partner Commission Machine** (Phase 2–3) — *a distribution
   engine*: external partners feed leads into the funnel that already exists.
   **Shipped first because it is the highest-leverage net-new module and is
   fully specified.**
4. **Content + Newsletter + Webinar** (Phase 3) — compounding inbound.
5. **SEO + Retargeting** (Phase 3–4) — durable, low-cost demand.
6. **Upsell / Referral loops** (Phase 4) — expand revenue per customer.
7. **Platform** — only after the machines above are proven.

## Machine 6 — Affiliate / Partner Commission Machine (shipped)

The first machine delivered from this vision. It is **distinct** from the
customer-referral program (Machine 5): that one gives existing paying tenants
*non-cash subscription credit*; this one pays *cash commission* to *external*
affiliates and partners.

**Tiers**

| Tier | Name | Commission |
|------|------|-----------|
| tier1 | Affiliate Lead | 5% of first paid Diagnostic |
| tier2 | Qualified Referral | 10% of first paid deal |
| tier3 | Strategic Partner | 15–20% of first paid deal |
| tier4 | Implementation Partner | negotiated flat handoff fee |

**Hard gates (doctrine-enforced):**
- Commission is calculated **only** after a recorded `invoice_paid` event.
- Refund within 30 days triggers a clawback.
- A payout settles **only** admin-approved commissions.
- Affiliate disclosure is required; missing disclosure blocks the commission.
- No self-referrals, no duplicate leads, no commission on unqualified leads.
- Partner-facing assets are policy-checked for guaranteed-outcome language.
- Emails are hashed, never stored raw.

**Files:**
- `auto_client_acquisition/partnership_os/affiliate_store.py` — persistence,
  scoring, commission + clawback logic (JSONL store, Postgres-ready).
- `api/routers/affiliate_program.py` — `/api/v1/affiliates` API (public
  application + admin approval/commission/payout endpoints).
- `db/migrations/versions/20260517_013_affiliate_program.py` — schema
  (raw-SQL reference: `db/migrations/013_affiliate_program.sql`).
- `frontend/src/app/[locale]/partners/apply/page.tsx` — public application.
- `frontend/src/app/[locale]/partners/dashboard/page.tsx` — partner dashboard.
- `tests/test_affiliate_persistence.py`, `tests/test_affiliate_commission.py`,
  `tests/test_affiliate_doctrine.py` — 31 tests.

## Guardrails (apply to every machine)

- No partner or marketer may make exaggerated or guaranteed-outcome claims.
- No commission on unqualified leads; no payout without approval.
- No misleading ads, no cold mass WhatsApp, no scraping.
- No data collection without consent (PDPL); no client results published
  without consent.
- Every machine records an evidence event for every state change.

## Not Yet Built

Machines 3, 4, 7, 8, 9, 10 are **planned, not implemented**. Machines 1, 2,
11 are **partially** present via existing routers and are not yet wired into
the full `Input → … → Evidence Event` skeleton. This document is a roadmap,
not a claim of delivered capability — consistent with the no-overclaim
register (`dealix/registers/no_overclaim.yaml`).
