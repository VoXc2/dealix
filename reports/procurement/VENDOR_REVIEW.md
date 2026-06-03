# Vendor Review — Findings (2026-06-03)

Source: `data/procurement/vendors.jsonl` (validated against `schemas/vendor.schema.json`).

| Vendor | Category | Data access | Risk | Status | Key gap |
|--------|----------|-------------|------|--------|---------|
| AI Model API Provider | ai_api | metadata | high | in_review | DPA + residency; PII-redacted prompts |
| Cloud Hosting | hosting | client_data | high | tbd | KSA region + DPA |
| Transactional Email | email | pii | medium | not_reviewed | SPF/DKIM/DMARC + suppression sync |
| Managed MySQL | database | client_data | high | in_review | backups + residency |
| GitHub (SCM/CI) | devtools | metadata | medium | approved | least-priv enforced |

## Findings
- 🟢 No secrets shared with any vendor; PII redacted before AI prompts.
- 🟡 Two high-risk vendors handle client data without confirmed residency/DPA.
- 🟢 SCM/CI vendor reviewed and least-privilege.

**Action (founder):** confirm KSA residency + sign DPAs for hosting/database/AI
before storing client data at scale.
