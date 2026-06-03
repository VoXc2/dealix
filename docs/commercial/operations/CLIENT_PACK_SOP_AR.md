# SOP — حزمة عميل (عرض + ديك + ديمو)

**الغرض:** مسار واحد لكل اجتماع مبيعات — بدون إرسال آلي.

## قبل الاجتماع (5 دقائق)

1. افتح `/ar/ops/war-room` واختر الهدف.
2. اضغط **حزمة عميل** (أو من الطرفية):
   ```bash
   py -3 scripts/generate_client_pack.py --company "اسم الشركة"
   ```
3. المخرجات في `data/client_packs/<slug>/`:
   - `proposal.md` — عرض ثنائي اللغة (راجع ثم أرسل يدوياً)
   - `deck_notes.md` — ما تعدّله في الشرائح
   - `runbook_excerpt.md` — مقتطف من Runbook

## الديك (pptx)

1. انسخ القالب: `docs/commercial/ops_client_pack/dealix_ops_sales_kit_ar.pptx`
2. عدّل 3–5 شرائح حسب `deck_notes.md` (اسم الشركة، الألم، العرض، السعر).

## الديمو الحي

1. `/ar/business-now#strategy`
2. simulate حسب قطاع/مدينة/ميزانية العميل.
3. GTM أول 10 + Sales Script + Proof demo (من نفس الصفحة).

## بعد الاجتماع

1. حدّث حالة War Room (`meeting_booked` → `scope_requested` → `invoice_sent` يدوياً).
2. سجّل أدلة في `/ar/ops/evidence` عند أي إرسال يدوي.
3. لا revenue قبل `invoice_paid` · لا upsell قبل Proof Pack.

## مراجع

- Runbook كامل: [dealix_ops_runbook_ar.md](../ops_client_pack/dealix_ops_runbook_ar.md)
- سلم البيع: [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../MASTER_COMMERCIAL_OPERATING_PLAN_AR.md)
