# docs/operating_factory — دليل المنظومة

هذا المجلد هو **العقل التشغيلي** لـ Dealix Maximum Revenue Factory. ابدأ من
الدستور ثم انتقل حسب حاجتك.

| الملف | متى تقرأه |
|-------|-----------|
| [`DEALIX_MAXIMUM_REVENUE_FACTORY_AR.md`](./DEALIX_MAXIMUM_REVENUE_FACTORY_AR.md) | **ابدأ هنا** — الدستور الكامل |
| [`DAILY_LOOP_AR.md`](./DAILY_LOOP_AR.md) | تشغيل اليوم بالساعة |
| [`WEEKLY_LOOP_AR.md`](./WEEKLY_LOOP_AR.md) | التعلّم الأسبوعي |
| [`MONTHLY_REVIEW_AR.md`](./MONTHLY_REVIEW_AR.md) | قرار التوسّع الشهري |
| [`ROLE_OWNERSHIP_AR.md`](./ROLE_OWNERSHIP_AR.md) | من يملك/يوافق على ماذا (RACI) |
| [`QUALITY_GATES_AR.md`](./QUALITY_GATES_AR.md) | كل بوابات الجودة |
| [`READY_TO_LAUNCH_CHECKLIST_AR.md`](./READY_TO_LAUNCH_CHECKLIST_AR.md) | متى ننزل السوق |

## ملفات مرتبطة

```txt
docs/privacy/    سياسات الخصوصية وتقليل البيانات
docs/security/   سياسة المحتوى الخارجي كبيانات غير موثوقة
reports/operating_factory/   حالة الحلقة + Scorecard الإطلاق
reports/account_intelligence/NIGHTLY_400_ACCOUNT_PACKS_REPORT.md
reports/gtm/MAXIMUM_REVENUE_FACTORY_OPERATING_LOOP_FINAL_REPORT.md
company_os/      طبقة التشغيل الفعلية (بيانات/حوكمة/مالية/تسليم)
scripts/operating_factory_check.py   فحص تكامل المنظومة
```

## الفحص

```bash
python3 scripts/operating_factory_check.py
```

يتحقّق من: اكتمال أقسام Scorecard، تغطية الحلقة اليومية للتدفّق الكامل، وجود
حلقة التعلّم الأسبوعية، تغطية البوابات (Email/Call/Proposal/Delivery)، خلو نسخة
العميل من الادعاءات المضمونة والأسماء الداخلية، ووجود سياسات الأمان والخصوصية.

---

*Dealix Operating Factory Index | 2026-06-03*
