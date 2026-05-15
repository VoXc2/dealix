# Compliance & Certifications Inventory

> **Status:** living document. Update when any certification status changes.
> **Audience:** founder, prospective enterprise customers, prospective investors.

---

## Current State (2026-05-12)

### Achieved ✅

| Certification | Status | Evidence | Renewal |
|---------------|--------|----------|---------|
| **PDPL (Personal Data Protection Law)** | Compliant by design | `integrations/pdpl.py`, `api/middleware/http_stack.py` | Continuous |
| **ZATCA Phase 2 e-Invoicing** | Wired (production-ready) | `integrations/zatca.py` (25 functions), invoice chaining | Continuous |
| **Saudi Commercial Registration (CR)** | {CR_NUMBER if set} | MCI portal | Annual |
| **VAT Registration** | {VAT_NUMBER if set} | ZATCA portal | Continuous |

### In Progress 🟡

| Certification | Status | Target completion | Owner |
|---------------|--------|--------------------|-------|
| **SDAIA Controller Registration** | Pre-DPO appointment | Q3 2026 (after first enterprise customer) | Founder |
| **ISO 27001** | Not started; gap analysis pending | Q1 2027 | Future hire |
| **SOC 2 Type II** | Not started | Q3 2027 (if US enterprise customer demands) | Future hire |

### Not Pursued 🔴 (and why)

| Certification | Reason for not pursuing now |
|---------------|------------------------------|
| HIPAA | Dealix doesn't process healthcare data; pursue if healthcare customer signs |
| PCI-DSS Level 1 | Moyasar handles cardholder data; Dealix is out-of-scope |
| GDPR (EU) | Not targeting EU customers; PDPL is functionally equivalent for Saudi customers |

---

## PDPL Compliance Detail

Dealix's PDPL stance is the foundational moat. Every claim must be backed by code.

### Article-by-Article Compliance Map

| PDPL Article | Requirement | Dealix Implementation | File |
|--------------|-------------|-----------------------|------|
| Art. 5 (Lawful Basis) | Consent or other lawful basis before processing | Consent flows for email + WhatsApp | `integrations/pdpl.py:build_consent_request_*` |
| Art. 11 (Notice) | Privacy notice before collection | Privacy policy page + just-in-time notices | `landing/privacy-policy.html` |
| Art. 13 (Erasure) | Right to deletion within 30 days | Cascade erasure with audit trail | `integrations/pdpl.py:build_erasure_audit_entry` |
| Art. 14 (Portability) | Right to data export (structured format) | JSON export per data subject | `integrations/pdpl.py:build_data_export` |
| Art. 18 (Record-keeping) | 5-year audit log for data access | Middleware logging on 15 personal-data paths | `api/middleware/http_stack.py:_PERSONAL_DATA_PREFIXES` |
| Art. 21 (Breach Notification) | Notify SDAIA within 72 hours | Breach notification builder + runbook | `integrations/pdpl.py:build_breach_notification` + `docs/ops/PDPL_BREACH_RUNBOOK.md` |
| Art. 32 (DPO) | Designate DPO for significant processing | Appointment kit ready; activates at enterprise customer #1 | `docs/legal/DPO_APPOINTMENT_TEMPLATE.md` |

### PDPL Sub-Processor Inventory

(Sub-processors that may access personal data on Dealix's behalf — public list at `landing/sub-processors.html`)

| Sub-processor | Location | Purpose | Data accessed | DPA in place? |
|---------------|----------|---------|---------------|---------------|
| Anthropic | US | LLM inference | Customer prompts (anonymized when possible) | Standard Anthropic terms |
| OpenAI | US | LLM inference fallback | Same as Anthropic | Standard OpenAI terms |
| Moyasar | KSA | Payment processing | Cardholder data (not seen by Dealix) | Standard Moyasar terms |
| Meta Platforms | US/EU | WhatsApp Business Cloud | Phone numbers, message content | Meta Business Terms |
| AWS (S3 me-south-1) | Bahrain (GCC) | Backups | Encrypted DB snapshots | AWS DPA |
| Resend / SendGrid | US | Transactional email | Email addresses, names | Standard terms |
| Google (Maps, CSE) | US | Lead enrichment | Public business data only | Standard terms |
| Hunter.io | France | Email enrichment | Public domain emails | Standard terms |
| Firecrawl | US | Page content extraction | Public web pages | Standard terms |
| Wappalyzer | US | Tech fingerprint | Public site metadata | Standard terms |

**Cross-border transfer note:** all transfers outside Saudi Arabia rely on Standard Contractual Clauses (SDAIA-approved or equivalent) and customer consent in the MSA.

---

## ZATCA Phase 2 Compliance Detail

Dealix issues e-invoices for every paid customer. All invoices are:

- UBL 2.1 compliant XML (`integrations/zatca.py:build_invoice_xml`)
- QR code with TLV encoding per ZATCA spec (`integrations/zatca.py:build_qr_tlv`)
- Cleared in real-time via Fatoorah API for B2B (or 24h reporting for B2C)
- Chained with previous invoice hash (Phase 2 mandate)
- Retained for 6 years (ZATCA mandate)

**For customers:** Dealix invoices appear in the customer's ZATCA portal automatically.

---

## Pre-Enterprise-Customer Checklist

Before signing any contract > 50K SAR/year, ensure:

- [ ] CR number is current with MCI
- [ ] VAT registration is active with ZATCA
- [ ] Privacy policy at `landing/privacy-policy.html` is updated within 30 days
- [ ] Sub-processors list at `landing/sub-processors.html` is current
- [ ] DPO appointed (or Path A external retainer in place — see `docs/legal/DPO_APPOINTMENT_TEMPLATE.md`)
- [ ] DPIA (Data Protection Impact Assessment) draft for the customer's use case
- [ ] MSA template (`docs/legal/ENTERPRISE_MSA_TEMPLATE.md`) reviewed by counsel for that customer's specifics
- [ ] Insurance: minimum 1M SAR cyber + 500K SAR professional indemnity

---

## Pre-Investor Checklist

Before any institutional fundraise:

- [ ] All "Achieved" certifications above documented with evidence
- [ ] "In Progress" items have written plans (not aspiration)
- [ ] Cap table is clean (no informal verbal equity promises)
- [ ] IP assignment agreements signed for any contractor who touched code
- [ ] ZATCA history pulled showing clean tax compliance

---

## Audit Trail

Whenever a certification status changes, append a row here:

| Date | Change | Owner |
|------|--------|-------|
| 2026-05-12 | Initial document created; PDPL + ZATCA marked Achieved | Founder |
