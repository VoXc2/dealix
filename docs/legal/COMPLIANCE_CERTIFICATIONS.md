# Compliance, Assurance & Certification Evidence Inventory

> **Status:** CURRENT_ONLY evidence inventory.  
> **Audience:** founder, delivery, sales, partners, enterprise diligence.  
> **Rule:** source code can prove a control exists; it cannot by itself prove legal compliance, regulatory registration, production deployment, tax status, data residency, or a third-party certification.

## 1. Evidence Classes

Use only these statuses:

| Status | Meaning |
|---|---|
| `VERIFIED_CURRENT` | Current primary evidence has been checked for the exact entity/deployment/scope. |
| `CONTROL_IMPLEMENTED_NOT_ATTESTED` | A control/capability exists in source or process, but no blanket compliance/certification claim is authorized. |
| `PLANNED` | Roadmap item; not current capability or certification. |
| `UNKNOWN_HOLD` | Evidence is absent, stale, scope-ambiguous, or not independently verified. Do not market as achieved. |
| `NOT_APPLICABLE_PROVEN` | Non-applicability has been assessed for a defined scope and evidence exists. |

**Never convert `CONTROL_IMPLEMENTED_NOT_ATTESTED` into “Compliant”, “Certified”, “Ready”, or “Production-ready”.**

---

## 2. Current Dealix Assurance Inventory

| Area | Current authority | Evidence type | Commercial wording allowed |
|---|---|---|---|
| Saudi PDPL | `CONTROL_IMPLEMENTED_NOT_ATTESTED` | Consent/audit/erasure/export/privacy-control code and policies | “PDPL-aware controls” / “controls designed to support PDPL obligations” |
| ZATCA e-invoicing | `CONTROL_IMPLEMENTED_NOT_ATTESTED` | Source capabilities and readiness tooling | “ZATCA/e-invoicing readiness support”; verify taxpayer wave + deployed integration |
| NCA cybersecurity controls | `CONTROL_IMPLEMENTED_NOT_ATTESTED` | Control mapping / gap assessment / governance | “NCA control mapping / readiness support”; never “NCA certified” |
| ISO 27001 | `UNKNOWN_HOLD` unless a current certificate is attached | Third-party certificate required | No certification claim |
| SOC 2 | `UNKNOWN_HOLD` unless a current report is attached | Independent report required | No attestation claim |
| Commercial Registration | `UNKNOWN_HOLD` in this repository unless current official evidence is attached in the approved evidence store | Official Saudi registry evidence | Do not publish a number/status from placeholders |
| VAT registration | `UNKNOWN_HOLD` in this repository unless current official evidence is attached in the approved evidence store | Official ZATCA evidence | Do not claim active registration from source/config |
| Data residency | `UNKNOWN_HOLD` per deployment | Live provider/resource/location evidence | State only verified deployment-specific residency |
| Encryption | `UNKNOWN_HOLD` per deployed service until runtime/config evidence is collected | Live deployment + key/config evidence | Distinguish designed/configured capability from deployed proof |
| Uptime / incidents | `UNKNOWN_HOLD` unless current telemetry window is attached | Monitoring/incident evidence | No static uptime or “zero incidents” claims without dated telemetry |

---

## 3. PDPL — What We Can and Cannot Claim

### Source controls currently available

Dealix contains implementation support for items such as:
- consent records and consent-request preparation;
- tenant-scoped access patterns;
- personal-data export and erasure helpers;
- audit trails;
- breach-notification preparation;
- data-processing/governance workflows.

These are **control evidence**, not a legal attestation that Dealix or a customer is fully compliant.

### Breach notification

The Saudi PDPL law requires a controller to notify the competent authority of qualifying breaches in accordance with the Regulations. The Implementing Regulations specify notification within **72 hours of awareness** when the incident may harm personal data/data subjects or conflict with their rights or interests (Implementing Regulations, Article 24). The controller must also notify affected data subjects without undue delay when the applicable harm threshold is met.

Operational consequence for Dealix:
- breach tooling should prepare evidence and deadlines;
- the incident must be assessed against the regulatory threshold;
- legal/regulatory submission remains an authorized external action;
- a source helper must never report “PDPL compliant = true” simply because controls exist.

### Registration / DPO / transfer obligations

Whether controller registration, a DPO, DPIA, transfer safeguards, or other obligations apply depends on the legal entity and processing facts. Treat each as `UNKNOWN_HOLD` until current official evidence and scope analysis are available.

This document is operational governance, not legal advice.

---

## 4. ZATCA / E-Invoicing — Evidence Boundary

Source code may demonstrate technical capabilities such as invoice construction, validation, QR/TLV helpers, hashes, or API adapters. It does **not** prove:
- that the Dealix legal entity is registered for VAT;
- that a particular taxpayer is in a particular integration wave;
- that production credentials are valid;
- that invoices are currently cleared/reported successfully;
- that a customer is compliant;
- that a deployed release equals the reviewed source.

A current ZATCA claim requires the relevant official taxpayer/wave evidence plus live integration receipts for the exact deployment/customer.

Commercial wording:
- allowed: “e-invoicing readiness/integration support”;
- blocked without evidence: “ZATCA compliant”, “ZATCA certified”, “production-ready”, “all invoices clear automatically”.

---

## 5. Cybersecurity / NCA / ISO / SOC

- Mapping controls to NCA guidance or running a gap assessment is not certification.
- A repository security policy is not proof that the deployed system follows it.
- ISO 27001 can be claimed only with a current certificate whose organization/scope matches the claim.
- SOC 2 can be claimed only with the relevant current independent report and scope.
- Pen-test, vulnerability-scan, incident, backup/restore and SLO claims require dated evidence.

---

## 6. Sub-Processors and Cross-Border Processing

Do not maintain a static “current sub-processor” list by inferring from packages, old architecture, provider accounts, or historical documentation.

For a customer/deployment, derive the list from:
1. exact deployed services/providers;
2. exact data categories and purposes;
3. processor/sub-processor contractual terms;
4. actual regions/data flows;
5. required transfer safeguards and risk assessment;
6. customer-specific agreement/notice.

Provider presence in source code ≠ provider used in production. Provider credential presence ≠ authorized processing.

---

## 7. Evidence Required Before External Claims

### Company / tax status
- current official commercial-registration evidence;
- current VAT/tax registration evidence where applicable;
- exact legal entity name matching the claim.

### PDPL
- processing inventory / ROPA appropriate to scope;
- lawful-basis/consent evidence where relevant;
- privacy notices;
- processor/sub-processor evidence;
- transfer analysis where relevant;
- security controls and incident procedure;
- registration/DPO/DPIA evidence if applicable;
- deployment-specific data-flow evidence.

### ZATCA
- taxpayer/wave evidence;
- production integration identity/credentials (never exposed in reports);
- dated validation/clearance/reporting receipts;
- exact deployed release identity.

### Security certifications
- valid third-party certificate/report;
- entity and scope match;
- validity dates;
- evidence reference safe to disclose.

---

## 8. Claims Firewall

Blocked unless directly proven for the exact scope:
- “PDPL Compliant” / “Saudi-PDPL compliant”;
- “ZATCA Ready/Compliant/Certified” as a blanket company claim;
- “Saudi data residency” as a blanket claim;
- “ISO 27001 certified” / “SOC 2 compliant”;
- “0 incidents” or fixed uptime without a dated telemetry window;
- “production-ready” based only on source code/tests;
- “registered / VAT active” based on placeholders or config;
- guaranteed refund/KPI/revenue terms not present in an approved customer-specific agreement.

Preferred wording:
- “PDPL-aware controls”; 
- “e-invoicing readiness support”; 
- “control mapping / evidence pack”; 
- “deployment-specific status available after verification”; 
- “UNKNOWN/HOLD pending evidence”.

---

## 9. Production Evidence Is a Separate Layer

`source capability != source acceptance != runtime acceptance != deployed identity != customer value != public proof`

Before a public trust claim that depends on production:
1. accepted source SHA;
2. deployed Web/API/service SHA identity;
3. live configuration/runtime evidence;
4. backup/restore and rollback evidence where relevant;
5. current telemetry/security evidence;
6. public surface/index parity;
7. claim-specific evidence reference.

HTTP 200 alone is not release identity or Production Green.

---

## 10. Ownership and Update Rule

Whenever an assurance status changes, record:
- date/time;
- entity/deployment/customer scope;
- old status;
- new status;
- primary evidence reference;
- verifier/reviewer;
- expiry/recheck date if applicable.

No agent may self-author a certificate or mark a control `VERIFIED_CURRENT` from its own generated report alone. Independent primary evidence is required.

---

## 11. Current Primary References

- Saudi Data & AI Authority (SDAIA): Personal Data Protection Law and Implementing Regulations.
- National Data Governance Platform: current PDPL services/guidance.
- ZATCA official taxpayer/e-invoicing notices for customer-specific wave and integration status.
- NCA official controls/guidelines for cybersecurity mapping.
- Dealix `data/brand/brand_authority.json` for claim policy.
- Dealix `docs/security/BUSINESS_CLAIMS_SAFETY_POLICY_AR.md`.
- GitHub issue `#1901` for current commercial-authority migration.
- GitHub issue `#1914` for current execution/model authority.

**Evidence before claims. Controls before certification. Exact scope before commercial authority.**
