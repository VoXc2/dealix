# Agent #13 — Legal Guard Final Report

**Date:** 2026-06-03
**Agent:** Agent #13 — Legal, Compliance, Contract Guard

---

## 1. ملخص تنفيذي

`docs/legal/` كان عنده وثائق artifacts قوية (DPA, MSA, DPO, DSAR,
Compliance, Risk Register). Agent #13 بنى **الـ operational handoff
machinery** الناقصة: متى يحتاج مراجعة، من يقرر، كيف يُسجَّل، ما هي
الـ triggers. لا agent يضع final legal decision — البشر (المؤسس +
محامٍ + DPO) فقط.

## 2. ما أُنشئ

| المسار | الملف |
| --- | --- |
| `docs/agent_definitions/agent_13_legal_compliance.md` | تعريف |
| `reports/legal/LEGAL_COMPLIANCE_GAP_AUDIT.md` | Gap audit |
| `docs/legal/LEGAL_REVIEW_POLICY_AR.md` | سياسة المراجعة |
| `docs/legal/CONTRACT_HANDOFF_CHECKLIST_AR.md` | تسليم العقد |
| `docs/legal/CASE_STUDY_PERMISSION_POLICY_AR.md` | إذن دراسة الحالة |
| `schemas/legal_review.schema.json` | schema |
| `schemas/contract_handoff.schema.json` | schema |
| `schemas/case_study_permission.schema.json` | schema |

## 3. Triggers المعرّفة (16)

راجع `docs/legal/LEGAL_REVIEW_POLICY_AR.md` § 2.

**Critical (5):** final contract, non-standard payment terms, enterprise
project > 250K SAR, partner revenue-share, legal claim about third party.

**High (8):** named case study, custom data processing, exclusivity,
indemnity > standard, liability cap < standard, SLA > 99.9%, cross-border,
regulated sector claim.

**Medium (3):** sub-processor, ZATCA non-standard, third-party brand.

## 4. Approval Levels

| Level | Who | When |
| --- | --- | --- |
| Low | Automated | instant |
| Medium | Operator/Founder | < 4h |
| High | Founder | < 24h |
| Critical | Lawyer + Founder | < 5d |

## 5. Schemas

- `legal_review.schema.json` — review record
- `contract_handoff.schema.json` — handoff record
- `case_study_permission.schema.json` — permission record

كلها مع `additionalProperties: false` و pattern matching.

## 6. Case Study Levels

| Level | Description | Approval |
| --- | --- | --- |
| L0 | No case study | none |
| L1 | Composite / hypothetical | labeled |
| L2 | Anonymized | Medium |
| L3 | Named | High + consent |
| L4 | Logo + quote | High + consent + DPO |
| L5 | Enterprise KPIs | Critical + lawyer |

## 7. Existing Legal Inventory (recap)

22+ وثيقة موجودة في `docs/legal/` و `docs/` (DPA, MSA, DPO, DSAR,
Sub-Processor, Risk Register, Compliance Certs, ToS, Privacy, Refund,
Cross-Border, PDPL Breach, DSAR SOP, etc.).

## 8. Remaining Blockers

1. **محامٍ مرخّص رسمي** غير معين.
2. **DPO معين رسمياً** غير موجود.
3. لا audit سنوي لهذه السياسة.
4. لا automated CI check يمنع نشر case study بدون `csp_*` APPROVED.
5. لا expiry reminder للـ permissions القديمة.
6. لا تغطية لازمات AI/ML التوليدي (EU AI Act، etc.).

## 9. Founder Next Actions

1. ✅ اعتماد Phase 1 docs.
2. ⏳ تعيين محامٍ خارجي (للـ Critical reviews).
3. ⏳ تعيين DPO (للـ High reviews).
4. ⏳ إضافة CI check: `tests/test_no_case_study_without_consent.py` (TBD).
5. ⏳ بناء claims evidence matrix (`CLAIMS_EVIDENCE_MATRIX_AR.md` TBD).
6. ⏳ بناء consent flow template (`CASE_STUDY_CONSENT_FLOW_AR.md` TBD).

## 10. Cross-Agent

- **Agent #14 (Localization):** claims = `ARABIC_BRAND_VOICE_AR.md` § 3 banned.
- **Agent #15 (Services):** كل deliverable مع claim = `legal_review.schema.json`.
- **Agent #16 (Data Room):** `case_study_permissions.jsonl` = data room evidence.
- **Agent #17 (Procurement):** vendor PDPL compliance = legal review trigger.

## 11. المراجع

- `docs/agent_definitions/agent_13_legal_compliance.md`
- `reports/legal/LEGAL_COMPLIANCE_GAP_AUDIT.md`
- `docs/legal/LEGAL_REVIEW_POLICY_AR.md`
- `docs/legal/CONTRACT_HANDOFF_CHECKLIST_AR.md`
- `docs/legal/CASE_STUDY_PERMISSION_POLICY_AR.md`
- `schemas/legal_review.schema.json`
- `schemas/contract_handoff.schema.json`
- `schemas/case_study_permission.schema.json`
- `docs/legal/FOUNDER_RISK_AND_COMPLIANCE_REGISTER_AR.md`
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md`
- `docs/SECURITY_PDPL_CHECKLIST.md`
- `docs/PDPL_BREACH_RESPONSE_PLAN.md`
- `docs/PRIVACY_POLICY_v2.md`
- `docs/TERMS_OF_SERVICE_v2.md`
