# Data Classification — Dealix (AR)

> **Source-of-truth:** `DATA_GOVERNANCE_OS_AR.md` §"Data Classification"

---

## D0 — Public

- Marketing copy
- Public pricing
- Published case studies
- Public job postings

**Handling:** unrestricted

## D1 — Business Metadata

- Company name
- Sector
- Region
- Company size (range, not exact)
- Public sources of leads

**Handling:** can be in analytics, can be in public reports (aggregated)

## D2 — Business Contact Info

- Business email
- Business phone
- Job title
- LinkedIn URL (public)

**Handling:**
- In CRM
- In analytics (with purpose)
- NOT in public reports

## D3 — Client Operational Data

- Drafts
- Approval logs
- Replies
- WhatsApp threads
- Proof packs
- Weekly reports

**Handling:**
- Tenant-scoped
- In LLM prompts with audit
- NOT shared across tenants
- Encrypted at rest

## D4 — Sensitive Client Data

- Pricing strategy
- Internal notes
- Medical/health (if any)
- Financial details
- Legal-sensitive copy

**Handling:**
- Tenant-scoped
- Redacted in LLM prompts unless necessary
- Field-level encryption (E4+)
- Access logged

## D5 — Secrets / Payment / Legal

- API keys
- Tokens
- Passwords
- Credit card numbers
- Bank accounts
- Private keys

**Handling:**
- NEVER in prompts (راجع `docs/ai_ops/PII_AND_SECRET_MODEL_POLICY_AR.md`)
- Encrypted in env / vault
- Audit on every access
- Auto-rotation

## D6 — Forbidden

- لا يُجمع أصلاً
- Blocked at intake
- Examples: بيانات الأطفال، biometric غير مصرح

---

## Cross-Border Rules

| Data class | Out of KSA? |
|------------|-------------|
| D0 | ✅ |
| D1 | ✅ (aggregated) |
| D2 | with DPA + redaction |
| D3 | with DPA |
| D4 | with explicit DPA + SCCs |
| D5 | with strictest controls |
| D6 | ❌ |

---

## Per-Field Classification

راجع `schemas/` للـ field-level classification:
- Required fields marked
- Sensitive fields marked with class
- PII fields redacted in export by default

---

> **Owner:** Data Lead + Privacy Officer · **Review:** كل release
