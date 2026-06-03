# تسليم السلم — بعد أول «نعم»

> بوابات: `invoice_paid` → `engagement_id` → Proof Pack → upsell

## 1) Diagnostic مدفوع (Ops)

| بند | مرجع |
| --- | --- |
| Scope | [dealix_ops_runbook_ar.md](../commercial/ops_client_pack/dealix_ops_runbook_ar.md) — مخرجات التشخيص |
| SOP | [DIAGNOSTIC_DELIVERY_SOP.md](../03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md) |
| وكيل | **dealix-delivery** |

**مخرجات:** Revenue Workflow Map · Source Quality · Pipeline Risk · Decision Passport · توصية Sprint/Retainer

## 2) Sprint 499

| بند | مرجع |
| --- | --- |
| يوم بيوم | [CUSTOMER_ONBOARDING_DAY_BY_DAY.md](CUSTOMER_ONBOARDING_DAY_BY_DAY.md) |
| 14 خطوة | [FIRST_CUSTOMER_ONBOARDING.md](FIRST_CUSTOMER_ONBOARDING.md) |
| API | `POST /api/v1/sprint/run` |
| وكيل | **dealix-delivery** |

**مخرج:** Proof Pack 14 قسم — لا upsell قبل تسليمه

## 3) Data Pack 1500 (بديل/توسيع)

- `POST /api/v1/data-os/import-preview/upload`
- Proof Pack + JSON DQ

## 4) Growth 2999 (Retainer)

- بعد Proof فقط
- [customer_success_playbook.md](customer_success_playbook.md)
- وكيل: **dealix-pm** + delivery

## ربط تجاري

[COMMERCIAL_WIRING_MAP.md](../COMMERCIAL_WIRING_MAP.md) · حالة الربط [FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md](FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md)
