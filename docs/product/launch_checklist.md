---
title: GA Launch Checklist — 60 Gates Across Product, GTM, Trust, Ops, Legal
doc_id: W5.T29.launch-checklist
owner: HoP
status: draft
last_reviewed: 2026-05-13
audience: [internal, customer]
language: en
ar_companion: docs/product/launch_checklist.ar.md
related: [W0.T00, W1.T05, W3.T07, W4.T14, W5.T10, W5.T18, W5.T30]
kpi:
  metric: launch_gate_pass_rate
  target: 100
  window: 14d
rice:
  reach: 100
  impact: 2.5
  confidence: 0.9
  effort: 4
  score: 56
---

# GA Launch Checklist

## 1. Context

GA launch is the single highest-risk operating event of 2026. It is the moment when private trust (paid pilots, design partners, controlled cohorts) becomes public commitment, and the cost of a misstep compounds across every downstream metric — pipeline, brand, regulatory standing, employee morale. The checklist is the disciplined antidote to launch-day chaos: a comprehensive, owned, time-phased set of 60 gates spanning Product, GTM, Trust, Operations, and Legal.

This document is the operating contract between the launch room and the rest of the company for the 14 days before launch, launch day, and 7 days after. Every gate has a single named owner, a binary pass criterion, and a deadline anchored to T-minus-14 / T-7 / T-0 / T+7. Gates are not negotiable on the morning of launch; they are negotiated 14 days out and enforced thereafter.

Cross-link: `PUBLIC_LAUNCH_CHECKLIST.md` is the day-to-day execution checklist (tactical items, hour-by-hour); `COMMERCIAL_LAUNCH_MASTER_PLAN.md` is the strategic narrative and sequencing; `LAUNCH_GATES.md` captures the original launch-gate philosophy. This document is the canonical, structured 60-gate matrix that all three reference.

## 2. Audience

- **HoP (owner)** — runs the 14-day countdown, the launch-room standup, the daily gate roll-up.
- **HoP staff (PMs, Eng leads, Design lead)** — own product gates.
- **HoM (Head of Marketing) / HoS (Head of Sales)** — own GTM gates.
- **HoT (Head of Trust) / Security & Privacy leads** — own Trust gates.
- **HoO (Head of Ops) / Finance lead** — own Ops gates.
- **GC (General Counsel) / external counsel** — own Legal gates.
- **CEO** — final go/no-go authority at T-0.

## 3. Decisions / Content

### 3.1 Cadence — T-14, T-7, T-0, T+7

The checklist is time-phased; gates land in one of four buckets. Anchoring gates to a relative-day cadence (rather than absolute dates) lets us rehearse twice before the real launch.

- **T-14 (14 days before)**: long-lead gates. If a T-14 gate is Red, launch slips. No daily-standup mitigation can recover a T-14 miss.
- **T-7 (7 days before)**: medium-lead gates. Yellow at T-7 → daily review by HoP. Red at T-7 → escalation to CEO and active launch-slip conversation.
- **T-0 (launch day)**: launch-day gates. Hour-by-hour from 06:00 SA time. Daily-launch-room dry run is at T-3 and T-1.
- **T+7 (7 days after)**: post-launch gates. Stabilization, retrospective, customer-feedback intake.

### 3.2 The 60 Gates

#### Product (12 gates)

| # | Gate | Cadence | Owner |
|---|------|---------|-------|
| P1 | Production deployment frozen feature-set; release branch cut | T-14 | HoP |
| P2 | E2E tests Green on staging for full customer path (signup → first lead → outcome) | T-14 | Eng Lead |
| P3 | Load test passed at 5x projected launch-day traffic | T-14 | Eng Lead |
| P4 | Onboarding flow rehearsed end-to-end by 3 internal users | T-7 | PM |
| P5 | Decision Passport tour validated in Arabic + English | T-7 | Design Lead |
| P6 | Bilingual product copy review signed off | T-7 | Design Lead |
| P7 | Mobile responsiveness verified on top 3 KSA devices | T-7 | Design Lead |
| P8 | Feature flags audited; launch-day flags locked | T-3 | Eng Lead |
| P9 | Monitoring dashboards green; alert routing confirmed | T-3 | SRE |
| P10 | Rollback plan rehearsed (last successful rollback ≤ 30 days) | T-3 | SRE |
| P11 | Launch-day production cutover executed; smoke tests Green | T-0 | HoP |
| P12 | Post-launch error-budget burn ≤ 25% of monthly budget | T+7 | SRE |

#### GTM (15 gates)

| # | Gate | Cadence | Owner |
|---|------|---------|-------|
| G1 | Launch press release approved by CEO + GC | T-14 | HoM |
| G2 | Top-10 prospect list locked; owner per logo assigned | T-14 | HoS |
| G3 | Sales collateral (one-pager, deck, ROI calculator) finalized | T-14 | HoM |
| G4 | Demo environment seeded with bilingual demo data | T-14 | HoS |
| G5 | Bilingual website copy reviewed; legal disclaimers in place | T-7 | HoM |
| G6 | SEO content queue (10 launch-anchor posts) scheduled | T-7 | HoM |
| G7 | Paid media campaigns staged (LinkedIn, Google KSA targeting) | T-7 | HoM |
| G8 | Top-3 analyst / journalist briefings completed | T-7 | HoM |
| G9 | Partner co-announcement timing aligned | T-7 | HoS |
| G10 | Founder LinkedIn launch post drafted + reviewed | T-3 | CEO |
| G11 | Customer reference quotes captured (≥ 3) | T-3 | HoS |
| G12 | Launch event (virtual or in-person) logistics confirmed | T-3 | HoM |
| G13 | Press release dispatched at agreed embargo | T-0 | HoM |
| G14 | Inbound lead capture verified end-to-end | T-0 | HoS |
| G15 | Week-1 pipeline review and re-targeting | T+7 | HoS |

#### Trust (12 gates)

| # | Gate | Cadence | Owner |
|---|------|---------|-------|
| T1 | PDPL compliance attestation signed by GC + HoT | T-14 | HoT |
| T2 | Data residency in-region verified for all production data | T-14 | HoT |
| T3 | SOC 2 Type I report (if applicable) or interim trust pack ready | T-14 | HoT |
| T4 | DPA template finalized and customer-ready | T-14 | GC |
| T5 | Penetration test report received; criticals remediated | T-7 | HoT |
| T6 | Trust center page live (security, privacy, compliance) | T-7 | HoT |
| T7 | Sub-processor list published | T-7 | HoT |
| T8 | Incident response runbook rehearsed in last 30 days | T-7 | HoT |
| T9 | Data subject request (DSR) intake flow tested | T-3 | HoT |
| T10 | Breach notification template approved | T-3 | GC |
| T11 | Trust pack referenced in launch press materials | T-0 | HoM |
| T12 | Week-1 trust inbox triaged; no open criticals | T+7 | HoT |

#### Ops (11 gates)

| # | Gate | Cadence | Owner |
|---|------|---------|-------|
| O1 | On-call rotation published for launch week + 2 weeks after | T-14 | HoO |
| O2 | Customer support routing (Tier 1 / Tier 2 / Eng) tested | T-14 | HoO |
| O3 | Billing / Moyasar live cutover completed and reconciled | T-14 | Finance |
| O4 | ZATCA e-invoicing in production with first test invoice issued | T-14 | Finance |
| O5 | Launch-room operating cadence published (standups, escalation) | T-7 | HoO |
| O6 | Customer onboarding capacity confirmed for projected volume | T-7 | HoCS |
| O7 | Internal launch-comms (Slack, all-hands brief) staged | T-7 | HoO |
| O8 | Support SLA published externally (response time commitments) | T-3 | HoO |
| O9 | Launch-day war room confirmed; attendees notified | T-3 | HoO |
| O10 | War room runs from T-2h to T+8h on launch day; hourly status | T-0 | HoO |
| O11 | Post-launch retrospective scheduled (T+5, ≥ 90 min) | T+7 | HoO |

#### Legal (10 gates)

| # | Gate | Cadence | Owner |
|---|------|---------|-------|
| L1 | Terms of Service v2 published and dated | T-14 | GC |
| L2 | Privacy Policy v2 published and dated | T-14 | GC |
| L3 | Refund policy reviewed and published | T-14 | GC |
| L4 | Cross-border transfer addendum executed for non-Saudi sub-processors | T-14 | GC |
| L5 | Saudi commercial registration current; trade-license verified | T-7 | GC |
| L6 | Trademark / brand registration filed (logo, name) | T-7 | GC |
| L7 | Customer-facing legal pack (TOS, PP, DPA) bundled and linked | T-7 | GC |
| L8 | Marketing claim review (no unsubstantiated performance claims) | T-3 | GC |
| L9 | Launch press materials legal-cleared | T-0 | GC |
| L10 | Week-1 legal inbox triaged; no open contracts blockers | T+7 | GC |

### 3.3 Daily Cadence in the Final 14 Days

- **Daily**: 17:00 launch-room standup; HoP runs; 15 minutes; per-category roll-up of gate status (Green / Yellow / Red); blockers escalated to category owner with 24-hour resolution SLA.
- **T-7**: full-pass dry-run review; CEO attends.
- **T-3**: final rehearsal of launch day (war room exercise); rollback rehearsal.
- **T-1**: go/no-go meeting; CEO + HoP + HoT + GC + HoO; final Red items resolved or launch slipped.
- **T-0**: war room from 06:00; hour-by-hour through launch hour and 8 hours after.
- **T+1, T+3, T+5, T+7**: post-launch stand-downs; T+5 retrospective.

### 3.4 Decision Rights at the Go/No-Go

- **Go**: requires all 60 gates Green OR Yellow with documented mitigations approved by the gate's owner and CEO.
- **Conditional Go (delayed launch by ≤ 7 days)**: CEO approval; HoP issues new cadence anchored to the new T-0.
- **No-Go**: CEO authority alone; communicated within 60 minutes to the launch room and within 4 hours externally if external commitments made.

No individual category owner can unilaterally veto launch — but any Red on a Trust or Legal gate at T-1 is a presumptive No-Go that requires CEO override with written rationale.

### 3.5 Anti-Patterns

- **Hidden gates** — work that wasn't on the 60-gate list surfacing at T-3. The list is exhaustive; if something is missing, add it at the next quarterly framework review, not at launch.
- **Owner ambiguity** — multiple owners on a single gate. Banned. One owner per gate.
- **Slip-driven scope-add** — using a launch slip to add scope. Banned. A slip preserves scope; new scope is a new launch.
- **Last-minute marketing claim addition** — claims appearing in press materials that haven't passed L8. Banned.

## 4. KPIs / Acceptance

| Metric | Target | Window |
|--------|--------|--------|
| Gate pass rate at T-7 | ≥ 90% Green | T-7 |
| Gate pass rate at T-1 | 100% Green or Yellow-with-mitigation | T-1 |
| Launch-day P0 incidents | 0 | T-0 to T+7 |
| Launch-day rollbacks executed | 0 (target); ≤ 1 (tolerable) | T-0 |
| Trust gates Red at any point in 14 days | 0 | T-14 to T+7 |
| Post-launch NPS at T+30 | ≥ 40 | T+30 |
| Retrospective action items closure | 100% by T+30 | T+30 |

## 5. Dependencies

- Docs: W1.T05 (ICP — informs G2 prospect list), W3.T07 (trust pack — backs T-series), W4.T14 (policy gates — back L-series), W5.T10 (CS framework — informs O6 onboarding capacity), W5.T18 (pilot framework — informs sales motion at launch), W5.T30 (executive cadence — informs daily standup model).
- Code: full release branch frozen at T-14; deploy pipeline; observability stack.
- People: HoP (owner), category owners as listed, CEO (go/no-go).

## 6. Cross-links

- Day-to-day: `PUBLIC_LAUNCH_CHECKLIST.md`
- Strategic: `COMMERCIAL_LAUNCH_MASTER_PLAN.md`
- Gate philosophy: `LAUNCH_GATES.md`
- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- ICP: `docs/go-to-market/icp_saudi.md`
- Lead engine: `docs/product/saudi_lead_engine.md`
- Pricing: `docs/pricing/pricing_packages_sa.md`
- Pilot framework: `docs/delivery/pilot_framework.md`
- CS framework: `docs/customer-success/cs_framework.md`
- Executive cadence: `docs/operations/executive_operating_cadence.md`
- Arabic companion: `docs/product/launch_checklist.ar.md`

## 7. Owner & Review Cadence

- **Owner**: HoP.
- **Review**: weekly during the final 14 days; quarterly thereafter for framework integrity.
- **Escalation**: any Red gate after T-7 → CEO same-day; any Trust or Legal Red at any time → CEO + GC same-hour.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoP | Initial checklist: 60 gates (12 Product, 15 GTM, 12 Trust, 11 Ops, 10 Legal), T-14/T-7/T-0/T+7 cadence, decision rights at go/no-go |
