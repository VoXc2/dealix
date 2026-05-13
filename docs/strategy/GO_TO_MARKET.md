---
doc_id: strategy.go_to_market
title: Dealix Go-to-Market — Channels and First-25 Conversion
owner: CEO + CRO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
language: en
---

# Go-to-Market (Summary)

> Short summary of channels and first-25-customer conversion math.
> Full 12-month plan in `docs/go-to-market/saudi_gtm_12m.md`. Outbound
> message templates in `templates/outbound_messages.md`.

## Channel mix (annual target)

| Channel | Share | Owner |
|---------|-------|-------|
| Outbound (Lead Engine + SDR) | 45% | CRO + SDR |
| Partner-sourced | 25% | CRO + Partner Manager |
| Events (industry + roundtables) | 15% | Marketing |
| Inbound (content, SEO bilingual, AI-engine citations) | 15% | Marketing |

Quarter-by-quarter mix shifts (Q1 outbound-heavy → Q3 partner-balanced)
per `docs/go-to-market/saudi_gtm_12m.md` §3.1.

## Outbound — operating rules (hard)

1. **No cold WhatsApp.** Ever. Per Operating Principle hard-no list and
   `dealix/trust/forbidden_claims.py`. WhatsApp requires PDPL Art. 14
   consent or a prior business relationship.
2. **No LinkedIn automation.** Manual, approved messages only.
3. **No scraping.** Source-registered providers only (≥25 KSA sources).
4. **Every message** carries the PDPL Art. 13 footer (AR + EN, see
   `templates/outbound_messages.md`).
5. **Every send** is logged as `message.drafted → approved → sent` in
   the event store and passes the Outreach OS Approval Matrix.

## Email sequences (3 starting offers)

Each starting offer has a 3-email sequence with bilingual subject lines
and a break-up email:

| Sequence | Days | Offer | Open / Reply target |
|----------|------|-------|----------------------|
| A — Revenue Intelligence | D1 / D4 / D8 | SAR 9,500, 10 days | 35% open, 3% reply |
| B — AI Quick Win | D1 / D3 / D6 | SAR 12,000, 7 days | 30% open, 3% reply |
| C — Company Brain | D1 / D7 / D13 | SAR 20,000, 21 days | 25% open, 2% reply |

A/B test variants per `docs/experiments/ab_framework.md` (W4.T26). Full
copy in `templates/outbound_messages.md`.

## First-25-customer conversion model (Weeks 3–12)

| Segment | Volume | Channel | Conversion | Demos |
|---------|--------|---------|------------|-------|
| B2B services (Riyadh/Jeddah) | 200 | Lead Engine outbound | 8% | 16 |
| Clinics (SFDA-licensed) | 60 | Outbound + chamber lists | 10% | 6 |
| Logistics (CR-active ≥ 3y, 30–200 emp) | 60 | Outbound + Maroof | 8% | 5 |
| Inbound (content + 2 partner refs) | n/a | SEO + partner | n/a | 10 |
| **Total demos** | | | | **~37** |
| Demos → qualified opps | | | 50% | 18 |
| Qualified → close | | | 40% | **7 closes** |

Plan target: 7 closes in 90 days · floor: 5 closes. Each close = one
of the three starting offers (no bespoke in conversation 1).

## Inbound

- **Landing site**: 5-pillar service pages + 3 offer pages (per the
  90-day plan).
- **Service Activation Console** (`/status.html`): bilingual,
  structured, honest readiness JSON — designed for AI-engine citation
  (ChatGPT, Perplexity, Gemini). Cited within 1–12 weeks per the 2026
  research in `docs/STRATEGIC_MASTER_PLAN_2026.md` Part I.
- **Bilingual content**: 6 published pieces by end of Q1; 24 by Q4.
  Khaliji Arabic register, not translated MSA.
- **AR-first GEO content**: vertical landing pages, FAQ pages,
  case-study pages — all structured for AI-engine retrieval.

## Events

- Q1: 1 industry conference (LEAP or Money 20/20 Riyadh) + 2 vertical
  roundtables.
- Q2: 2 vertical roundtables + Sales Knowledge Day (own event).
- Q3: First customer summit (15–25 Saudi customers in person, Riyadh).
- Q4: Second customer summit + 1 vertical sponsorship.

## Sales motion — the 5 rules (binding)

1. **Map to one of three starting offers in 30 minutes.** Never start
   with "what do you need?".
2. **SOW signed from 1 of 3 fixed templates within 7 days.**
3. **No bespoke pricing in conversation 1.**
4. **Quality Score ≥ 80** before any handoff or upsell conversation.
5. **Day-30 post-close**: retainer / next-sprint conversation, every
   customer, no exceptions.

## First-90-day pipeline target

- 200 ICP-qualified accounts in CRM by Day 60.
- 37 demos booked, 18 qualified opps, **7 closes**.
- SAR 1.5M pipeline by end of Q1; SAR 1.5M closed.
- 2 retainers signed by end of Phase 3.

## Cross-links

- 12-month GTM plan (W2.T04): `docs/go-to-market/saudi_gtm_12m.md`
- Outbound message templates: `templates/outbound_messages.md`
- ICP: `docs/go-to-market/icp_saudi.md`
- Pricing: `docs/pricing/pricing_packages_sa.md`
- Partner program: `docs/strategy/PARTNERSHIPS.md`
- 90-day plan: `docs/strategy/90_DAY_PLAN.md`
- A/B framework: `docs/experiments/ab_framework.md`
- Existing GTM: `docs/GTM_PLAYBOOK.md`, `docs/V6_GTM_EXECUTION_PLAN.md`
