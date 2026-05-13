---
title: Dealix Incident Response (Customer-Facing)
doc_id: W3.T07c.incident-response
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [customer, partner, regulator]
language: en
ar_companion: docs/trust/incident_response.ar.md
related: [W0.T00, W3.T07a, W3.T07b, W3.T07d, W3.T15, W3.T27]
kpi:
  metric: pdpl_72h_notification_sla_met_percent
  target: 100
  window: 90d
rice:
  reach: 60
  impact: 3
  confidence: 0.9
  effort: 1.5
  score: 108
---

# Dealix Incident Response (Customer-Facing)

## 1. Context

This document is the customer-facing summary of Dealix's incident response programme. It describes the commitments Dealix makes to enterprise customers around detection, containment, eradication, recovery, communication, and post-incident learning when a security incident or personal-data breach affects, or has a reasonable likelihood of affecting, a customer's data. The authoritative internal artefacts are `docs/PDPL_BREACH_RESPONSE_PLAN.md`, `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`, `docs/SECURITY_RUNBOOK.md`, and the on-call rotation defined in `docs/ON_CALL.md`. The Saudi regulatory baseline is the Personal Data Protection Law (PDPL), its Implementing Regulations, and the NCA Essential Cybersecurity Controls (ECC-1:2018). For sector-regulated customers (SAMA for financial institutions, CST for telcos, NHIC/MoH for healthcare), Dealix supports the customer's reporting obligation to its primary regulator.

## 2. Audience

- Customer security operations and incident management teams.
- Customer DPOs and legal/compliance counsel.
- SDAIA and sector regulators receiving customer-led notifications.
- Dealix internal incident commanders, legal, and customer success.

## 3. Decisions & Content

### 3.1 Definitions

- **Security incident:** any event that compromises, or has a reasonable likelihood of compromising, the confidentiality, integrity, or availability of Dealix systems or customer data.
- **Personal data breach:** a security incident that leads to the accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data processed by Dealix on behalf of a customer.
- **High-risk breach:** a personal data breach likely to result in a high risk to the rights of data subjects, triggering both regulator and data-subject notification obligations under PDPL.

### 3.2 Severity Classification

| Sev | Definition (customer-facing) | Example |
|---|---|---|
| **Sev 1** | Confirmed or highly likely unauthorised access to customer personal data; or full unavailability of a customer's tenant. | External actor exfiltration confirmed by logs. |
| **Sev 2** | Material degradation affecting a customer's ability to operate; or a contained security incident with limited blast radius. | Authentication outage > 30 min; suspicious anomaly contained to staging. |
| **Sev 3** | Limited impact; isolated to a small subset of users; recovery already underway. | One customer admin locked out due to misconfiguration. |
| **Sev 4** | Informational/no customer-visible impact. | Sub-processor advisory with no Dealix exposure. |

### 3.3 Detection and Triage

Detection sources include: continuous log/metric/trace analysis, security telemetry forwarders, customer reports, sub-processor advisories, public threat intelligence, and bug-bounty submissions. Dealix targets a **mean time to detect (MTTD) of ≤ 30 minutes for Sev 1**, with continuous improvement reported in internal reliability reviews. Once triggered, an incident commander is paged within 15 minutes, opens an incident channel, and begins the structured runbook in `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`.

### 3.4 Customer Notification SLAs

For confirmed or reasonably suspected personal data breaches affecting a customer's data, Dealix commits to:

- **Initial notification:** without undue delay and in any event within **24 hours** of confirmation, by both the contractually designated email channel and the customer's named operational contact, allowing the customer to meet the **PDPL 72-hour regulator notification window** to SDAIA.
- **Substantive update:** within **72 hours**, including known facts, categories and approximate number of data subjects affected, categories and approximate number of records, likely consequences, and the measures taken or proposed.
- **Ongoing updates:** at least every 24 hours for Sev 1, and at meaningful state changes for Sev 2.
- **Post-incident report:** within **15 calendar days** of incident closure, providing a written root-cause narrative, timeline, evidence summary, and remediation actions with target dates.

For non-personal-data security incidents that affect service availability, the standard customer notification path is the operational status channel plus a Sev 1/2 e-mail blast.

### 3.5 Regulator Notification

For incidents meeting the PDPL definition of a high-risk personal data breach, the **customer (as data controller) holds the primary obligation** to notify SDAIA within 72 hours of becoming aware. Dealix supports this obligation by providing, within the SLA above, the information the controller requires to file a complete notification. Where Dealix is also a controller (e.g., for platform operational data), Dealix files its own notification directly with SDAIA. Sector-specific notifications (SAMA, CST, MoH) are supported with the same information pack on request.

### 3.6 Escalation Matrix

| Trigger | First responder | Incident commander | Executive escalation |
|---|---|---|---|
| Sev 1 (personal data) | On-call SRE | Head of Engineering | CTO + HoLegal within 30 min; CEO within 2 h |
| Sev 1 (availability) | On-call SRE | Head of Engineering | CTO within 30 min |
| Sev 2 | On-call SRE | Senior engineer on duty | CTO at incident close |
| Sub-processor advisory | Security lead | Security lead | HoLegal review |

### 3.7 Customer Communication Channels

- **Primary:** the contractually nominated security/operational contact (set in the DPA, updatable via the customer admin console).
- **Secondary:** the operational status page (planned trust.dealix.com).
- **Escalation:** named executive sponsor on the customer's MSA; reachable via the 24/7 incident line for Sev 1.
- All notifications are bilingual (Arabic + English) for Saudi customers by default.

### 3.8 Post-Incident Review

Every Sev 1 and Sev 2 incident is followed by a **blameless root-cause analysis (RCA)** within 10 working days of incident closure. The RCA covers what happened, why it happened (the human and systemic contributing factors), what we did, what worked, what did not, and the durable remediations with owners and dates. The customer-shareable version is provided as part of the post-incident report at §3.4. The internal version is retained as audit evidence and reviewed against repeat-pattern signals during quarterly reliability reviews.

### 3.9 Sub-Processor Incidents

If a sub-processor experiences an incident that affects, or may affect, Dealix-processed customer data, the sub-processor's contractual notification flows into the same Dealix incident channel. Dealix re-assesses severity through the customer lens, applies the SLA in §3.4 from the moment Dealix has sufficient information to act, and where appropriate updates the sub-processor's status on the published list.

### 3.10 Forensics, Evidence, and Legal Hold

For Sev 1 incidents, evidence is preserved under a documented chain of custody. Where regulator or law-enforcement involvement is reasonably foreseeable, a legal hold is initiated; logs that would normally be eligible for retention rotation are exempted from the retention window for the duration of the matter. Counsel coordination is led by HoLegal.

## 4. KPIs

- **Primary:** 100% of qualifying personal-data incidents notified to the customer within the 24-hour initial-notification SLA, over a rolling 90-day window.
- 100% of Sev 1 incidents closed with an RCA delivered within 10 working days.
- 100% of post-incident reports delivered within 15 calendar days of closure.
- Sev 1 MTTD ≤ 30 minutes (continuous improvement).

## 5. Dependencies

- Up-to-date contractual contact list per customer (DPA flow).
- 24/7 on-call rotation staffed.
- Bilingual notification template library reviewed by HoLegal.
- Trust/status page infrastructure.

## 6. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Internal IR: `docs/PDPL_BREACH_RESPONSE_PLAN.md`, `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`, `docs/SECURITY_RUNBOOK.md`, `docs/ON_CALL.md`
- Security overview: `docs/trust/security_overview.md`
- Data governance: `docs/trust/data_governance.md`
- Access control: `docs/trust/access_control.md`
- Enterprise procurement: `docs/procurement/enterprise_pack.md`
- Risk register: `docs/legal/enterprise_risk_register.md`

## 7. Owner & Review Cadence

- Owner: Head of Legal & Compliance (HoLegal); operational co-owner is Head of Engineering.
- Reviewed every 30 days during GTM window, then quarterly; immediately after any Sev 1 incident.

## 8. Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-13 | Initial draft (W3.T07c) | HoLegal |

## 9. External Attestations

| Attestation | Status | Availability |
|---|---|---|
| Tabletop exercise report (annual) | Drafted | Under NDA |
| Live-fire drill report | Targeted Q3 2026 | Under NDA |
| PDPL compliance attestation | Live (self) | Under NDA |
