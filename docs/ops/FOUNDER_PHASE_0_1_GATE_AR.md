# بوابة المرحلة 0–1 — أول Diagnostic مدفوع + Proof Pack

**الغرض:** صمام أمان قبل توسيع المنتج أو الفريق — يتماشى مع [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md).

---

## متى تُفتح البوابة (PASS)

| شرط | مصدر |
|-----|------|
| `payment_received` حقيقي (شركة حقيقية) | [evidence_events_tracker.csv](../commercial/operations/evidence_events_tracker.csv) |
| `proof_pack_delivered` حقيقي | نفس السجل |
| KPI غير placeholder | `dealix/transformation/kpi_founder_commercial_import.yaml` |

**تحقق:**

```bash
py -3 scripts/founder_comprehensive_plan_status.py --section phase
py -3 scripts/verify_first_paid_diagnostic_tracker.py
```

---

## عند BLOCKED

1. أغلق مسار إغلاق واحد — [EVIDENCE_EVENTS_CLOSE_PATH_AR.md](../commercial/operations/EVIDENCE_EVENTS_CLOSE_PATH_AR.md)
2. DoD تسليم — [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](../commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md)
3. دفع يدوي — [MANUAL_PAYMENT_SOP.md](MANUAL_PAYMENT_SOP.md)

**ممنوع حتى PASS:** بناء ميزات جديدة · توظيف مبيعات تقليدية · ادعاء «إيراد live» في التسويق.

---

*آخر تحديث: 2026-05-18*
