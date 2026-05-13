# سجل الملكية الفكرية لديلكس — طبقة رأس المال

**الطبقة:** L1 · Capital Model
**المالك:** المؤسس
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [IP_REGISTRY.md](./IP_REGISTRY.md)

## السياق
IP Registry هو القائمة المرجعية لملكية ديلكس الفكرية: المنهجيات،
القوالب، Playbooks، البيانات، Benchmarks، الوحدات البرمجية،
المعايير، والمواد التدريبية. هو العرض الموحَّد الذي يحوّل Capital
Ledger ونظام تدرّج الأصول إلى جدول أصول واحد قابل للدفاع — الجدول
الذي يُستخدم في محادثات المستثمرين، ومفاوضات الشركاء، وفي التموضع
التنافسي المُشار إليه في `docs/COMPETITIVE_POSITIONING.md` وفي السرد
الاستراتيجي في `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## البنية

| العمود | الوصف |
|---|---|
| IP Asset | الاسم المرجعي |
| Type | Methodology / Template / Playbook / Dataset / Benchmark / Software Module / Standard / Training Material |
| Description | تعريف بسطر واحد |
| Used In | الخدمات أو المنتجات أو المحتوى الذي يظهر فيه الأصل |
| Status | Core / Building / Sunset |

## السجل الابتدائي

| IP Asset | Type | Description | Used In | Status |
|---|---|---|---|---|
| Dealix Method | Methodology | Diagnose → Design → Build → Validate → Deliver → Prove → Expand | All services | Core |
| Proof Pack Template | Template | Standard proof of delivery and impact | All services | Core |
| Arabic QA Guide | Standard | Arabic business writing quality | Reports / drafts | Core |
| Saudi B2B Playbook | Playbook | Sector-specific revenue ops | Sales / Revenue | Building |
| Governance Matrix | Policy | Risk and approval rules | All services | Core |

هذه الصفوف الخمسة هي الـ IP المرجعي. يُضاف أي أصل إضافي حين يصل إلى
Stage 3 في `docs/assets/ASSET_GRADUATION_SYSTEM.md`.

## أنواع IP — التصنيف الكامل

- **Methodology** — عملية من البداية إلى النهاية (مثلاً Dealix Method).
- **Template** — هيكل وثيقة أو تقرير قابل لإعادة الاستخدام.
- **Playbook** — دليل تشغيلي خطوة بخطوة لقطاع أو حركة بيعية.
- **Dataset** — بيانات منظَّمة تملك ديلكس حقّ استخدامها والإشارة إليها.
- **Benchmark** — مرجع كمّي (مثلاً متوسطات زمن الردّ في الدعم).
- **Software Module** — شيفرة مُحزَّمة للاستخدام الداخلي أو لدى العملاء.
- **Standard** — قاعدة جودة تُطبّقها الشركة باستمرار.
- **Training Material** — محتوى دورة أو منهج شهادة.

## قواعد الإضافة / الترقية / الإيقاف

- **إضافة** عندما يصل أصل إلى Stage 3 في نظام التدرّج.
- **ترقية إلى Core** عند الاستخدام في 3+ خدمات والتحقّق من ملاحظات
  التسليم لدى العملاء.
- **Sunset** عند عدم الاستخدام لربعَين متتاليَين، أو عند وصول بديل
  أفضل إلى حالة Core.

تُدوَّن كل التغييرات في Change log داخل هذا الملف، وتُعكَس في
السجل المرجعي على Notion.

## عدسة قابلية الدفاع

يُراجَع كل صف سنوياً على أربعة أسئلة:

1. هل الأصل فريد لديلكس أم سلعة عامة؟
2. هل يستطيع منافس استنساخه خلال ربع واحد؟
3. هل يؤثّر جوهرياً على Win-Rate أو على تكلفة التسليم؟
4. هل يحمل قيمة عربية أو حوكمية أو خاصة بالسعودية لا يستطيع المستورد
   مجاراتها؟

الأصول التي تفشل في الأسئلة الأربعة هي مرشّحة للإيقاف.

## الواجهات
| المدخلات | المخرجات | الملاك | الإيقاع |
|---|---|---|---|
| قرارات الترقية | صفوف جديدة في السجل | المؤسس | ربعياً |
| إحصائيات إعادة الاستخدام من السجل | تحديثات الحالة | المؤسس | ربعياً |
| مراجعة قابلية الدفاع السنوية | قائمة الترقية / الإيقاف | المؤسس | سنوياً |
| احتياجات المبيعات والمحتوى | مرشّحون لـ Stage 5 | المؤسس | ربعياً |

## المقاييس
- Core asset count — عدد الصفوف في Core؛ الهدف ≥ 10 خلال 12 شهراً.
- Building → Core conversion rate — نسبة صفوف Building المرفوعة خلال 4 أرباع؛ الهدف ≥ 50%.
- Defensibility score — نسبة الصفوف التي تجتاز ≥ 2 من أسئلة قابلية الدفاع؛ الهدف ≥ 80%.
- Sunset rate — صفوف Sunset سنوياً؛ الهدف ≤ 15% من الإجمالي.

## ذات صلة
- `docs/COMPETITIVE_POSITIONING.md` — يستخدم IP Registry لصياغة الـ Moat.
- `docs/BRAND_PRESS_KIT.md` — يستخرج أصول Stage 5 إلى المواد الخارجية.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — الخطة الاستراتيجية المعتمدة على تراكم IP.
- `docs/assets/ASSET_GRADUATION_SYSTEM.md` — خطّ الإمداد للسجل.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
