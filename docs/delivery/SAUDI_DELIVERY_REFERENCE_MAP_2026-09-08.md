# Dealix Saudi Delivery Reference Map — 2026-09-08

Status: `REFERENCE_NOT_CERTIFICATION`.

Purpose: give `dealix-sales`, `dealix-delivery` and `dealix-engineer` one current Saudi reference map when preparing diagnostics, bid/no-bid packets, solution designs, acceptance plans and proof packs. This does **not** claim legal compliance, certification, regulator approval, licensing or customer eligibility.

## Authority rules

- Official source/version/date must be re-verified for every material customer/tender packet.
- `reference mapped != requirement satisfied`.
- `requirement satisfied != certification / regulator approval`.
- Dealix must not claim a license, classification, accreditation, NCA approval, SAMA authorization, SDAIA conformity, NDMO maturity level or government eligibility without direct evidence.
- Customer/legal/regulatory interpretation remains a separate review where required.
- External submission, binding quote, contract and production mutation remain exact action-bound L5.

## Reference matrix

| Delivery situation | Current Saudi reference family | What Dealix should prove in its packet | What Dealix must not claim |
|---|---|---|---|
| AI system / agent / RAG / decision support | SDAIA AI Ethics Principles and current SDAIA responsible-AI guidance | use-case boundaries, human accountability, transparency, fairness/bias controls, privacy/security, risk classification, evaluation and monitoring plan | SDAIA approval/conformity unless formally evidenced |
| Personal-data processing | Saudi PDPL + Implementing Regulations | lawful basis/purpose, minimization, retention, access controls, data-subject handling, processor/sub-processor boundary, incident/escalation responsibilities | blanket legal compliance from a technical design alone |
| Direct marketing / commercial messaging | PDPL Implementing Regulations direct-marketing provisions + Dealix Durable Consent / Suppression / ChannelEligibility | identity of sender, purpose, consent evidence where required, easy opt-out, withdrawal enforcement, suppression precedence, durable audit trail | public contact = consent; delivery = relationship |
| Cross-border personal-data transfer | Regulation on Personal Data Transfer Outside the Kingdom + customer DPA/data map | transfer purpose, data categories, destination, processor chain, safeguards/assessment where required, redaction/localization options | unrestricted transfer right |
| Government / enterprise data governance | NDMO / National Data Governance references applicable to the customer and tender | data ownership/stewardship, catalog/classification, quality, lineage, retention, access, metadata, evidence/provenance and operating roles | a specific NDMO/NDI maturity score without assessment evidence |
| General cybersecurity | NCA Essential Cybersecurity Controls (ECC 2-2024) and current implementation guides | control applicability matrix, identity/access, asset/config management, logging/monitoring, vulnerability/patching, backup/recovery, incident responsibilities, supplier risk | NCA certification/approval unless directly evidenced |
| Cloud workloads / cloud services | NCA Cloud Cybersecurity Controls (CCC 2-2024) | shared-responsibility model, cloud/data location, tenant isolation, IAM, encryption/key boundary, logging, backup/recovery, provider evidence | cloud compliance from provider name alone |
| Data lifecycle cybersecurity | NCA Data Cybersecurity Controls (DCC-1:2022) | classification-to-control mapping, data-at-rest/in-transit protection, lifecycle access, deletion/retention evidence, monitoring | DCC compliance without scope/control evidence |
| Critical/sensitive systems when applicable | NCA Critical Systems Cybersecurity Controls and sector-specific controls | applicability decision, critical-asset boundaries, elevated control/availability/incident evidence | critical-system scope determination without customer/regulator evidence |
| Open Banking / financial API integration | SAMA Open Banking Framework, business rules, technical standards/API specifications, certification/testing requirements | API contract, consent/customer-permission boundary, authentication/authorization, auditability, error/retry/idempotency, sandbox/certification path | SAMA license/authorization or production access without evidence |
| Government software / integration delivery | Digital Government Authority GPaaS/open-source/DevSecOps references and customer procurement requirements | source provenance, secure SDLC, API/integration contract, CI/CD evidence, SBOM/security scanning, documentation/handover, reuse/interoperability | government endorsement or mandatory applicability beyond the tender/customer scope |
| E-invoicing integration | ZATCA Fatoora official implementation/onboarding specifications for the customer's applicable wave | taxpayer/wave eligibility evidence, integration architecture, certificate/device boundary, invoice flow/error handling, acceptance/test evidence | that a named company is in scope without verified ZATCA/customer evidence |
| Health / digital-health solution | Ministry of Health / applicable health regulator requirements and sandbox path where relevant | data sensitivity, clinical/non-clinical boundary, integration, safety/human oversight, privacy/security and evidence plan | clinical approval, medical efficacy or regulator clearance without formal evidence |
| Public procurement | Etimad competition documents + entity-specific mandatory conditions | exact eligibility, scope decomposition, mandatory documents, references, bond/financial conditions, delivery capacity, acceptance, subcontract/partner route, deadlines | registration = qualification; tender listing = relationship; draft = submission |

## Official reference entry points

Re-verify version and applicability before use:

- SDAIA Data Governance / PDPL portal: `https://dgp.sdaia.gov.sa/`
- SDAIA AI ethics / publications: `https://sdaia.gov.sa/`
- NCA regulatory controls: `https://nca.gov.sa/en/regulatory-documents/controls-list/`
- NCA implementation guides: `https://nca.gov.sa/en/regulatory-documents/guides/`
- SAMA Open Banking: `https://www.openbanking.sama.gov.sa/`
- DGA GPaaS / open-source program: `https://dga.gov.sa/en/programs/GPaas`
- ZATCA e-invoicing: `https://zatca.gov.sa/en/E-Invoicing/`
- Etimad tenders: `https://tenders.etimad.sa/`
- Ministry of Health: `https://www.moh.gov.sa/`

## Packet contract by phase

### Diagnostic
Include only:
- observed evidence;
- hypothesis vs confirmed fact split;
- applicable-reference candidates;
- unknowns/data needed;
- expected economic/operational outcome;
- no compliance guarantee.

### Discovery
Resolve:
- system/data/process scope;
- accountable business owner;
- regulated/sensitive data classes;
- required integrations;
- customer security/legal/procurement constraints;
- acceptance authority and proof requirements.

### Solution / quote preparation
Produce:
- solution route: `BUILD_DIRECT / CONFIGURE_ADAPT / INTEGRATE_EXISTING_PRODUCT / QUALIFIED_PARTNER / SUBCONTRACT_PACKAGE / DISCLOSED_REFERRAL / DECLINE_DEFER`;
- reference applicability matrix;
- explicit customer/partner responsibilities;
- security/privacy/data boundaries;
- acceptance tests and proof plan;
- exclusions and unresolved regulatory/contract assumptions;
- customer-specific commercial scope, never a generic compliance promise.

### Delivery / proof
Retain:
- versioned requirement/reference snapshot used for the project;
- architecture/config/source evidence;
- test/acceptance receipts;
- deviations and approved exceptions;
- customer acceptance;
- permission boundary for any case study/customer proof.

## Current top-3 procurement application — 2026-09-08

### HRDF — AI Governance & Ethics
Primary references: SDAIA AI Ethics + PDPL/data governance + customer/tender-specific governance requirements. Dealix should route to `PRIME / QUALIFIED_PARTNER / DECLINE` only after eligibility, references and delivery authority are proven.

### Imam Turki Royal Nature Reserve — Data Office / RAG / AI Agents
Primary references: NDMO/data-governance requirements applicable in the tender, SDAIA AI Ethics for RAG/agents, PDPL where personal data exists, NCA controls for technical delivery. Required packet should separate Data Office operating model, warehouse/data quality, RAG/agent evaluation, security/privacy, evidence and maturity-assessment boundaries.

### Eastern Province Development Authority — Facility Management System
Primary references: tender requirements, NCA/data/privacy requirements applicable to hosted/integrated systems and government-delivery controls. Dealix should not pretend to own a full CAFM product when a qualified product/integration partner is the stronger route.

`CERTIFICATION_CLAIM_AUTHORITY=false`
`REGULATOR_APPROVAL_CLAIM_AUTHORITY=false`
`TENDER_SUBMISSION_AUTHORITY=false`
`L5_EXECUTED=NONE`
