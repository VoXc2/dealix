---
title: Dealix Saudi Partner Program
doc_id: W3.T06.partner-program-sa
owner: CRO
status: draft
last_reviewed: 2026-05-13
audience: [partner, internal]
language: en
ar_companion: docs/partnerships/partner_program_sa.ar.md
related: [W0.T00, W1.T05, W2.T03, W2.T04, W2.T08, W2.T09, W3.T15, W3.T27]
kpi:
  metric: active_saudi_partners
  target: 8
  window: 90d
rice:
  reach: 50
  impact: 3
  confidence: 0.8
  effort: 2
  score: 60
---

# Dealix Saudi Partner Program

## 1. Context

Dealix already operates two partner artifacts in the repository — `docs/AGENCY_PARTNER_PROGRAM.md` (Arabic-first early-stage program built around proof-pack gating) and `docs/partners/PARTNER_PACKAGES.md` (English service-package sheet). Both were written for the founder-led, agency-channel phase. The 90-day Saudi GTM elevates partnerships from an opportunistic agency channel to a deliberate, multi-tier program built to accelerate enterprise pipeline coverage in Kingdom verticals (banking, telco/MNO, retail/F&B, government, healthcare) where direct sales motion is slower than a partner-led motion. This document is the canonical, customer-and-partner-facing Saudi partner program spec. It does not replace the proof-pack gating discipline; it formalises the path partners follow after Dealix has produced sufficient evidence (≥3 proof packs across at least two verticals).

The program is designed to clear five concrete blockers we have observed in Saudi enterprise deals: (1) the procurement requirement that a Saudi-registered vendor co-signs the engagement; (2) the language/local-presence requirement of MoF/MoH/MoI tenders; (3) the staffing reality that a 7-person Dealix team cannot personally cover all 22 named accounts; (4) the trust acceleration that comes from a recognised SI brand co-presenting; and (5) the implementation-arm requirement (data migration, change management, CRM connector tailoring) that customers expect a partner — not the vendor — to perform.

## 2. Audience

- **Prospective partners** (Saudi SIs, MSPs, agencies, government resellers) deciding whether to join.
- **Existing partners** referencing tier rules, commission economics, and joint-selling motion.
- **Dealix CRO and partner manager** running onboarding, conflict resolution, and quarterly reviews.
- **Dealix finance and legal** for commission accruals, ZATCA-compliant invoicing of partner payouts, and partner agreement templates.

## 3. Decisions / Content

### 3.1 Three partner tiers (global) × four Saudi-specific archetypes

| Tier | Role | Target archetype in KSA | Min. annual ARR contribution | Margin |
|------|------|--------------------------|------------------------------|--------|
| Referral | Source qualified opportunity; Dealix sells and delivers | Independent consultants, ex-CRO advisors, accountants, small marketing agencies | SAR 60k | **15% of Year-1 ARR**, one-time |
| Reseller | Front the contract, invoice the customer, Dealix delivers; partner owns commercial relationship | Saudi-registered software resellers, distributors with CR + ZATCA setup, IT product houses | SAR 250k | **25% of Year-1 ARR**, recurring at 15% Y2+ |
| SI Implementation | Reseller + paid implementation services (data migration, integrations, change management, training) | Tier-1 systems integrators, vertical SIs (banking, telco, govt), large management-consulting arms | SAR 500k | **30% margin on subscription** + 100% margin on services + 5% co-marketing fund |

The four Saudi-specific archetypes the program is sized for:

**Archetype A — Saudi Tier-1 SI** (e.g., the local arms of regional SIs, large local groups with public-sector practices). Multi-vertical reach, contracts in SAR, can stand a 6–9 month procurement cycle. Slot into **SI Implementation** tier. Joint pursuit on government and SAMA-regulated bank deals where MoF/SDAIA-recognised vendor status matters.

**Archetype B — Saudi MSP / Managed-Service Provider**. Sells "outcome subscriptions" — they wrap Dealix into a managed-pipeline-operations service, run the playbook for the customer, and bill a blended price. Slot into **Reseller** tier with a managed-service rider. KPI: 3 MSPs signed in the first 12 months, each managing ≥2 customers.

**Archetype C — Local marketing or sales-ops agency**. Generates leads, runs Dealix on behalf of mid-market customers (Growth tier), retains the customer relationship. Slot into **Reseller** tier. This is the channel `docs/AGENCY_PARTNER_PROGRAM.md` already addresses; the new program preserves the Arabic-first onboarding artefacts there.

**Archetype D — Government / public-sector reseller**. Pre-listed on Etimad or holding the relevant MoF supplier ID. Slot into **Reseller** or **SI Implementation** depending on services scope. This archetype unlocks public-tender access; the partner agreement includes a government-specific addendum referencing the Local Content (Saudi-Made) preference and Etimad invoicing.

### 3.2 Commission and economics (binding)

The commission table is anchored on **Year-1 ARR booked**, net of any waived setup fees, net of VAT. All commissions are paid against a partner-issued, ZATCA-compliant invoice (Phase 2 e-invoicing). The standard payment terms are NET-30 from customer cash receipt; Dealix does not pre-fund commissions.

| Action | Referral | Reseller | SI Implementation |
|--------|----------|----------|-------------------|
| Y1 commission on subscription | 15% one-time | 25% | 30% |
| Y2+ commission on subscription | 0% | 15% | 20% |
| Implementation services revenue | n/a | 50/50 split if Dealix delivers; 100% to partner if partner delivers | 100% to partner |
| Co-marketing fund (% of Y1 ARR) | 0% | 3% | 5% |
| Renewal protection | If partner remains active | If partner remains active and engaged in renewal | If partner has ≥1 named CSM seconded |
| Cap | none | none | none |

**Commission worked example** (Growth tier, SAR 9,500/month = SAR 114,000 Y1 ARR):

- Referral path: SAR 17,100 one-time → partner.
- Reseller path: SAR 28,500 Y1 + SAR 17,100/yr from Y2 → partner.
- SI Implementation path: SAR 34,200 Y1 + SAR 22,800/yr from Y2 + 100% of services (typical implementation services: SAR 60,000–150,000).

The example shows why we expect SI partners to invest in formal certification (Section 3.4) — the lifetime margin justifies their go-to-market spend.

### 3.3 Saudi-specific terms (non-negotiable)

1. **Saudi-registered entity**: Reseller and SI partners must have an active Commercial Registration (CR), VAT registration, and Etimad supplier ID (for government deals). Referral partners may be individuals.
2. **Local content**: partners are expected to staff Saudi nationals on customer-facing implementation roles wherever feasible, and to track and report Saudi-content ratios for any tender that requires it.
3. **Arabic-language obligation**: partners must operate in Arabic when the customer requests it. Dealix supplies bilingual collateral; partners supply bilingual delivery staffing.
4. **PDPL alignment**: partners that touch customer personal data are sub-processors and must execute the Dealix Sub-Processor Addendum and PDPL flow-down terms (referenced in `docs/legal/enterprise_risk_register.md`, item 10).
5. **ZATCA invoicing**: all partner-to-Dealix and Dealix-to-partner invoices are Phase 2 e-invoices.
6. **Conflict resolution**: deal registration is first-come-first-registered, validated within 5 business days; conflicts are resolved by the Dealix partner manager with a default split of 60/40 in favour of the first-registered partner if both materially contributed.

### 3.4 Onboarding — 4-week curriculum

Onboarding is owned by the Dealix Partner Manager (under CRO). It is identical in shape for Reseller and SI tiers; Referral partners complete only Weeks 1 and 2.

**Week 1 — Foundations.** Dealix product overview, Saudi ICP walkthrough (`docs/go-to-market/icp_saudi.md`), vertical positioning (`docs/go-to-market/saudi_vertical_positioning.md`), trust posture (`docs/trust/security_overview.md`). Output: partner team has watched 6 hours of recorded sessions and passed a 30-question knowledge check.

**Week 2 — Commercials.** Saudi pricing packages (`docs/pricing/pricing_packages_sa.md`), ROI model (`docs/sales/roi_model_saudi.md`), persona-value matrix (`docs/sales/persona_value_matrix.md`), value metrics (`docs/pricing/value_metrics.md`). Output: partner can produce a SAR-denominated, VAT-aware proposal from a discovery brief without Dealix help.

**Week 3 — Demo and discovery.** Sales playbook (`docs/SALES_PLAYBOOK.md`), Saudi Lead Engine (`docs/product/saudi_lead_engine.md`), live demo certification (partner SE delivers two end-to-end demos to Dealix coaches and is graded). Output: at least one certified partner solution engineer.

**Week 4 — Procurement and delivery.** Enterprise procurement pack (`docs/procurement/enterprise_pack.md`), PDPL and DPA training, ZATCA invoicing for partner deals, deal registration tool walkthrough. Output: partner is "deal-ready" and can register their first opportunity.

Re-certification is required every 12 months or upon a major product release (defined in `docs/product/revenue_weighted_roadmap.md`).

### 3.5 Co-selling motion

Co-selling is the operating motion for Reseller and SI tiers. The four standard plays:

1. **Joint account planning** (quarterly). Each named account in the partner's territory gets a single shared account plan in the partner portal, owned jointly by Dealix AE and partner account manager. Outcome metric: pipeline coverage ≥3× quarterly target on jointly-planned accounts.

2. **Lead exchange**. Dealix routes inbound leads in the partner's named verticals/territories to the partner under deal-registration rules. Partners route inbound leads they cannot serve to Dealix. SLA: 5 business days to claim or release.

3. **Co-presented executive briefings**. For accounts in the Trust verticals (banking, telco, govt), Dealix and partner co-present a 90-minute executive briefing. Dealix supplies the deck (bilingual); partner supplies the local relationship.

4. **Co-funded pilots**. For Enterprise-tier and Sovereign-tier deals, Dealix and SI partner co-fund a paid pilot (Dealix waives 50% of pilot fee, partner waives 50% of implementation services). Used selectively — capped at four co-funded pilots per partner per year.

### 3.6 Partner portal — minimum viable scope (90 days)

A partner portal is a 12-month commitment, but the 90-day Saudi launch requires a thin slice:

- **Deal registration**: simple web form (Notion or HubSpot Forms in the interim) capturing customer name, CR number, vertical, tier intent, opportunity size, partner team. SLA-tracked 5-day claim window. Source of truth for commissions.
- **Collateral library**: bilingual sales decks, ROI calculator, pricing PDFs, demo recordings, certification materials. Versioned; partners get notified on material changes.
- **Pricing calculator**: SAR-denominated, VAT-aware, partner margin-aware. Generates a watermarked proposal PDF.
- **Demo environment**: a shared sandbox tenant where partners can run end-to-end demos without touching production data.
- **Support channel**: dedicated `partners@dealix.sa` mailbox routed to partner manager; named-account Slack/WhatsApp group for active opportunities.
- **Commission ledger**: read-only view of registered deals, deal status, accrued and paid commissions. Reconciled monthly against ZATCA invoices.

The full multi-tenant portal (auto-provisioned tenants, signed-NDA gating, in-portal training, etc.) is a Wave 4 engineering item tracked in `docs/product/revenue_weighted_roadmap.md`.

### 3.7 Partner exclusivity, segmentation, conflict

The program is **non-exclusive by default**. We grant **segmented preference** (vertical × territory × tier) rather than exclusivity. Example: a Tier-1 SI may receive preferred status on "Banking — Riyadh — Enterprise & Sovereign tiers" without blocking another partner serving Banking — Eastern Province at the Growth tier. Exclusivity, if ever requested, requires CRO and HoLegal sign-off and a binding minimum-ARR commitment per `docs/legal/enterprise_risk_register.md` item 9.

## 4. KPIs

| Metric | Target | Window | Measurement | Owner |
|--------|--------|--------|-------------|-------|
| Active Saudi partners | **8** | 90d | Partners that have completed onboarding **and** registered ≥1 deal | Partner Manager |
| Partner-sourced pipeline coverage | 2× quota | 90d | Sum of registered, validated opportunities ÷ quarterly quota | CRO |
| Partner-sourced closed-won ARR | SAR 600k | 90d | Closed-won where deal registration is active | CRO |
| Time-to-first-registered-deal | ≤30 days from kickoff | 90d | Partner portal timestamp | Partner Manager |
| Certified partner SEs | ≥1 per Reseller/SI partner | 90d | Certification ledger | Partner Manager |
| Partner NPS | ≥40 | 90d | Quarterly survey | CRO |

## 5. Dependencies

- **Upstream**: `W0.T00` master plan; `W1.T05` Saudi ICP; `W2.T03` pricing packages; `W2.T08` persona-value matrix; `W2.T09` AR sales playbook; existing `docs/AGENCY_PARTNER_PROGRAM.md`, `docs/partners/PARTNER_PACKAGES.md`, `docs/PARTNER_LEGAL_AGREEMENT.md`.
- **Downstream**: `W3.T15` procurement pack (partner-supplied to customer); `W3.T27` legal risk register (sub-processor, exclusivity, change-of-control risks).
- **Code anchors**: `auto_client_acquisition/...` lead-routing logic when partner deal-registration is integrated; `api/routers/billing/...` for commission accruals.

## 6. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md` (`W0.T00`)
- ICP: `docs/go-to-market/icp_saudi.md` (`W1.T05`)
- Lead Engine: `docs/product/saudi_lead_engine.md` (`W1.T31`)
- Pricing: `docs/pricing/pricing_packages_sa.md` (`W2.T03`)
- ROI model: `docs/sales/roi_model_saudi.md` (`W2.T02`)
- Persona-value matrix: `docs/sales/persona_value_matrix.md` (`W2.T08`)
- Sales playbook: `docs/SALES_PLAYBOOK.md`
- Procurement pack: `docs/procurement/enterprise_pack.md` (`W3.T15`)
- Trust overview: `docs/trust/security_overview.md` (`W3.T07a`)
- Legal risk register: `docs/legal/enterprise_risk_register.md` (`W3.T27`)
- Existing partner artefacts: `docs/AGENCY_PARTNER_PROGRAM.md`, `docs/partners/PARTNER_PACKAGES.md`, `docs/PARTNER_LEGAL_AGREEMENT.md`
- AR companion: `docs/partnerships/partner_program_sa.ar.md`

## 7. Owner & Review Cadence

Owner: **CRO** (Partner Manager runs day-to-day; CRO is accountable). Review cadence: **monthly partner business review** with each active partner; **quarterly program review** with CRO, HoLegal, Finance to revisit commission economics, conflict log, and tier composition. Escalation path: Partner Manager → CRO → CEO. Legal/contract escalation: HoLegal.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | — | Initial draft (W3.T06) |
