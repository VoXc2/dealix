# تمنيج البيانات — منظومة تحقيق القيمة

**الطبقة:** L3 · منظومة تحقيق القيمة
**المالك:** رئيس البيانات
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [DATA_PRODUCTIZATION.md](./DATA_PRODUCTIZATION.md)

## السياق
كل تكليف متكرّر ينتج بيانات. وبلا مخططات واضحة تبقى هذه البيانات
ارتجالية وتنهار جودة الذكاء الاصطناعي. يحدّد هذا الملف "منتجات البيانات"
القياسية لدى ديلكس، ومخططاتها، والانضباط الذي يحفظ نظافتها. ويغذّي
البنية في `docs/BEAST_LEVEL_ARCHITECTURE.md` وأعمال الموثوقية في
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`.

## المبدأ

> أي خدمة بلا مخطط واضح تصبح فوضى.

منتج البيانات مملوك، مُؤرَّخ، موثَّق، يصل إليه مستخدمون معتمدون،
ويُعاد استخدامه بين التكليفات.

## منتجات البيانات الأساسية

### Lead Dataset
- `company_name` (string)
- `city` (string)
- `sector` (enum)
- `source` (string)
- `relationship_status` (enum: none / consented / existing)
- `notes` (text)

### Support Dataset
- `message` (text)
- `channel` (enum: email / whatsapp / web / phone)
- `customer_type` (enum)
- `timestamp` (datetime)
- `category` (enum)
- `resolution_status` (enum: open / resolved / escalated)

### Document Dataset
- `title` (string)
- `owner` (string)
- `last_updated` (datetime)
- `sensitivity` (enum: public / internal / restricted)
- `source_type` (enum: file / wiki / drive / crm)
- `allowed_users` (list)

## الانضباط

- لكل مجموعة بيانات مخطط منشور وتعريف مُؤرَّخ.
- كل تغيير في المخطط يشحن عبر PR مع ملاحظات الترحيل.
- كل مجموعة بيانات لها وصيّ.
- المجموعات تحمل وسوم حساسية يحترمها الوكلاء.
- البيانات القديمة تُوسَم تلقائياً.

## الأنماط الخاطئة

- مخططات لكل عميل تنحرف بلا حدود.
- حقول حرّة حيث تلزم القوائم.
- الحساسية غير محدّدة افتراضياً.
- تكليفات متكرّرة بلا منتج بيانات.

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| Raw client inputs | Productized dataset | Data steward | Per engagement |
| Schema change request | New version + migration | Head of Data | Per change |
| Sensitivity labels | Agent access filter | Knowledge Agent | Per query |
| Data quality telemetry | Quality dashboard | Head of Data | Continuous |

## المقاييس
- Productization Coverage — نسبة التكليفات المتكرّرة على المخطط القياسي.
- Schema Drift — تغييرات المخطط لكل مجموعة كل ربع.
- Stewardship Coverage — نسبة المجموعات ذات وصيّ مسمّى.
- Sensitivity Compliance — نسبة السجلات الموسومة بصواب.

## ذات صلة
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — السياق المعماري
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — أعمال الموثوقية
- `docs/AI_STACK_DECISIONS.md` — قرارات الحزمة
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — موقف البيانات
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | مسودة أولى |
