---
title: Dealix Enterprise Procurement Pack (Saudi Arabia)
doc_id: W3.T15.enterprise-pack
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [customer, internal, partner]
language: en
ar_companion: docs/procurement/enterprise_pack.ar.md
related: [W0.T00, W3.T06, W3.T07a, W3.T07b, W3.T07c, W3.T07d, W3.T27]
kpi:
  metric: enterprise_rfp_responses_completed
  target: 6
  window: 90d
rice:
  reach: 50
  impact: 3
  confidence: 0.85
  effort: 2
  score: 64
---

# Dealix Enterprise Procurement Pack (Saudi Arabia)

## 1. Context

Saudi enterprise procurement cycles routinely require a single, coherent bundle of artefacts at the very first formal step — typically the moment a vendor is invited to respond to an RFP, RFQ, or vendor-onboarding workflow. Sending these artefacts incrementally extends cycle time by 2–4 weeks per gap. This Enterprise Procurement Pack is the canonical bundle Dealix provides on first request, designed to satisfy the procurement-and-legal expectations of the named enterprise accounts targeted by the Saudi GTM (banks, telcos, retail/F&B groups, government bodies, healthcare operators) without rework.

The pack composes existing repository artefacts (`docs/legal/ENTERPRISE_MSA_TEMPLATE.md`, `docs/DPA_DEALIX_FULL.md`, `docs/legal/DPA_TEMPLATE_AR.md`, `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`, `docs/SLO.md`, `docs/INVOICING_ZATCA_READINESS.md`, `docs/legal/COMPLIANCE_CERTIFICATIONS.md`, `docs/legal/DPO_APPOINTMENT_LETTER.md`, `docs/legal/SUB_PROCESSOR_NOTIFICATION_EMAIL.md`, `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`) into a single addressable bundle, plus the new bundle-specific artefacts described below: the pre-filled security questionnaire library, the SLA tier table, the ZATCA invoicing setup notes, the VAT line-item conventions, and the vendor-onboarding form checklist.

## 2. Audience

- Customer procurement, vendor-onboarding, and legal teams.
- Customer DPO and CISO offices for the security questionnaire portion.
- Partners that resell or co-sell Dealix and need to provide the pack to end-customer procurement.
- Internal Dealix sales engineering, account executives, and customer success.

## 3. Decisions & Content

### 3.1 Bundle Manifest

The Enterprise Pack ships as a versioned archive (release notes included) with the following manifest. Every artefact is bilingual (Arabic + English) unless otherwise marked.

1. Company information sheet (legal name, CR, VAT number, ZATCA TIN, registered address, banking details on request, key contacts).
2. Master Services Agreement template — `docs/legal/ENTERPRISE_MSA_TEMPLATE.md`.
3. Data Processing Addendum — `docs/DPA_DEALIX_FULL.md` (EN) and `docs/legal/DPA_TEMPLATE_AR.md` (AR).
4. Cross-Border Transfer Addendum — `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.
5. Service Level Agreement table — see §3.3.
6. Sub-processor list — `docs/legal/COMPLIANCE_CERTIFICATIONS.md` + `docs/legal/SUB_PROCESSOR_NOTIFICATION_EMAIL.md`.
7. Privacy Policy — `docs/PRIVACY_POLICY_v2.md`.
8. Terms of Service — `docs/TERMS_OF_SERVICE_v2.md`.
9. Refund Policy — `docs/REFUND_POLICY.md`.
10. Trust & Compliance summary — `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`, `docs/trust/security_overview.md`, `docs/trust/data_governance.md`, `docs/trust/incident_response.md`, `docs/trust/access_control.md`.
11. Pre-filled security questionnaire library — see §3.2.
12. DPO appointment evidence — `docs/legal/DPO_APPOINTMENT_LETTER.md`.
13. ZATCA-compliant invoice samples — see §3.4.
14. Insurance certificate (cyber, professional indemnity) — provided on request under NDA.
15. Pen-test attestation letter — provided under NDA.

### 3.2 Pre-Filled Security Questionnaire Library (50 Common Questions)

Dealix maintains a library of answered responses to the 50 questions that recur across SAMA, NCA, NDMO, and Big-4-issued vendor security questionnaires. The library is keyed by topic for fast assembly into customer-specific response documents. Headline coverage:

- **Organisational security (Q1–Q6):** company registration, ISMS scope, governance, security organisation chart, training programme cadence, third-party risk function.
- **Identity & access (Q7–Q13):** SSO support, MFA enforcement, RBAC model, privileged access management, password and session policies, account lifecycle, JIT internal access.
- **Data protection (Q14–Q22):** encryption at rest/in transit, key management, BYOK, retention policy, deletion procedures, PDPL alignment, sub-processor disclosure, data residency options.
- **Application security (Q23–Q29):** SDLC, code review, SAST/SCA, dependency management, container scanning, secrets management, vulnerability disclosure.
- **Operations & resilience (Q30–Q36):** monitoring, logging, incident response, RTO/RPO, backup posture, DR drills, status page.
- **Compliance & audit (Q37–Q43):** SOC 2 status, ISO 27001 status, ECC alignment, PDPL DPO, audit log retention, customer audit rights, regulator cooperation.
- **AI/LLM-specific (Q44–Q50):** training-data posture, model providers, prompt-injection mitigations, hallucination management, bias/fairness, automated decision-making notices, AI feature opt-out.

Each answer is signed off by the relevant control owner (HoLegal, CTO) and re-reviewed quarterly.

### 3.3 Service Level Agreement (SLA) Tier Table

| Tier | Monthly uptime target | Sev 1 response | Sev 1 resolution target | Service credits |
|---|---|---|---|---|
| Starter | 99.5% | 60 minutes | Best effort | 5% credit per 1% below target |
| Business | 99.9% | 30 minutes | 4 hours | 10% per 0.5% below; cap 25% MRR |
| Enterprise | 99.95% | 15 minutes | 2 hours | 15% per 0.5% below; cap 50% MRR; named TAM |
| Enterprise+ (Kingdom Residency) | 99.95% | 15 minutes | 2 hours | Enterprise terms + dedicated Saudi support shift |

Uptime is measured against the documented service definition in `docs/SLO.md`; planned maintenance windows are excluded. SLA penalty caps and exclusions are described in detail in the MSA template.

### 3.4 ZATCA Invoicing Setup

Dealix is live on ZATCA Fatoorah Phase 2. The Enterprise Pack contains:

- **VAT registration confirmation** (15-digit VAT number).
- **ZATCA TIN** and Phase 2 compliance evidence.
- **Sample compliant invoice** (Arabic-primary, QR code, UUID, hash, cryptographic stamp) — see `docs/INVOICING_ZATCA_READINESS.md`.
- **Sample compliant credit note**.
- **Buyer information requirements** the customer must provide (legal name in Arabic + English, CR, VAT number, billing address).
- **E-invoice transmission flow diagram** showing real-time clearance with ZATCA.
- **Currency**: SAR primary; multi-currency available on Enterprise plan with FX policy documented.
- **Payment terms**: net 30 default; net 60 negotiable on Enterprise plan; early-payment discount table available.

### 3.5 VAT Line-Item Conventions

- 15% Saudi VAT applied to all Kingdom-based invoices.
- Line items mapped to ZATCA-recognised goods/services categories.
- Bilingual line-item descriptions on every invoice.
- Per-tenant cost centre and PO number support to satisfy customer internal allocation rules.

### 3.6 Vendor Onboarding Form Checklist

The artefacts most frequently requested by Saudi enterprise vendor-onboarding portals (Saudi Aramco SAP Ariba, STC e-procurement, MoF Etimad, hospital group portals):

- Commercial Registration (CR) copy.
- VAT registration certificate.
- Chamber of Commerce certificate (current).
- General Organisation for Social Insurance (GOSI) certificate (current).
- Zakat & Tax certificate.
- Saudization (Nitaqat) certificate where applicable.
- Bank account verification letter.
- Bank guarantee or performance bond — issued on request; pricing/availability in §3.7.
- Authorised signatory letter and ID copy.
- Company profile (Arabic + English).
- Articles of association / partner agreement.
- Insurance certificates (cyber, professional indemnity, public liability).
- Anti-bribery and code-of-conduct attestation.
- Conflict-of-interest declaration.
- Saudi business address and lease evidence.

### 3.7 Bank Guarantees and Performance Bonds

Where a customer requires a bank guarantee or performance bond (common for government and large bank engagements), Dealix issues these on a case-by-case basis through its banking relationships. Standard parameters: bond amount tied to first-year contract value (typically 5–10%), validity period matching contract term plus 30-day tail, drawable on specified default events. The cost of issuance is typically included in Enterprise-tier contracts above a defined threshold and surfaced as a line item below it.

### 3.8 DPA Operating Notes

The Dealix DPA is offered first; customer-redline cycles are accommodated. The Dealix DPA already covers SDAIA-aligned cross-border safeguards, sub-processor notification, audit rights with reasonable-notice provisions, security-incident notification (24-hour initial, 72-hour substantive), data-subject-rights cooperation, and termination/return/destruction. Customer-paper DPAs are accepted subject to legal review.

### 3.9 MSA Operating Notes

The MSA is bilingual, governed by the laws of the Kingdom of Saudi Arabia, with dispute resolution by the Saudi Center for Commercial Arbitration (SCCA) seated in Riyadh, in Arabic with English translation. Carve-outs and standard positions on liability caps, indemnities, IP, and confidentiality are documented in the risk register (`docs/legal/enterprise_risk_register.md`).

### 3.10 Trust Portal (Planned)

A customer-accessible trust portal is planned for Q3 2026 publication, replacing the email-based pack delivery for steady-state customers. Until then, the pack is delivered through the customer's preferred secure channel (typically email with link, or upload to the customer's vendor portal) under NDA where required.

## 4. KPIs

- **Primary:** 6 enterprise RFP responses completed using the pack in 90 days.
- Mean time to deliver pack from request: ≤ 1 working day.
- Customer security questionnaire turnaround: ≤ 5 working days for standard sets.
- Zero rejections on ZATCA-compliant invoicing.

## 5. Dependencies

- Bilingual maintenance of every artefact in the pack.
- Quarterly questionnaire-library refresh.
- Banking relationship to issue performance bonds at scale.
- Trust portal infrastructure (planned).
- Up-to-date insurance certificates.

## 6. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Lead Engine: `docs/product/saudi_lead_engine.md`
- Pricing: `docs/pricing/pricing_packages_sa.md`
- Partner program: `docs/partnerships/partner_program_sa.md`
- Trust: `docs/trust/security_overview.md`, `docs/trust/data_governance.md`, `docs/trust/incident_response.md`, `docs/trust/access_control.md`
- Legal: `docs/legal/ENTERPRISE_MSA_TEMPLATE.md`, `docs/legal/DPA_TEMPLATE_AR.md`, `docs/DPA_DEALIX_FULL.md`, `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`, `docs/legal/COMPLIANCE_CERTIFICATIONS.md`, `docs/legal/DPO_APPOINTMENT_LETTER.md`, `docs/legal/SUB_PROCESSOR_NOTIFICATION_EMAIL.md`
- Compliance: `docs/INVOICING_ZATCA_READINESS.md`, `docs/SLO.md`, `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
- Risk register: `docs/legal/enterprise_risk_register.md`

## 7. Owner & Review Cadence

- Owner: Head of Legal & Compliance.
- Reviewed every 30 days during the 90-day GTM window; quarterly thereafter; immediately on any change to a Saudi regulatory baseline (PDPL Implementing Regs, NCA controls, ZATCA phase changes).

## 8. Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-13 | Initial draft (W3.T15) | HoLegal |
