---
title: Saudi Pricing Packages (SAR)
doc_id: W2.T03.pricing-sa
owner: CRO
status: draft
last_reviewed: 2026-05-13
audience: [customer, partner, internal]
language: en
ar_companion: docs/pricing/pricing_packages_sa.ar.md
related: [W0.T00, W1.T05, W2.T16, W2.T02, W3.T06, W3.T15]
kpi:
  metric: pricing_page_to_call_conversion
  target: 8%
  window: 60d
rice:
  reach: 250
  impact: 2
  confidence: 0.9
  effort: 1
  score: 450
---

# Saudi Pricing Packages (SAR)

## 1. Context

Existing `docs/PRICING_AND_PACKAGING_V6.md`, `docs/PRICING_STRATEGY.md`, and `docs/OFFER_LADDER_AND_PRICING.md` are USD-anchored and tier-name-anchored. Saudi enterprise buyers procure in SAR with VAT line items, expect ZATCA Phase 2 e-invoicing, and have a specific willingness to pay differentiated by tier. This document is the canonical SAR-denominated package sheet; it does not replace the strategy docs — it is the customer-facing pricing artifact.

## 2. Audience

Customer (read-only), partner (read-only), CRO/sales (canonical reference for proposals).

## 3. Decisions / Content

### 3.1 Packages

**Starter** (SME tier)
- **SAR 2,400 / month** (annual: SAR 24,000) excl. VAT
- 1 seat, 1,000 enriched leads / month, 200 ranked-A
- Lead Engine (basic source set: 10 sources)
- Decision Passport (L0–L2)
- Email + WhatsApp support, business hours
- Self-serve onboarding, knowledge base
- SLA: 99.5% availability, p95 < 500 ms

**Growth** (Mid-market)
- **SAR 9,500 / month** (annual: SAR 96,000) excl. VAT
- 5 seats, 5,000 enriched leads / month, 1,000 ranked-A
- Full Lead Engine (≥25 sources)
- Decision Passport (L0–L4)
- Bilingual sales playbook access
- Onboarding manager (90 days), QBRs quarterly
- SLA: 99.7%, p95 < 300 ms

**Enterprise** (Tier-1)
- **From SAR 35,000 / month** (annual from SAR 420,000) excl. VAT
- Unlimited seats, 50,000 enriched leads / month, 10,000 ranked-A
- Lead Engine with custom source onboarding
- Decision Passport (L0–L5) with attestation reports
- Dedicated CS, named DPO contact
- PDPL Art. 27 (health data) optional add-on
- SLA: 99.9%, p95 < 200 ms; financial penalties on breach
- Single-tenant deployment optional (Sovereign)

**Sovereign** (Govt / regulated)
- **Custom (typical SAR 80,000+ / month)** excl. VAT
- In-Kingdom data residency, dedicated VPC
- Customer-managed keys (KMS BYOK)
- SAMA-regulated bank tier add-ons
- Custom red-team / pen-test cadence
- White-glove migration & training
- SLA: 99.95%; named operations contact

### 3.2 Add-ons (all tiers)

| Add-on | Price (SAR/mo) | Notes |
|--------|----------------|-------|
| Extra seat (Growth) | 1,500 | per seat |
| Extra enriched leads | 0.40 each | per lead beyond tier cap |
| Premium source pack (LinkedIn Sales Nav) | 4,000 | per seat license |
| Custom data source connector | 12,000 / one-time | + 2,000/mo maintenance |
| ZATCA Phase 2 e-invoicing integration | 8,000 | one-time |
| Bilingual onboarding (AR-led) | 15,000 | one-time |
| Custom training program (4 sessions) | 12,000 | |
| Premium support (24/7 AR/EN) | 6,500 | Enterprise only |

### 3.3 Discounts & terms

- Annual prepay: 15% off list.
- 2-year prepay: 20% off list.
- 3-year prepay: 25% off list (Enterprise/Sovereign only).
- Multi-product: 10% off second product (when expansion catalog launches).
- Logo discount: 1 anchor logo per vertical may receive up to 30% off Y1 in exchange for case study + referral rights (CRO approval).
- ZATCA-compliant invoicing only. VAT (15%) added at invoice time.
- Procurement standard: net-30; net-60 for govt/Sovereign with CFO approval.

### 3.4 Pilot pricing (consumed by T18 pilot framework)

- 90-day paid pilot: SAR 60,000 fixed (credits 100% toward annual contract if signed within 30 days of pilot end).
- Pilot scope: 1 vertical, 5 seats, 5,000 enriched leads, success criteria defined per T18 pilot framework.

### 3.5 SAR Examples

- BFSI Tier-1 bank, 50 seats, 50K leads/mo, 3-year Enterprise: list SAR 35,000/mo × 12 × 3 = SAR 1,260,000 minus 25% prepay = **SAR 945,000 + VAT** total contract value (~SAR 1.087M with VAT).
- Mid-market retail chain, 5 seats, Growth annual: SAR 96,000 list × 0.85 (annual prepay) = **SAR 81,600 + VAT** (~SAR 93,840 with VAT).

## 4. KPIs

- Pricing-page → pricing-call conversion: 8% in 60 days.
- Discount rate (avg actual vs list): ≤ 12% (excluding anchor logos).
- Procurement cycle (signed quote → counter-signed agreement): ≤ 21 days.

## 5. Dependencies

- T16 value metrics, T2 ROI model, T15 procurement pack, T6 partner program (partner discounts), T18 pilot framework.

## 6. Cross-links

- Existing: `docs/PRICING_AND_PACKAGING_V6.md`, `docs/PRICING_STRATEGY.md`, `docs/OFFER_LADDER_AND_PRICING.md` (strategy docs; not replaced).
- Value metrics: `docs/pricing/value_metrics.md`
- ROI: `docs/sales/roi_model_saudi.md`

## 7. Owner & Review Cadence

- **Owner**: CRO.
- **Review**: quarterly with CEO and CFO; mid-year list-price refresh.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CRO | Initial SAR pricing packages, add-ons, discounts, ZATCA |

## 9. SAR Examples (extended)

See section 3.5 for inline examples. Customer-by-customer ROI references are in T2 ROI model.
