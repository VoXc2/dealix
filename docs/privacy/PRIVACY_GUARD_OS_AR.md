# Privacy Guard OS
## نظام حماية الخصوصية

**Document Type:** Privacy Policy
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This document defines the privacy guard for Dealix, ensuring compliance with Saudi Personal Data Protection Law (PDPL) and protecting client data.

---

## 2. Saudi PDPL Compliance

### 2.1 Key Requirements

| Requirement | Implementation |
|-------------|----------------|
| Lawful basis for processing | Consent or legitimate interest documented |
| Purpose limitation | Data used only for stated purpose |
| Data minimization | Collect only necessary data |
| Accuracy | Keep data accurate |
| Storage limitation | Retain only as long as needed |
| Security | Appropriate security measures |
| Accountability | Document all processing |
| Data subject rights | Support access, correction, deletion |

### 2.2 Data Subject Rights

| Right | Implementation |
|-------|----------------|
| Access | DSR (Data Subject Request) process |
| Rectification | Update upon request |
| Erasure | Delete upon request (unless legal obligation) |
| Restriction | Restrict processing upon request |
| Portability | Export in machine-readable format |
| Objection | Stop processing upon objection |

---

## 3. Data Classification

### 3.1 Data Categories

| Category | Examples | Handling |
|---------|----------|----------|
| Public business info | Company name, website, public signals | Public, no restrictions |
| Business contact | Email, phone, title, company | Business use, consent implied |
| Client operational | Workflows, tools, integrations | Protected, access limited |
| Sensitive client data | PII, financial, passwords | Maximum protection, lawful basis required |
| Secrets | API keys, credentials, tokens | Never in prompts/logs/reports |
| Payment/legal | Contracts, invoices, negotiations | Legal review required |

### 3.2 PII Definition

Personal Identifiable Information (PII):
- Names
- Email addresses
- Phone numbers
- National IDs
- IBAN numbers
- Physical addresses
- Any data that can identify an individual

---

## 4. Handling Requirements

### 4.1 Data Minimization

Collect only what is necessary:
- State the purpose
- Collect minimum necessary
- Don't collect "just in case"
- Delete when no longer needed

### 4.2 PII Handling

| Action | Requirement |
|--------|-------------|
| Collection | Minimum necessary, lawful basis |
| Storage | Encrypted, access controlled |
| Processing | Purpose limited, logged |
| Sharing | Only with consent or legal obligation |
| Deletion | Upon request or retention period end |

### 4.3 Secrets Handling

Never in:
- Prompts
- Logs
- Reports
- External messages
- Unencrypted storage

---

## 5. DPA Requirements

### 5.1 DPA Checklist

See `docs/wave8/DPA_CHECKLIST_AR_EN.md`

### 5.2 Key DPA Elements

| Element | Requirement |
|---------|-------------|
| Parties identified | Controller and processor identified |
| Processing scope | Clearly defined |
| Data categories | Specified |
| Purpose documented | Stated |
| Retention period | Defined |
| Security measures | Specified |
| Breach notification | 72-hour requirement |

---

## 6. Consent Management

### 6.1 Consent Requirements

| Type | Requirement |
|------|-------------|
| Marketing consent | Explicit opt-in |
| WhatsApp consent | Explicit, documented |
| Data processing consent | Clear purpose stated |

### 6.2 Consent Record

See `docs/wave8/CONSENT_RECORD_TEMPLATE.json`

---

## 7. Retention and Deletion

### 7.1 Retention Periods

| Data Type | Retention Period |
|-----------|------------------|
| Business contact | Active relationship + 2 years |
| Client data | Contract period + 5 years |
| Lead data | 1 year without engagement |
| Consent records | Duration + 3 years |
| Audit logs | 5 years |

### 7.2 Deletion Process

1. Request received (DSR)
2. Identity verified
3. Data located
4. Deletion confirmed
5. Customer notified

---

## 8. Related Documents

| Document | Purpose |
|----------|---------|
| `SAUDI_PDPL_OPERATIONAL_GUARD_AR.md` | Saudi PDPL specifics |
| `DPA_CHECKLIST_AR_EN.md` | DPA pre-signing checklist |
| `WHATSAPP_CONSENT_CHECKLIST_AR_EN.md` | WhatsApp consent |
| `PII_REDACTION_POLICY_AR.md` | PII handling |
| `RETENTION_DELETION_POLICY_AR.md` | Retention rules |

---

*Policy maintained by Agent #5 — Security Red Team*
