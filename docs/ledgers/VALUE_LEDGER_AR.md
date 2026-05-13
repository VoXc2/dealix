# سجل القيمة — منظومة تحقيق القيمة

**الطبقة:** L3 · منظومة تحقيق القيمة
**المالك:** رئيس التنفيذ
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [VALUE_LEDGER.md](./VALUE_LEDGER.md)

## السياق
سجل القيمة هو المرجع الموحّد لكل ادعاءات القيمة التي أنتجتها ديلكس. هو
طبقة "الإيصالات" التي تحوّل عمل التنفيذ إلى نتائج تجارية قابلة للإثبات،
ويغذّي لوحات
`docs/BUSINESS_KPI_DASHBOARD_SPEC.md` والمنظور المالي
`docs/FINANCE_DASHBOARD.md`. بدون قيود في السجل تبقى حزم الإثبات مجرد
مخرجات معزولة، ومعها تستطيع ديلكس الحديث عن القيمة على مستوى الشركة —
بحسب القدرة والقطاع والخدمة والمجموعة الزمنية. وينفّذ السجل القاعدة
المعرَّفة في `docs/company/VALUE_REALIZATION_SYSTEM.md` والالتزام
الدستوري في `docs/DEALIX_OPERATING_CONSTITUTION.md` بضرورة وجود حزم
إثبات للأعمال المفوترة.

## مخطط السجل

| الحقل | النوع | الوصف |
|---|---|---|
| ID | string | معرّف فريد `V-NNN` |
| Client | string | اسم رمزي للعميل |
| Service | string | اسم الخدمة من سلّم الخدمات |
| Value Type | enum | Revenue / Time / Quality / Risk / Knowledge |
| Metric | string | الاسم الدقيق للمؤشر |
| Baseline | string | القيمة قبل (أو "unknown" مع السبب) |
| Result | string | القيمة بعد |
| Evidence | string | مسار حزمة الإثبات |
| Next Value | string | فرصة القيمة التالية المقترحة |
| Owner | string | مسؤول التنفيذ في ديلكس |
| Date | date | تاريخ التوقيع |

## القيود الابتدائية

| ID | Client | Service | Value Type | Metric | Baseline | Result | Evidence | Next Value |
|---|---|---|---|---|---|---|---|---|
| V-001 | Client A | Lead Intelligence | Revenue | ranked accounts | unknown | top 50 | proof pack | Pilot Conversion |
| V-002 | Client B | Quick Win | Time | manual hours | 6/week | 2/week | workflow report | Monthly AI Ops |

> الجدول أعلاه هو الصيغة البذرية. تضاف قيود جديدة عند كل تكليف ويجب أن
> ترتبط بمصدر دليل.

## القاعدة

> أي حزمة إثبات بدون قيد في سجل القيمة = **غير مكتملة**.

حزمة الإثبات هي الأثر التقني (بيانات، صور، تقارير) أما السجل فهو الأثر
التجاري. ويجب توفر الاثنين قبل اعتبار التكليف مكتملاً.

## التجميعات المنشورة

- **حسب نوع القيمة** — توزيع الإيراد/الوقت/الجودة/المخاطر/المعرفة.
- **حسب القدرة** — إسقاط القيمة على القدرات من
  `docs/company/CAPABILITY_VALUE_MAP.md`.
- **حسب الخدمة** — القيمة بحسب خط الخدمة من
  `docs/COMPANY_SERVICE_LADDER.md`.
- **حسب القطاع** — إشارة تركّز المخاطر وملاءمة القطاع.
- **حسب المجموعة الزمنية** — احتفاظ وتوسّع ربع سنوي.

## الإجراء

1. يفتح مسؤول التنفيذ قيداً مبدئياً عند انطلاق التكليف (خط الأساس).
2. يحدّث القيد عند التسليم (النتيجة + الدليل).
3. يسجّل مسؤول نجاح العميل فرصة القيمة التالية وتاريخ الإغلاق المستهدف.
4. يقدّم مسؤول نجاح العميل عرض القيمة التالية خلال 14 يوماً.
5. يعتمد رئيس التنفيذ القيد أسبوعياً ويوقّع الموجز الشهري.

## الأنماط الخاطئة

- إدخال قيود متأخرة من الذاكرة بعد أشهر.
- إغلاق قيد بدون رابط دليل.
- "Baseline = unknown" بدون مبرّر مكتوب.
- تعدّد القيود لتكليف واحد حين يكفي مقياس مركّب واحد.

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| Engagement kickoff metadata | Candidate ledger row | Delivery owner | Per engagement |
| Proof pack | Result + evidence link | Delivery owner | Per engagement |
| Ledger snapshot | Monthly aggregation report | Head of Delivery | Monthly |
| Cohort snapshot | Quarterly retention/expansion view | CEO | Quarterly |

## المقاييس
- Ledger Coverage — نسبة المشاريع الموثّقة في السجل.
- Median Time-to-Entry — وسيط الأيام بين الانطلاق وأول قيد.
- Evidence Completeness — نسبة القيود ذات رابط دليل صالح.
- Next-Value Pull-Through — نسبة القيمة التالية التي تحوّلت إلى إيراد.

## ذات صلة
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — لوحة المؤشرات المستهلِكة
- `docs/FINANCE_DASHBOARD.md` — لوحة المالية الرابطة للقيمة بالإيراد
- `docs/EXECUTIVE_DECISION_PACK.md` — الحزمة التنفيذية المرجعية
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — اشتراط حزمة الإثبات
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | مسودة أولى |
