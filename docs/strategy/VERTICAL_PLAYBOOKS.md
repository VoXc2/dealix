---
doc_id: strategy.vertical_playbooks
title: Dealix Vertical Playbooks — Pain / Offer / KPI / Risk
owner: CRO
status: approved
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
---

# Vertical Playbooks

> Six priority sectors. Each card lists pain, best offers, KPIs to move,
> and material risks. Long-form BFSI / Retail / Healthcare positioning
> in `docs/go-to-market/saudi_vertical_positioning.md`. Existing legacy
> sector pages in `docs/SECTOR_PLAYBOOKS.md`.

## 1. B2B Services (consulting, agencies, IT services, professional services)

- **Buyer**: Managing Partner, Head of Sales, CEO.
- **Pain**: lumpy pipeline; bilingual proposals burn 4–8 hrs / proposal;
  account research is manual; no audit trail for outreach.
- **Best offers**: Revenue Intelligence Sprint (SAR 9,500, 10 days) →
  Monthly RevOps Retainer; AI Quick Win (proposal generator, weekly CEO
  report); Sales Knowledge Assistant (proposal snippets, objection
  handling).
- **KPIs to move**: BDR throughput +4× per rep; proposal cycle 4 hrs →
  30 min; pipeline coverage 3.0×; cost-per-qualified-account −30%.
- **Risks**: founder bypasses ICP; team treats the engine as a contact
  list (anti-pattern). Mitigation: ICP gate in Sprint scope.

## 2. Clinics (SFDA-licensed, single and multi-branch)

- **Buyer**: Clinic Director, Marketing Head, CFO.
- **Pain**: patient acquisition cost climbing; follow-up missed (rebook
  rate low); insurance pre-auth manual; bilingual SMS / WhatsApp at
  scale; PDPL Class A health data sensitivity.
- **Best offers**: AI Support Desk Sprint (SAR 12K–30K, 14 days,
  suggested-reply for WhatsApp/Inbox) → Customer Support AI Retainer
  (5K–20K / mo); AI Quick Win for missed-rebook recovery flow; Customer
  Feedback Intelligence (NPS + branch comparison).
- **KPIs to move**: rebook rate +20pp; first-response time 2 hrs → 10
  min; appointment no-show −15%; insurance pre-auth cycle −40%.
- **Risks**: PDPL Art. 27 (health data) — never auto-send to patients;
  suggested-reply only; DPO sign-off on every flow. Hard gate.

## 3. Logistics (3PL, last-mile, freight, customs brokers)

- **Buyer**: COO, Head of Commercial, Head of Operations.
- **Pain**: account expansion vs new-logo; ops dashboards manual; ZATCA
  e-invoicing reconciliation; Saudi-Made / Local Content compliance
  reporting; cross-border / GCC expansion data fragmented.
- **Best offers**: Revenue Intelligence Sprint (expansion-signal seeded)
  → Executive Reporting Automation Retainer (12K–40K setup + 5K–15K /
  mo); AI Operations Automation Sprint (route exception triage, weekly
  ops report); SOP Automation (driver onboarding, customs).
- **KPIs to move**: expansion pipeline +50%; weekly ops report cycle 6
  hrs → 1 hr; exception-handling time −40%; on-time delivery reporting
  freshness < 60 min.
- **Risks**: customer data is per-shipment heavy (PII + commercial). PII
  detection gate mandatory before any model call.

## 4. Real Estate (developers, brokers, property managers)

- **Buyer**: Sales Director, Head of Marketing, CEO.
- **Pain**: lead routing across branches/projects; bilingual contracts
  and listings; NHC / PIF megaproject opportunity tracking; broker
  productivity uneven; lead-to-viewing conversion low.
- **Best offers**: Revenue Intelligence Sprint (broker territory seed) →
  Sales Pipeline Setup (8K–25K) → Monthly RevOps Retainer; Company Brain
  Sprint (listings, policies, contract templates with citation);
  Customer Feedback Intelligence (project-level NPS).
- **KPIs to move**: lead-to-viewing +25pp; SLA on lead first-touch < 15
  min; bilingual listing time-to-publish −60%; broker close rate +10pp.
- **Risks**: scraping listing portals is forbidden (Operating Principle
  hard-no list). Source-registered providers only.

## 5. Education / Training (universities, K-12 chains, training providers, edtech)

- **Buyer**: Head of Enrollment, CFO, Academic Dean.
- **Pain**: enrollment funnel leaks; instructor scheduling manual;
  Saudization-training compliance reporting; bilingual student support;
  MoE / TVTC tender response cycles.
- **Best offers**: Revenue Intelligence Sprint (enrollment funnel
  cleanup) → AI Quick Win (instructor scheduling, weekly enrollment
  dashboard); Company Brain Sprint (policy and curriculum library);
  AI Support Assistant (student admissions Q&A, suggested-reply).
- **KPIs to move**: enrollment funnel conversion +5–10pp; student-
  support response time 2 hrs → 15 min; tender response cycle 4 weeks
  → 2 weeks; instructor utilization +15%.
- **Risks**: minors data — strict PDPL Art. 27 equivalent treatment.
  No model output to or about minors without explicit DPO approval.

## 6. Multi-branch Retail (F&B chains, fashion, specialty retail, ≥10 outlets)

- **Buyer**: COO, CMO, Head of Retail Operations.
- **Pain**: branch-level reporting fragmented; loyalty data dormant;
  feedback fragmented across channels (WhatsApp, IG, Google reviews);
  franchise / wholesale acquisition slow.
- **Best offers**: Customer Feedback Intelligence (SAR 7.5K–25K, branch
  + product comparison) → Executive Reporting Automation (weekly retail
  ops report) → Monthly AI Ops Retainer; Revenue Intelligence Sprint
  for wholesale / franchise pipeline; AI Support Desk for centralized
  customer service.
- **KPIs to move**: branch-level NPS visibility 0 → 100% of outlets;
  feedback issue-to-action cycle 14 days → 3 days; wholesale pipeline
  +50%; weekly ops report cycle 8 hrs → 1 hr.
- **Risks**: loyalty data is PII-dense — Data Quality + PII detection
  gates mandatory before model calls.

## Bonus: BFSI / Retail / Healthcare (already in long-form playbook)

See `docs/go-to-market/saudi_vertical_positioning.md` for BFSI,
Retail/eCommerce, and Healthcare cards with anchor logos and 90-day
vertical success metrics. Not duplicated here.

## How sales uses these cards

1. **First meeting**: read the pain bullets out loud; ask "which one
   hurts most this quarter?" — no pitch, just resonance.
2. **Map to one starting offer**: one of three only (Revenue / Quick Win
   / Company Brain). Never bespoke in conversation 1.
3. **Quote in SAR + days**: from the canonical catalog only.
4. **Verify PDPL constraint** (e.g., health data, minors) at SOW stage.
5. **Set retainer expectation**: at sprint close, propose the matching
   retainer from this card.

## Sequencing (90-day rollout)

- **Phase 1 (Months 1–3)**: B2B Services, Clinics, Logistics — fastest
  cycles, smallest committee, most catalog-fit.
- **Phase 2 (Months 4–6)**: Real Estate, Education/Training, Multi-
  branch Retail — needs bilingual content + branch-level reporting.
- **Phase 3 (Months 7–12)**: BFSI / Healthcare deepening, GCC expansion
  via Saudi anchors.

## Cross-links

- Long-form (BFSI / Retail / Healthcare): `docs/go-to-market/saudi_vertical_positioning.md`
- AR companion: `docs/go-to-market/saudi_vertical_positioning.ar.md`
- ICP: `docs/go-to-market/icp_saudi.md`
- Legacy sector pages: `docs/SECTOR_PLAYBOOKS.md`, `docs/VERTICAL_OS_STRATEGY.md`
- Service catalog: `docs/strategy/service_portfolio_catalog.md`
- Three starting offers: `docs/strategy/three_starting_offers.md`
- Persona-value matrix: `docs/sales/persona_value_matrix.md`
- Competitive landscape: `docs/strategy/competitive_landscape_sa.md`
