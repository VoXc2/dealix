---
title: Dealix Security Overview (Saudi Enterprise)
doc_id: W3.T07a.security-overview
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [customer, partner, regulator]
language: en
ar_companion: docs/trust/security_overview.ar.md
related: [W0.T00, W3.T07b, W3.T07c, W3.T07d, W3.T15, W3.T27]
kpi:
  metric: enterprise_security_questionnaires_passed
  target: 12
  window: 90d
rice:
  reach: 80
  impact: 3
  confidence: 0.9
  effort: 2
  score: 108
---

# Dealix Security Overview (Saudi Enterprise)

## 1. Context

Saudi enterprise buyers — particularly the regulated tier (banking under SAMA, telco under CST, government under NDMO/SDAIA, healthcare under MoH and CCHI) — require a clear, written security narrative before granting Dealix access to any production data, even in a paid pilot. This document is the customer-facing summary of Dealix's security posture as of 13 May 2026. It is the artifact that procurement teams will attach to their internal vendor-risk file, that CISOs will read before approving a proof-of-value, and that legal teams will reference when negotiating the Data Processing Addendum.

The intent of this overview is not to substitute for the internal `docs/SECURITY_GUIDE.md`, `docs/SECURITY_RUNBOOK.md`, `docs/SECURITY_PDPL_CHECKLIST.md`, or `docs/PRIVACY_PDPL_READINESS.md` — those remain the source of truth for our engineering team. Instead, this document distills the controls a Saudi enterprise buyer needs to evaluate, organised against the Saudi regulatory backbone (PDPL, NCA ECC-1:2018, NDMO Data Management standards) and against the international frameworks (SOC 2 Type II, ISO/IEC 27001:2022) on which Dealix is currently on a defined trajectory.

## 2. Audience

- Enterprise CISO/CIO offices conducting initial vendor evaluation.
- Procurement and vendor-risk teams preparing internal approval files.
- Legal counsel negotiating MSA/DPA terms.
- Auditors and regulators requesting a vendor security profile.
- Dealix sales engineering and partner enablement teams.

## 3. Decisions & Content

### 3.1 Compliance and Certification Trajectory

Dealix operates today under a documented control framework derived from SOC 2 Trust Services Criteria, ISO/IEC 27001:2022 Annex A, and NCA Essential Cybersecurity Controls (ECC-1:2018). Formal certification is sequenced against revenue milestones and enterprise contractual demands.

| Standard | Current State | Target Milestone | Owner |
|---|---|---|---|
| SOC 2 Type II | Readiness review complete; control gaps logged | Type I report Q3 2026; Type II report Q1 2027 | HoLegal + CTO |
| ISO/IEC 27001:2022 | Statement of Applicability drafted; ISMS scope defined | Stage 1 audit Q4 2026; certification Q2 2027 | HoLegal |
| NCA ECC-1:2018 | Self-assessment against 114 controls complete | Third-party attestation Q3 2026 | CTO |
| NDMO Data Management & Personal Data Protection Standards | Gap analysis complete | Continuous compliance — no certificate issued by NDMO | HoLegal |
| ZATCA Fatoorah Phase 2 | Live in production | N/A — operational | HoP |

### 3.2 Encryption and Key Management

Dealix encrypts customer data at rest using AES-256 (FIPS 140-2 validated cryptographic modules where the underlying cloud provider exposes them). All customer data in transit is protected with TLS 1.3; TLS 1.2 is permitted only for legacy webhook receivers and is logged for review. Application-level encryption is applied to a defined set of sensitive fields (national ID fragments, payment tokens, OAuth refresh tokens) using envelope encryption with provider-managed KMS. Customer-managed keys (CMK / BYOK) are available on the Enterprise plan and are documented in the Enterprise Pack (`docs/procurement/enterprise_pack.md`). Key rotation is automated on a 90-day cycle for data-encryption keys and a 365-day cycle for key-encryption keys; emergency rotation is achievable within 4 hours of a verified compromise.

### 3.3 Network and Infrastructure Controls

Production workloads are isolated in dedicated VPCs with private subnets for data planes, public subnets only for managed load balancers, and explicit deny-all default network ACLs. WAF rules cover the OWASP Top 10 with custom rule packs for credential-stuffing and PII-exfiltration patterns. DDoS protection operates at the L3/L4 edge with automated mitigation for volumetric attacks. Saudi tenants are served from a Kingdom-eligible region where regulatory mandate or contractual commitment requires in-Kingdom processing — see `docs/trust/data_governance.md` for the residency narrative.

### 3.4 Application Security Lifecycle

Every change to the Dealix production codebase passes through a defined pipeline: peer code review (minimum one reviewer; two for changes touching authentication, payments, or PII handlers), automated static analysis (SAST), software-composition analysis (SCA) on every pull request, container image vulnerability scanning before deploy, and infrastructure-as-code policy checks. Secrets scanning runs pre-commit and post-merge; the repository's pre-commit configuration is documented in `docs/PRE_COMMIT_SETUP.md` and the secret-management posture is governed by `docs/security/` runbooks. The historic PAT exposure incident and its remediation are documented transparently in `docs/SECURITY_INCIDENT_PAT_EXPOSURE.md`.

### 3.5 Penetration Testing and Bug Bounty

Dealix commissions an external penetration test annually against the customer-facing application surface, with a focused web/API test and a Saudi-locale-specific test covering ZATCA invoicing flows and Arabic input handling (homoglyph, RTL-mixing). A private bug bounty programme operates via a recognised platform; the public programme will open after the first SOC 2 Type II report is published. Critical findings are remediated within 7 calendar days, high within 30, medium within 90, low at the next quarterly maintenance cycle. Pen-test attestation letters are made available under NDA on request.

### 3.6 Vulnerability Management

A continuous vulnerability-management programme operates against three layers: cloud configuration drift (CSPM tooling), container and OS-level CVEs (image scanning + runtime detection), and dependency CVEs (SCA + Renovate-driven patch automation). The triage SLAs above apply; an aggregated weekly vulnerability dashboard is reviewed by the CTO and recorded in `docs/WAVE17_VULNERABILITY_TRIAGE.md` and successor reports.

### 3.7 Monitoring, Detection, and Response

Production telemetry is shipped to a central observability stack (logs, metrics, traces) with a 90-day hot retention window. Security-relevant events (authentication anomalies, privilege escalation, data-export volume spikes, unusual cross-tenant query patterns) are forwarded to a detection-and-response pipeline with on-call paging via a defined rotation. Incident response is governed by `docs/trust/incident_response.md` (customer-facing) and `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` (internal).

### 3.8 Personnel Security

All Dealix employees with access to production environments complete a background check process consistent with Saudi labour law and the contractual jurisdiction of the employee. Annual security awareness training is mandatory; role-specific training (secure-coding for engineers, data-handling for support, phishing-resistance for finance) is delivered quarterly. Access is revoked within four working hours of termination; emergency revocation is automated for high-risk role changes.

### 3.9 Business Continuity and Disaster Recovery

Dealix maintains a documented RTO of 4 hours and RPO of 15 minutes for the customer-facing application tier. Backups are encrypted, geographically separated within the Kingdom-eligible region set, and tested through quarterly restore drills. The DR plan and drill evidence are referenced in `docs/DRILL_PLAN.md` and the operational readiness playbook.

### 3.10 Third-Party Risk

Sub-processors are listed in `docs/legal/COMPLIANCE_CERTIFICATIONS.md` and notified in advance per the DPA template. Each sub-processor undergoes an initial security assessment and annual re-assessment, weighted by data sensitivity and regulatory exposure (e.g., LLM providers, payment processors, and identity providers receive deepest review).

## 4. KPIs

- **Primary:** 12 enterprise security questionnaires successfully completed in 90 days.
- Mean response time to a customer security questionnaire ≤ 5 working days.
- Zero P1 security findings from external pen test left unremediated past SLA.
- 100% of new sub-processors approved through DPA notification flow before go-live.

## 5. Dependencies

- ISMS scope sign-off (HoLegal + CTO).
- Customer-facing trust portal (publication of attestation letters under NDA).
- Saudi-region infrastructure footprint expansion (CTO).
- Legal review of trust-page public claims (HoLegal).

## 6. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Lead Engine: `docs/product/saudi_lead_engine.md`
- Pricing: `docs/pricing/pricing_packages_sa.md`
- Internal security: `docs/SECURITY_GUIDE.md`, `docs/SECURITY_RUNBOOK.md`, `docs/SECURITY_PDPL_CHECKLIST.md`
- Data governance: `docs/trust/data_governance.md`
- Incident response: `docs/trust/incident_response.md`
- Access control: `docs/trust/access_control.md`
- Enterprise procurement bundle: `docs/procurement/enterprise_pack.md`
- Risk register: `docs/legal/enterprise_risk_register.md`

## 7. Owner & Review Cadence

- Owner: Head of Legal & Compliance (HoLegal), co-signed by CTO for technical controls.
- Reviewed every 30 days during the 90-day GTM window, then quarterly.
- External-claim changes require legal sign-off before publication.

## 8. Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-13 | Initial draft (W3.T07a) | HoLegal |

## 9. External Attestations

| Attestation | Status | Availability |
|---|---|---|
| SOC 2 Type I report | Targeted Q3 2026 | Under NDA after issuance |
| SOC 2 Type II report | Targeted Q1 2027 | Under NDA after issuance |
| ISO/IEC 27001:2022 certificate | Targeted Q2 2027 | Public after issuance |
| NCA ECC-1:2018 third-party attestation | Targeted Q3 2026 | Under NDA |
| Annual pen-test attestation letter | Available now | Under NDA |
| ZATCA Fatoorah Phase 2 compliance evidence | Available now | Public |
