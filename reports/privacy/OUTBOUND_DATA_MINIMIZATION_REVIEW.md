# Outbound Data Minimization Review — Dealix (Phase 8)

Report template for reviewing outbound data minimization against SDAIA PDPL: only the minimum data, only the defined classes, no special-category data, no PII in logs/reports, and deletion on trigger. Defaults stay `dry_run=true`, `approval_required=true`, `send_enabled=false`.

Builds on `company_os/governance/pdpl_checklist.md`, `docs/privacy/OUTBOUND_DATA_RETENTION_MATRIX.md`, and `docs/privacy/PROSPECT_DATA_CLASSIFICATION.md`.

---

## 1. Summary

| Field | Value |
|-------|-------|
| Review date | `____` |
| Records reviewed | `____` |
| Over-retention found | `____` |
| Deletions executed | `____` |
| PII leakage found | `____` (target: none) |

---

## 2. Class Compliance

| Class | In use | Minimized | Notes |
|-------|--------|-----------|-------|
| Public company data | ☐ | ☐ | public sources only |
| Role/business contact | ☐ | ☐ | role + domain only |
| Derived signal | ☐ | ☐ | cite evidence_level |

> Only these 3 classes are permitted. No special-category data. No personal (non-business) profiles.

---

## 3. Retention & Deletion

| Trigger | Acted on | Count |
|---------|----------|-------|
| Opt-out / unsubscribe → suppression + delete | ☐ | `__` |
| Deletion request (data subject) | ☐ | `__` |
| Idle expiry (90 days) | ☐ | `__` |
| Hard bounce → suppress + remove | ☐ | `__` |

Matrix: `docs/privacy/OUTBOUND_DATA_RETENTION_MATRIX.md`. Runbook: `docs/privacy/DELETION_REQUEST_RUNBOOK_AR.md`.

---

## 4. Minimization Checks

| Check | Status |
|-------|--------|
| Only minimum fields stored | ☐ |
| No special-category data | ☐ |
| No PII in logs/reports (role/domain placeholders) | ☐ |
| KSA processing, no cross-border transfer | ☐ |
| First-party sourcing only (no purchased lists) | ☐ |

---

## 5. Decision

| Field | Value |
|-------|-------|
| Minimization compliant | `____` (yes/no) |
| Actions required | `____` |
| Reviewed by | `____` |

---

*Dealix · Outbound Data Minimization Review · minimize + delete on trigger · no PII, no special-category data · send_enabled stays false · Ref: SDAIA PDPL*
