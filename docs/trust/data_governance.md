---
title: Dealix Data Governance (PDPL Alignment)
doc_id: W3.T07b.data-governance
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [customer, partner, regulator]
language: en
ar_companion: docs/trust/data_governance.ar.md
related: [W0.T00, W3.T07a, W3.T07c, W3.T07d, W3.T15, W3.T27]
kpi:
  metric: pdpl_dsar_sla_met_percent
  target: 100
  window: 90d
rice:
  reach: 80
  impact: 3
  confidence: 0.9
  effort: 2
  score: 108
---

# Dealix Data Governance (PDPL Alignment)

## 1. Context

This document is Dealix's customer-facing statement of how the platform handles personal data in alignment with the Kingdom of Saudi Arabia's Personal Data Protection Law (PDPL), Royal Decree M/19 of 9/2/1443 H, as amended, and its Implementing Regulations issued by SDAIA. It is the artifact that a Saudi customer's Data Protection Officer or compliance team will rely on to satisfy their own accountability obligations under PDPL Article 31, and it is the substantive technical narrative that supports the contractual commitments made in the Dealix Data Processing Addendum (`docs/DPA_DEALIX_FULL.md`, `docs/legal/DPA_TEMPLATE_AR.md`) and Cross-Border Transfer Addendum (`docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`). For internal engineering, `docs/DATA_MAP.md`, `docs/DATA_RETENTION_POLICY.md`, `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`, and `docs/PRIVACY_PDPL_READINESS.md` remain authoritative.

## 2. Audience

- Data Protection Officers and privacy counsel of Saudi enterprise customers.
- SDAIA and other regulators conducting vendor assessments.
- Internal Dealix legal, engineering, and customer-success teams.
- Partners acting as sub-processors or co-controllers under joint customer engagements.

## 3. Decisions & Content

### 3.1 Roles Under PDPL

For the vast majority of Dealix services, the customer is the **Data Controller** and Dealix is the **Data Processor**, acting strictly on the controller's documented instructions as set out in the executed DPA. For platform-level processing (account administration, billing, security telemetry, anti-abuse signals on the Dealix marketing site), Dealix is the controller for a narrowly scoped set of operational data described in the Dealix Privacy Policy (`docs/PRIVACY_POLICY_v2.md`).

### 3.2 Lawful Basis (PDPL Art. 5 & 6)

Dealix processes customer personal data only on a lawful basis selected and recorded by the customer in the DPA scope worksheet. The supported bases are: consent (Art. 6), performance of a contract with the data subject, compliance with a legal obligation binding on the controller, protection of vital interests, public interest, and legitimate interests (subject to the balancing test where applicable). Special-category data ("sensitive personal data" under PDPL Implementing Regulation Art. 3) is permitted only with the customer's explicit acknowledgement and the appropriate enhanced safeguards documented in the DPA's special-category annex.

### 3.3 Notice (PDPL Art. 13)

Dealix provides notice content (in Arabic and English) that customers may adopt or adapt into their own privacy notices. The platform also surfaces just-in-time notice elements (purpose-of-processing badges, retention-window markers) where the controller has opted into them. Customer-facing notices remain the legal responsibility of the controller; Dealix supplies the technical surfaces and the editable template.

### 3.4 Consent Management (PDPL Art. 14)

Where consent is the chosen lawful basis, Dealix records the consent event with the following minimum metadata: data subject identifier, purpose, version of notice presented, timestamp, channel, and proof-of-affirmative-action artifact (e.g., signed payload or session log reference). Withdrawal of consent is processed within the same SLA as a deletion request — see §3.7. The consent ledger is exportable to the controller on demand.

### 3.5 Cross-Border Transfer (PDPL Art. 18 & Implementing Regulation Ch. 5)

Cross-border transfers occur only under one of the legally available bases:

1. The destination country is on the SDAIA-recognised adequacy list, or
2. The controller has executed Dealix's Cross-Border Transfer Addendum incorporating SDAIA-aligned safeguards (binding contractual clauses, transfer impact assessment, encryption-in-transit and at-destination commitments), or
3. The data subject has provided explicit, informed consent specific to the transfer.

Where the customer has selected the Kingdom Residency option (Enterprise plan), no production customer data is processed or stored outside the Kingdom-eligible regions defined in the addendum. Sub-processor lists and their respective jurisdictions are kept current at `docs/legal/COMPLIANCE_CERTIFICATIONS.md` and notified per the DPA cadence.

### 3.6 Retention (PDPL Art. 21)

Personal data is retained only for as long as necessary for the purpose for which it was collected. Default retention windows are summarised below; customers may shorten or, where a defensible legal basis exists, lengthen these windows in their DPA scope worksheet.

| Data Category | Default Retention | Notes |
|---|---|---|
| Customer end-user profile data | Duration of subscription + 90 days | Then irreversible deletion or anonymisation |
| Transactional/billing records | 10 years | ZATCA invoicing & tax-record obligation |
| Authentication & session logs | 13 months | Security investigation window |
| Application audit logs (security-relevant) | 1 year hot, 7 years cold | Cold storage encrypted, access-restricted |
| Support-ticket content | Duration of subscription + 12 months | Subject to controller override |
| LLM prompt/response telemetry (operational) | 30 days, opt-in to extend for evaluation | No training on customer data — see §3.10 |
| Marketing-site analytics | 24 months | Aggregated/anonymised |
| Backups (system-level) | 35 days rolling | Outside this window only forensic snapshots |

Cross-reference: `docs/DATA_RETENTION_POLICY.md`.

### 3.7 Data Subject Rights (PDPL Art. 4)

Dealix supports the controller in responding to data-subject requests covering: right to be informed, right of access, right to rectification, right to erasure, right to object, right to data portability, and the rights related to automated decision-making. Operational SLAs against the controller's DPA commitment are: acknowledgement within 2 working days, substantive response within 25 calendar days (within the 30-day statutory window, leaving the controller a safety margin). The SOP is at `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`; customer-ready templates are at `docs/legal/DSAR_RESPONSE_TEMPLATES.md`.

### 3.8 Data Residency — Kingdom Option

The Kingdom Residency option pins all primary storage, replicas, application compute, queue/streaming infrastructure, search indexes, and backup objects to a Kingdom-eligible region. Disaster-recovery copies are also held within the Kingdom-eligible region set; no live or DR data leaves the Kingdom under this option. A small set of platform metadata strictly necessary for operating the Dealix control plane (e.g., feature flag configurations, anonymised performance metrics) may transit outside the Kingdom under the safeguards of §3.5; this set is enumerated in the addendum.

### 3.9 Data Categories Processed

The data categories Dealix processes are enumerated in `docs/DATA_MAP.md`. At a summary level, they include: customer end-user identifiers (name, work email, phone), customer-uploaded content (CRM exports, lead lists, transcripts), authentication artefacts, billing/payment metadata (no PAN; payment data is tokenised by Moyasar/Stripe per region), and operational telemetry. Sensitive personal data is processed only where the customer's DPA scope worksheet explicitly enables it.

### 3.10 AI and Machine Learning Governance

Customer data is **not** used to train Dealix-hosted foundation models or shared with third-party model providers for their training. Where Dealix uses third-party LLM providers, those providers are listed as sub-processors and contractually bound to a zero-training and zero-retention posture on inference traffic, subject to provider-specific exceptions disclosed in the sub-processor list. Internal evaluations and prompt-engineering work use synthetic, opt-in, or anonymised datasets. Customer-facing AI features that affect a data subject's rights (automated decision-making per PDPL Art. 4) are surfaced as such with explainability and human-review pathways.

### 3.11 Records of Processing (PDPL Implementing Regulation Art. 31)

Dealix maintains a Record of Processing Activities (RoPA) covering both its controller and processor capacities. The RoPA summary is available to customers under NDA on request; the internal record is held by the DPO.

### 3.12 DPO Contact

- **Dealix Data Protection Officer (Placeholder):** dpo@dealix.com (canonical address; appointed DPO named in `docs/legal/DPO_APPOINTMENT_LETTER.md`).
- Cross-reference: `docs/legal/DPO_APPOINTMENT_TEMPLATE.md`.

## 4. KPIs

- **Primary:** 100% of DSAR requests met within contractual SLA over a rolling 90-day window.
- Zero unresolved cross-border transfers outside a documented basis.
- 100% of new sub-processors notified per DPA cadence before go-live.
- Annual RoPA refresh signed by DPO.

## 5. Dependencies

- DPO appointment and registration where required.
- Continued maintenance of `docs/DATA_MAP.md` as the data-flow source of truth.
- Kingdom-eligible region availability for the residency option.
- Customer-facing trust portal section publishing the sub-processor list.

## 6. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Lead Engine: `docs/product/saudi_lead_engine.md`
- Pricing: `docs/pricing/pricing_packages_sa.md`
- Security overview: `docs/trust/security_overview.md`
- Incident response: `docs/trust/incident_response.md`
- Access control: `docs/trust/access_control.md`
- Internal: `docs/DATA_MAP.md`, `docs/DATA_RETENTION_POLICY.md`, `docs/PRIVACY_PDPL_READINESS.md`, `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`
- Legal: `docs/DPA_DEALIX_FULL.md`, `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`, `docs/PRIVACY_POLICY_v2.md`
- Risk register: `docs/legal/enterprise_risk_register.md`

## 7. Owner & Review Cadence

- Owner: Head of Legal & Compliance (HoLegal); DPO is functional owner.
- Reviewed every 30 days during GTM window; quarterly thereafter; immediate review on any PDPL Implementing Regulation revision.

## 8. Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-13 | Initial draft (W3.T07b) | HoLegal |

## 9. External Attestations

| Attestation | Status | Availability |
|---|---|---|
| SDAIA compliance self-attestation | Live | Under NDA |
| NDMO standards mapping | Live | Under NDA |
| Cross-border transfer impact assessment | Live | Under NDA |
| RoPA summary | Live | Under NDA |
