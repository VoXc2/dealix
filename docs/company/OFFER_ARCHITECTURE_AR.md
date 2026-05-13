# بنية العروض — طبقة رأس المال

**الطبقة:** L1 · Capital Model
**المالك:** المؤسس
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [OFFER_ARCHITECTURE.md](./OFFER_ARCHITECTURE.md)

## السياق
بنية العروض هي المخطّط الهيكلي لكل طرح تجاري تضعه ديلكس أمام
العميل. تُعرّف أربع طبقات، ودور كل طبقة في رحلة المشتري، والقاعدة
الصارمة التي تحكم الانتقال بينها. هي العمود الاستراتيجي لـ
`docs/OFFER_LADDER_AND_PRICING.md` ولحركة Pilot في
`docs/business/MANAGED_PILOT_OFFER.md`، وتعمل في خدمة تراكم رأس
المال المُعرَّف في `docs/company/DEALIX_CAPITAL_MODEL.md`.

## الطبقات الأربع

### 1. Front-end Offers — مدخل صغير وواضح ومنخفض المخاطرة
- AI Ops Diagnostic
- Revenue Diagnostic
- AI Quick Win Sprint

غاية هذه العروض تأهيل المشتري، وكشف المشكلات الحقيقية، وإنتاج Proof
Pack بأقل التزام من الطرفَين.

### 2. Core Offers — تطبيق عالي القيمة
- Lead Intelligence Sprint
- Company Brain Sprint
- Workflow Automation Sprint
- AI Support Desk Sprint

هذه هي محرّكات النقد الرئيسية. تُقدّم أثراً تجارياً ظاهراً ضمن
نافذة زمنية محدّدة، وتُنتج الأدلّة التي تعتمد عليها خريطة Proof to
Upsell.

### 3. Continuity Offers — متكرّرة
- Monthly RevOps OS
- Monthly AI Ops
- Monthly Support AI
- Monthly Company Brain

تُحوّل الـ Sprints المُثبَتة إلى أنظمة تشغيل مستمرّة، وتُوفّر قاعدة
الإيراد المتكرّر اللازمة لاستثمارات Academy و Platform.

### 4. Enterprise Offers — مُفصّلة
- Enterprise AI OS
- AI Governance Program
- Multi-Branch RevOps

تُباع فقط لعملاء أثبَتوا الثقة عبر Front-end أو Core، وتأخذ تسعيراً
ونطاقاً ومتطلّبات امتثال منفصلة.

## قاعدة التدرّج

> Entry Offer → Core Sprint → Pilot → Retainer → Enterprise.
> لا تقفز إلى Enterprise قبل الدليل.

تخطّي الطبقات — مثل قبول تفويض Enterprise من عميل جديد دون Sprint
مُسبق — ممنوع. القاعدة موجودة لأن مخاطر Enterprise تتطلّب دليل
ملاءمة، ولأن بيع Enterprise مبكراً يُجوّع خطّ أنابيب Proof Packs
الذي يُغذّي كل الإيراد الآخر.

## لماذا الطبقات مهمّة

كل طبقة تُنتج نوعاً مختلفاً من رأس المال:

- Front-end → Trust Capital (Proof Packs)
- Core → Service Capital (عروض وقوالب مُحَسَّنة)
- Continuity → Market Capital (جمهور ومراجع)
- Enterprise → IP Capital (حوكمة، تكامل، عمق)

التوازن بين الطبقات الأربع هو ما يُراكم الشركة.

## قائمة فحص تصميم العرض

لأي عرض جديد يدخل البنية، يجب:

1. أن يقع بوضوح داخل إحدى الطبقات الأربع.
2. أن يحمل KPI أساسياً معرَّفاً في
   `docs/company/SERVICE_KPI_MAP.md`.
3. أن يحمل صف تسعير في
   `docs/OFFER_LADDER_AND_PRICING.md` بهامش يتماشى مع
   `docs/UNIT_ECONOMICS_AND_MARGIN.md`.
4. أن يحدّد Upsell المرجعي من
   `docs/growth/PROOF_TO_UPSELL_MAP.md`.

## الواجهات
| المدخلات | المخرجات | الملاك | الإيقاع |
|---|---|---|---|
| طلب عرض | تصنيف الطبقة | المؤسس | لكل صفقة |
| اقتراح عرض جديد | قرار تموضع في الطبقة | المؤسس | لكل عرض |
| مراجعة ربعية | إجراءات إعادة موازنة الطبقات | المؤسس | ربعياً |
| Pipeline المبيعات | فعلي توزيع الطبقات | المؤسس | أسبوعياً |

## المقاييس
- Tier mix — نسبة الإيراد من Front-end / Core / Continuity / Enterprise؛ الهدف Continuity ≥ 30% بنهاية السنة.
- Progression rate — نسبة عملاء Front-end الذين يتقدّمون إلى Core خلال 6 أشهر؛ الهدف ≥ 40%.
- Premature-Enterprise count — عدد صفقات Enterprise المقبولة بلا دليل مُسبق؛ الهدف 0.
- Continuity attach rate — نسبة تسليمات Core التي تُرفَق بـ Continuity؛ الهدف ≥ 40%.

## ذات صلة
- `docs/OFFER_LADDER_AND_PRICING.md` — طبقة التسعير للبنية.
- `docs/business/MANAGED_PILOT_OFFER.md` — حركة Pilot التي تجسر Core إلى Continuity.
- `docs/COMPANY_SERVICE_LADDER.md` — كتالوج الخدمات المُسقَط على الطبقات.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — نموذج رأس المال الذي تخدمه البنية.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
