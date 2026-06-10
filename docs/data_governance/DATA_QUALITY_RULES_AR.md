# Data Quality Rules (AR)

---

## 1. Quality Dimensions

| Dimension | Description | Measurement |
|-----------|-------------|-------------|
| **Completeness** | هل الحقول المطلوبة ممتلئة | % of required fields non-null |
| **Accuracy** | هل القيم صحيحة | validation pass rate, sample verification |
| **Consistency** | هل متّسق عبر الأنظمة | reconciliation report |
| **Timeliness** | هل محدّث | time since last update |
| **Uniqueness** | هل لا تكرار | dedup rate |
| **Validity** | هل يطابق schema/rules | schema validation pass rate |

---

## 2. Per-Entity Rules

### Prospect
- `email`: required, valid format, normalized lowercase
- `phone`: optional, E.164 format
- `company_name`: required, dedup key
- `sector`: required, from allowlist
- `region`: required, from allowlist
- Dedup: email OR (company + phone)

### Contact
- `email`: required, unique per company
- `name`: required
- `title`: optional
- Dedup: email globally

### Client
- `company_id`: required, FK valid
- `status`: required, from allowlist (active, paused, churned)
- `contract_start`: required
- `contract_end`: optional

### Draft
- `content`: required, non-empty
- `language`: required (ar|en)
- `approval_id`: required before send

### Proposal
- `client_id`: required
- `version`: required, monotonic
- `status`: required (draft, sent, accepted, rejected)

---

## 3. Validation Patterns

- **Email:** RFC 5322 simplified
- **Phone KSA:** `+9665XXXXXXXX`
- **URL:** parseable
- **Date:** ISO 8601
- **Money:** decimal with currency
- **National ID:** 10 digits, checksum
- **VAT number:** KSA format

---

## 4. Drift Detection

Monthly report:
- % of entities with stale data
- % of entities with missing required fields
- Dedup rate
- Time since last activity

**Alert:** if drift > 10% → review

---

## 5. Quality Reports

- **Daily:** ingest validation errors
- **Weekly:** dedup + completeness
- **Monthly:** full quality scorecard

→ `reports/data_governance/DATA_QUALITY_REVIEW.md`

---

## 6. Remediation

- **Auto-fix:** normalize email, phone, dates
- **Manual review:** invalid values
- **Backfill:** missing required fields
- **Cleanup:** duplicates, orphans

---

## 7. Owner

- **Per entity:** assigned owner
- **Quality reports:** data lead
- **Remediation:** delivery team

---

> **Owner:** Data Lead · **Review:** شهري
