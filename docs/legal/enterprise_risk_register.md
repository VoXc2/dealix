---
title: Enterprise Legal & Contractual Risk Register (Saudi B2B SaaS)
doc_id: W3.T27.enterprise-risk-register
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W0.T00, W3.T06, W3.T07a, W3.T07b, W3.T07c, W3.T07d, W3.T15]
kpi:
  metric: top12_risks_with_assigned_mitigation
  target: 12
  window: 90d
rice:
  reach: 20
  impact: 3
  confidence: 0.85
  effort: 1.5
  score: 34
---

# Enterprise Legal & Contractual Risk Register (Saudi B2B SaaS)

## 1. Context

This register documents the top 12 enterprise legal and contractual risks Dealix faces when selling, contracting, and operating B2B SaaS in the Kingdom of Saudi Arabia. It is the internal source of truth for negotiation positions and is consulted by the deal desk before MSA/DPA redlines are accepted, by the executive team during quarterly risk reviews, and by the auditors of any future SOC 2 or ISO 27001 engagement. It is deliberately EN-only because the audience is the internal Dealix legal-and-finance circle; customer-facing positions are surfaced in the Enterprise Pack and in trust documents.

Each risk is logged with: description, likelihood, impact in SAR (or descriptor where monetisation is structural rather than numeric), owner, mitigation, and the standard contractual position Dealix will hold absent a paid concession.

## 2. Audience

- Head of Legal & Compliance, CRO, CTO, CEO.
- Finance for liability-cap and indemnity modelling.
- Deal desk and sales engineering for negotiation discipline.
- External counsel for benchmarking.

## 3. Decisions & Content — Top 12 Risks

### Risk 1: PDPL Violation

- **Description:** Failure to comply with the Personal Data Protection Law (e.g., late breach notification, unlawful cross-border transfer, missing DPO, insufficient lawful basis).
- **Likelihood:** Medium.
- **Impact:** SAR 100K–5M administrative fine per Implementing Regulation; reputational damage; deal-blocking with regulated customers.
- **Owner:** HoLegal (DPO functional).
- **Mitigation:** PDPL readiness programme (`docs/PRIVACY_PDPL_READINESS.md`), DPO appointed, 24-hour customer breach SLA, DPA and CBTA executed before any production data flow, quarterly audit.
- **Standard position:** Dealix's DPA includes 24-hour initial / 72-hour substantive breach notification; cross-border transfers occur only under documented basis; sub-processor list maintained publicly under NDA.

### Risk 2: ZATCA Non-Compliance

- **Description:** Failure to issue Phase-2-compliant e-invoices, late filing, incorrect VAT line items.
- **Likelihood:** Low (Dealix is live on Phase 2).
- **Impact:** SAR 1K–50K penalties per defect; cumulative; potential customer rejection of invoices.
- **Owner:** Head of People & Ops (HoP) (finance lead).
- **Mitigation:** ZATCA integration validated in production, monthly reconciliation, customer-side buyer information validated at onboarding.
- **Standard position:** All Saudi invoices ZATCA-compliant by default; bilingual line items; customer obliged to provide accurate buyer information.

### Risk 3: Cross-Border Data Flow (Outside SDAIA-Adequate Jurisdictions)

- **Description:** A regulator or customer audit finds production customer data processed in a jurisdiction without a valid PDPL transfer basis.
- **Likelihood:** Low under current sub-processor mix; Medium if new sub-processors added without review.
- **Impact:** Regulatory fine (Risk 1 scale); contract termination; service interruption.
- **Owner:** HoLegal + CTO.
- **Mitigation:** Cross-Border Transfer Addendum, sub-processor onboarding gate, Kingdom Residency option on Enterprise plan, transfer impact assessments.
- **Standard position:** Cross-border transfers only with executed CBTA or SDAIA-adequate destination; Kingdom Residency available on Enterprise tier.

### Risk 4: IP Ownership of Customer-Trained Models / Customer Data

- **Description:** Ambiguity over whether models tuned on customer data, derived embeddings, or aggregated insights are Dealix IP, customer IP, or joint IP.
- **Likelihood:** Medium (this is the single most-frequent enterprise legal redline).
- **Impact:** Loss of model improvement loop (commercial impact, SAR 1M+ over 24 months) if Dealix concedes derived-data ownership broadly; alternatively, deal loss if Dealix insists.
- **Owner:** HoLegal + CTO.
- **Mitigation:** Customer data remains the customer's. Dealix retains rights to aggregated, anonymised, non-identifiable insights for product improvement; no training of foundation models on customer data; explicit carve-out in MSA.
- **Standard position:** Customer owns input data and outputs. Dealix owns the platform, models it provides, and aggregated anonymised statistics. No training of third-party models on customer data without explicit opt-in.

### Risk 5: Liability Caps

- **Description:** Customer demands uncapped liability or caps disproportionate to contract value.
- **Likelihood:** High (enterprise norm to push for higher caps).
- **Impact:** Existential if uncapped on a data-breach scenario; manageable at 12× annual fees.
- **Owner:** HoLegal + CEO.
- **Mitigation:** Tiered cap structure with super-caps for specific carve-outs (data breach, IP indemnity).
- **Standard position:** Direct damages capped at 12× monthly fees paid in trailing 12 months. Super-cap of 24× for data breach where Dealix is at fault. Indirect/consequential damages excluded except for confidentiality breach and gross negligence. No uncapped liability except where law requires.

### Risk 6: SLA Penalty Caps

- **Description:** Customer demands large or uncapped service credits for SLA misses; recurring service credits eroding margin.
- **Likelihood:** Medium.
- **Impact:** Monthly margin erosion up to 50% of MRR at worst-case stack.
- **Owner:** HoLegal + CRO.
- **Mitigation:** Tiered service credit table; caps at 50% MRR for Enterprise; exclusions for planned maintenance and force majeure.
- **Standard position:** Service credits as defined in `docs/SLO.md` and §3.3 of Enterprise Pack. Service credit is the sole and exclusive remedy for SLA miss except for material breach.

### Risk 7: Force Majeure

- **Description:** Disagreement over what constitutes force majeure, particularly in light of pandemic, cyber-attacks on shared infrastructure, regulatory action.
- **Likelihood:** Low frequency, High impact when triggered.
- **Impact:** Potential breach claim during unavoidable outage.
- **Owner:** HoLegal.
- **Mitigation:** Modern force majeure clause covering pandemic, cyber-attack on shared infrastructure, regulator-mandated service disruption; mutual obligations to mitigate.
- **Standard position:** Dealix standard force majeure clause with explicit inclusion of pandemic, cyber, and regulator action; termination right after 30 continuous days of force-majeure non-performance.

### Risk 8: Change of Control

- **Description:** Customer requires consent or auto-termination on acquisition of Dealix; or Dealix faces issues if customer is acquired.
- **Likelihood:** Medium (large customers ask).
- **Impact:** Acquisition friction; potential deal collapse during M&A.
- **Owner:** HoLegal + CEO.
- **Mitigation:** Negotiate notice-only rather than consent; allow assignment to acquirer of substantially-all assets.
- **Standard position:** Either party may assign on change of control with 30 days' written notice; consent not unreasonably withheld for assignment to a non-competitor. No automatic termination right.

### Risk 9: Exclusivity Demands

- **Description:** Large customers (banks, telcos) request vertical or geographic exclusivity that would foreclose other deals.
- **Likelihood:** Medium.
- **Impact:** Strategic — could foreclose entire vertical TAM.
- **Owner:** CEO + CRO + HoLegal.
- **Mitigation:** No exclusivity by default. Where commercially justified (large minimum commit, multi-year), narrow exclusivity (named competitor list, time-boxed, geography-bounded) at premium pricing.
- **Standard position:** No exclusivity. Exception: 12-month named-competitor exclusivity available at +30% pricing premium and a defined minimum committed spend.

### Risk 10: Sub-Processor Disclosure & Approval

- **Description:** Customer demands prior written consent for any sub-processor change; this is operationally unworkable at scale.
- **Likelihood:** High (PDPL-aware customers ask).
- **Impact:** Operational friction; potential breach of contract on minor sub-processor swaps.
- **Owner:** HoLegal + CTO.
- **Mitigation:** Sub-processor list maintained, notification 30 days before adding/changing; customer objection right with negotiated outcome (find alternative or terminate the affected service).
- **Standard position:** Dealix maintains a public list; 30-day prior notification; customer may object within 15 days; if no resolution, customer may terminate the affected service module with pro-rata refund.

### Risk 11: AI Hallucination Liability

- **Description:** Customer or end-user suffers loss from acting on incorrect AI output; customer attributes liability to Dealix.
- **Likelihood:** Medium (rising as AI use deepens).
- **Impact:** Variable; could be substantial for high-stakes downstream actions.
- **Owner:** HoLegal + CTO.
- **Mitigation:** Clear "AI output is decision-support, not decision-of-record" language in MSA; explainability and human-review pathways for automated decisions affecting data subjects; opt-out for AI features; warranty disclaimer on AI outputs; customer indemnity for downstream-use claims.
- **Standard position:** Dealix warrants service availability and security, not the accuracy of any AI output. Customer is responsible for downstream use; Dealix indemnifies for IP infringement of training data only; Dealix offers explainability features for in-scope automated decisions.

### Risk 12: Regulator Subpoena / Compelled Disclosure

- **Description:** SDAIA, SAMA, CST, MoH, MoI, or law-enforcement compels Dealix to disclose customer data.
- **Likelihood:** Low–Medium.
- **Impact:** Customer trust impact; potential breach of confidentiality if mishandled.
- **Owner:** HoLegal.
- **Mitigation:** Documented compelled-disclosure SOP: validate the order, narrow scope where lawful, notify customer where lawful, log every event, return to customer for any subsequent customer-led regulator engagement.
- **Standard position:** Dealix will comply only with valid legal process; will narrow scope where possible; will notify customer unless prohibited; will not provide bulk access; will not disclose decryption keys customer holds under BYOK.

### 3.13 Summary Heat-Map (qualitative)

| Risk | Likelihood | Impact | Net |
|---|---|---|---|
| 1 PDPL | M | H | High |
| 2 ZATCA | L | M | Low |
| 3 Cross-border | L–M | H | Medium |
| 4 IP / model | M | H | High |
| 5 Liability cap | H | H | High |
| 6 SLA cap | M | M | Medium |
| 7 Force majeure | L | H | Medium |
| 8 Change of control | M | M | Medium |
| 9 Exclusivity | M | H | High |
| 10 Sub-processor | H | M | Medium |
| 11 AI hallucination | M | M–H | Medium–High |
| 12 Compelled disclosure | L–M | M | Medium |

## 4. KPIs

- **Primary:** 12 of 12 risks with named owner and active mitigation by day 90.
- 0 deals signed with a deviation from standard position absent deal-desk approval.
- Quarterly register review on calendar.
- Insurance cover sized to top-3 financial-impact risks.

## 5. Dependencies

- DPO appointed and registered.
- Insurance cover (cyber, PI) at appropriate limits.
- Deal-desk SOP referencing this register.
- External counsel retained for SCCA proceedings.

## 6. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Pricing: `docs/pricing/pricing_packages_sa.md`
- Trust: `docs/trust/security_overview.md`, `docs/trust/data_governance.md`, `docs/trust/incident_response.md`, `docs/trust/access_control.md`
- Procurement: `docs/procurement/enterprise_pack.md`
- Partner program: `docs/partnerships/partner_program_sa.md`
- Legal templates: `docs/legal/ENTERPRISE_MSA_TEMPLATE.md`, `docs/DPA_DEALIX_FULL.md`, `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`, `docs/legal/DPO_APPOINTMENT_LETTER.md`, `docs/legal/COMPLIANCE_CERTIFICATIONS.md`
- Internal: `docs/PRIVACY_PDPL_READINESS.md`, `docs/PDPL_BREACH_RESPONSE_PLAN.md`, `docs/INVOICING_ZATCA_READINESS.md`

## 7. Owner & Review Cadence

- Owner: Head of Legal & Compliance.
- Reviewed every 30 days during GTM window; quarterly thereafter; immediately on any change to PDPL Implementing Regulations, NCA controls, or ZATCA phasing; immediately after any deal-desk escalation referencing this register.

## 8. Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-13 | Initial top-12 register (W3.T27) | HoLegal |
