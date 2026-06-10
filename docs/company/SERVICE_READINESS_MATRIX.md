# Service Readiness Matrix

**الغرض:** منع خداع الذات — كل صف **خدمة + أدلة + score + حالة**.

**المزامنة:** شغّل `python scripts/print_service_readiness_matrix.py` لطباعة جدول محدّث من `SERVICE_ID_MAP` + `service_readiness_defaults.yaml` (للصق هنا أو في الاجتماعات).

**الربط:** [`EVIDENCE_SYSTEM.md`](EVIDENCE_SYSTEM.md)، [`SELLABILITY_POLICY.md`](SELLABILITY_POLICY.md)، [`SERVICE_ID_MAP.yaml`](SERVICE_ID_MAP.yaml).

---

## المصفوفة (أساس الريبو — آخر تحديث يدوي)

| Service | Offer | Scope | Intake | QA | Demo pack | Product | Gov docs | Proof tpl | Sales | Score | Status |
|---------|:-----:|:-----:|:------:|:--:|:-----------:|:-------:|:--------:|:---------:|:-----:|------:|--------|
| Lead Intelligence Sprint | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100 | Sellable |
| AI Quick Win Sprint | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100 | Sellable |
| Company Brain Sprint | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100 | Sellable |
| AI Support Desk Sprint | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | 90 | Sellable |
| AI Governance Program | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | 100 | Sellable |

**ملاحظات:**

- **Demo pack ✅** للصفوف الثلاثة الأولى = مجلدات [`demos/lead_intelligence_demo`](../../demos/lead_intelligence_demo) و[`demos/ai_quick_win_demo`](../../demos/ai_quick_win_demo) و[`demos/company_brain_demo`](../../demos/company_brain_demo).  
- **⚠️** لـ Support / Governance = لا يوجد حالياً مجلد `demos/` مخصص بنفس الصرامة؛ لا تسوق بقوة قبل إكمال الـdemo أو صرّح بـBeta.

---

## قواعد الحالة

| Score | Status |
|------:|--------|
| 90–100 | Sellable / Excellent |
| 85–89 | Sellable / Improve |
| 70–84 | Beta — لا scale في التسويق |
| أقل من 70 | Not Ready — لا بيع |

Score هنا = **Service Readiness** (0–100) من الحزمة؛ المعايير الإضافية في [`SELLABILITY_POLICY.md`](SELLABILITY_POLICY.md).
