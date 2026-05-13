---
title: Data Retention — Windows per Data Class
doc_id: W6.T37.data-retention
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [internal, customer]
language: en
ar_companion: none
related: [W3.T07b]
kpi:
  metric: retention_policy_compliance
  target: 100
  window: per_audit
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 0.5
  score: governance-pdpl
---

# Data Retention

## 1. Context

PDPL Art. 21 requires personal data be kept only as long as necessary. This
file is the operational summary of retention windows applied across Dealix.
Authoritative customer-facing canon is
[`../trust/data_governance.md`](../trust/data_governance.md) §3.6. Internal
Arabic operational draft is `docs/DATA_RETENTION_POLICY.md`.

## 2. Audience

Engineers (must wire retention rules into stores), HoData (operational
deletion), HoLegal (policy ownership), customers' DPOs (assurance).

## 3. Retention Windows

| Data class | Default retention | Notes |
|------------|------------------|-------|
| Customer end-user profile data | Duration of subscription + 90 days | Then irreversible deletion or anonymisation |
| Transactional / billing records | 10 years | ZATCA / tax obligation |
| Authentication & session logs | 13 months | Security investigation window |
| Application audit logs (security-relevant) | 1 year hot, 7 years cold | Cold encrypted, access-restricted |
| Support-ticket content | Subscription + 12 months | Subject to controller override |
| LLM prompt / response telemetry | 30 days | Opt-in to extend for evaluation; no training on customer data |
| Marketing-site analytics | 24 months | Aggregated / anonymised |
| System backups | 35 days rolling | Forensic snapshots outside this window only |
| Eval production samples | 30 days | Anonymised; eval purposes only |
| Project memory / embeddings | Duration of contract or until deletion request | Per `SUPABASE_STAGING_RUNBOOK.md` |
| Webhook DLQ | 7–30 days | Re-process then purge |

## 4. Customer Overrides

Customers may shorten retention via the DPA scope worksheet (always
allowed) or lengthen with a defensible legal basis (HoLegal review).
Overrides are recorded against the tenant config and reflected in storage
TTLs.

## 5. Deletion Procedure

On scheduled expiry or deletion request:

1. Verify requester identity + scope (customer / user / project).
2. Trigger irreversible deletion across:
   - Primary DB rows
   - Supabase project tables
   - Embeddings index entries
   - Backup retention adjustments (next rotation window)
3. Issue written confirmation within SLA (DSAR: 25 calendar days).

Cold-storage deletion follows the same procedure; encrypted shards are
retired and the encryption key destroyed where contractual.

## 6. Cross-links

- Internal AR draft: `docs/DATA_RETENTION_POLICY.md`
- Customer canon: [`../trust/data_governance.md`](../trust/data_governance.md)
- Compliance perimeter: [`COMPLIANCE_PERIMETER.md`](COMPLIANCE_PERIMETER.md)
- PDPL rules: [`PDPL_DATA_RULES.md`](PDPL_DATA_RULES.md)
- DSAR SOP: `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`
- Audit log policy: [`AUDIT_LOG_POLICY.md`](AUDIT_LOG_POLICY.md)

## 7. Owner & Review Cadence

- **Owner**: HoLegal.
- **Review**: every 6 months; immediate on PDPL Implementing Regulation
  revision.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoLegal | Initial retention windows summary |
