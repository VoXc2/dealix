# 7-Day Governed Revenue & AI Ops Diagnostic — كتاب تشغيل التشخيص في 7 أيام
<!-- Owner: Founder | Date: 2026-05-17 | Reconciled to the Governed Revenue & AI Ops ladder (D-003) -->

> **الغرض:** كتاب التشغيل اليومي للعرض العام لـ Dealix — التشخيص في 7 أيام للإيراد المُحوكَم وعمليات الذكاء الاصطناعي.
> **Purpose:** the day-by-day playbook for Dealix's public offer — the 7-Day Governed Revenue & AI Ops Diagnostic.
>
> مرجع الفئة والأسعار: [`../strategic/GOVERNED_REVENUE_AI_OPS_STRATEGY.md`](../strategic/GOVERNED_REVENUE_AI_OPS_STRATEGY.md) · [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).

## دور هذه الوثيقة — Role of this document

### عربي
هذا هو **العرض العام** لـ Dealix: العميل يدخل عبر سير عمل واحد محدد، فنُنتج له صورة بالأدلة لفجوات الإيراد وعمليات الذكاء الاصطناعي، وأعلى 3 قرارات جاهزة للتنفيذ، وحزمة إثبات. التشخيص يبيع **القرار**، لا الأداة. المُخرج النهائي للأسبوع: توصية واضحة بـ Revenue Intelligence Sprint أو إغلاق نظيف.

### English
This is Dealix's **public offer**: the customer enters through one defined workflow; we produce an evidenced picture of their revenue and AI-ops gaps, a top-3 set of execute-ready decisions, and a proof pack. The diagnostic sells the **decision**, not the tool. The end-of-week output is a clear recommendation for a Revenue Intelligence Sprint, or a clean close-out.

## التسعير — Pricing (4 tiers)

| الشريحة — Tier | السعر — Price | النطاق — Scope |
|---|---|---|
| Starter Diagnostic | 4,999 SAR | سير عمل واحد، شركة صغيرة |
| Standard Diagnostic | 9,999 SAR | عدة سير عمل، شركة متوسطة |
| Executive Diagnostic | 15,000 SAR | قيادة تنفيذية، خريطة حدود موافقة + مذكرة قرار |
| Enterprise Diagnostic | 25,000 SAR | مؤسسة متعددة الوحدات، حوكمة + جاهزية بيانات |

الترقية: → Revenue Intelligence Sprint (25,000 SAR+) → Governed Ops Retainer (4,999–35,000 SAR/شهر).

---

## Day 1 — سير العمل والمالك — Workflow Map + Named Owner

**ما يحدث — What runs:** مكالمة انطلاق (45 دقيقة) + Source Passport draft.

- تأكيد **مالك سير عمل مُسمّى** لدى العميل (Non-Negotiable #9). بلا مالك لا يبدأ التشخيص.
- تحديد **سير عمل واحد** للتشخيص (مثلاً: إحياء الحسابات الخاملة، أو تأهيل الاستفسارات).
- رسم **خريطة سير العمل**: الخطوات، المدخلات، المخرجات، نقاط القرار.
- توقيع Source Passport: `owner`, `source_type` (`client_upload` / `crm_export` / `manual_entry` — never `scraped`), `allowed_use`, `pii_flag`, `retention_days`.

**نقطة تحقّق المؤسس:** خريطة سير العمل + Source Passport هما العقد. بلا مالك مُسمّى لا يبدأ التشخيص.
**المُخرَج:** Workflow Map v1.

---

## Day 2 — مراجعة المصدر وجودة البيانات — Source & Data Quality Review

**ما يحدث — What runs:** قراءة عيّنة غير مُتلِفة ثم فحص جودة البيانات على الأبعاد الستة (اكتمال، صحة، تفرّد، اتساق، حداثة، مطابقة).

- استيراد عيّنة بـ `preview-only`، ثم احتساب درجة DQ.
- توثيق DQ baseline. DQ < 40 → مشكلة جاهزية بيانات، لا مشكلة تشخيص: يُقترح عرض **CRM/Data Readiness for AI** المجاور. DQ 40–70 → متابعة مع تحفّظات موثّقة. DQ ≥ 70 → متابعة نظيفة.

**نقطة تحقّق المؤسس:** مراجعة DQ score. لا فعل خارجي.
**المُخرَج:** Source & DQ Review.

---

## Day 3 — خريطة حدود الموافقة — Approval-Boundary Map

**ما يحدث — What runs:** تصنيف كل فعل في سير العمل على مستويات المخاطرة الأربعة.

- لكل فعل: `risk_level` ∈ {Low, Medium, High, Critical}، والإجراء المقابل (مسودة / موافقة / موافقة مؤسس + دليل / لا تنفيذ آلي).
- تحديد **بوابات الموافقة**: أين يتوقّف سير العمل لانتظار قرار بشري.
- توثيق ما لا يُؤتمت إطلاقاً (عقود، تسعير، بيانات حساسة، تواصل مع جهة تنظيمية).

**نقطة تحقّق المؤسس:** كل فعل High/Critical له بوابة موافقة صريحة. لا "فعل سحري" بلا بوابة.
**المُخرَج:** Approval-Boundary Map.

---

## Day 4 — فجوات الأدلة — Evidence Gaps

**ما يحدث — What runs:** تحديد أين يفتقر سير العمل إلى دليل قابل للتحقّق.

- لكل قرار في سير العمل: هل يوجد دليل؟ ما مصدره؟ هل قابل للتحقّق؟
- توثيق **فجوات الأدلة**: قرارات تُتّخذ اليوم بلا دليل، وما يلزم لسدّها.
- ربط كل فجوة بأثرها على الإيراد وبخطوة سدّها.

**نقطة تحقّق المؤسس:** كل فجوة موصوفة بصدق؛ لا مبالغة ولا ادعاء قدرة غير موجودة.
**المُخرَج:** Evidence Gap Register.

---

## Day 5 — أعلى 3 قرارات — Top-3 Decisions

**ما يحدث — What runs:** تجميع التشخيص في **أعلى 3 قرارات جاهزة للتنفيذ**.

- لكل قرار: ماذا، لماذا الآن، الدليل الداعم، المخاطرة، بوابة الموافقة، الأثر التقديري على الإيراد.
- ترتيب القرارات بأثر/جهد شفّاف وقابل للشرح.
- صياغة ثنائية اللغة (AR + EN) مُتكافئة، لا ملخّص.

**نقطة تحقّق المؤسس:** كل قرار له تبرير مقروء؛ لا قرار بلا دليل. لا لغة نتيجة مضمونة.
**المُخرَج:** Top-3 Decisions (bilingual).

---

## Day 6 — حزمة الإثبات — Proof Pack Assembly

**ما يحدث — What runs:** تجميع حزمة الإثبات وفق المعيار: استقبال، Source Passport، DQ، خريطة سير العمل، خريطة حدود الموافقة، فجوات الأدلة، أعلى 3 قرارات، قيود، منهجية، توقيعات.

- كل قسم إلزامي؛ القسم الناقص يُفشل التجميع.
- احتساب proof score. `proof_score < 70` لا يُسلَّم — تصعيد للعلاج أو رد جزئي وفق [REFUND_SOP](../REFUND_SOP.md).

**نقطة تحقّق المؤسس:** قراءة حزمة الإثبات من البداية للنهاية. لا placeholders، لا إثبات مزيّف.
**المُخرَج:** Proof Pack (proof_score مُسجَّل).

---

## Day 7 — توصية الـ Sprint والملخص الآمن — Sprint Recommendation + Case-Safe Summary

**ما يحدث — What runs:** مكالمة تسليم (60 دقيقة) تشرح حزمة الإثبات قسماً قسماً، ثم توصية واضحة.

- **توصية Sprint:** هل ينتقل العميل إلى Revenue Intelligence Sprint (25,000 SAR+)؟ التوصية مبنية على proof score، وجود مالك سير عمل، وتجدّد Source Passport.
- تسجيل **أصل رأسمالي** واحد على الأقل قابل لإعادة الاستخدام (قاعدة ترتيب، قالب، نمط حوكمة، رؤية قطاعية).
- صياغة **ملخص آمن** مجهول الهوية وفق قالب [docs/case-studies/](../case-studies/) — لا اسم عميل، لا أرقام تُعرّف، صريح أنه "Hypothetical / case-safe template" إن لم يُسمَّ عميل حقيقي.

**نقطة تحقّق المؤسس:** التوصية صادقة — Sprint فقط عند استيفاء المعايير، وإلا تشخيص ثانٍ أو إغلاق نظيف.
**المُخرَج:** Sprint Recommendation + Case-Safe Summary draft. التشخيص يُعلَّم `status=delivered`.

---

## معايير الخروج — Exit Criteria

التشخيص يُعدّ **مُسلَّماً** فقط عند:

- وجود Source Passport.
- خريطة سير العمل + خريطة حدود الموافقة + سجل فجوات الأدلة مكتملة.
- أعلى 3 قرارات ثنائية اللغة مُتكافئة.
- حزمة إثبات `proof_score >= 70` بكل أقسامها.
- موافقة المؤسس مُسجَّلة على التسليم النهائي.
- توصية Sprint مُوثّقة + مسودة ملخص آمن.

تحت `proof_score = 70` لا يُسلَّم — تمديد (بخصم المؤسس لا غرامة العميل) أو رد وفق [REFUND_SOP](../REFUND_SOP.md).

---

## الممنوعات — Boundaries (non-negotiables)

- لا scraping، لا توعية باردة آلية، لا أتمتة LinkedIn.
- لا إرسال خارجي بلا موافقة صريحة من العميل.
- لا ضمان صفقات أو ROI — استبدل بـ "فرص مُثبتة بأدلة / evidenced opportunities".
- لا PII في حزمة الإثبات أو السجلات — أعداد فقط، لا أسماء.
- إذا طلب العميل فعلاً ممنوعاً → رفض مُسجَّل، إنهاء نظيف، رد الجزء غير المكتسب.

---

## روابط مرجعية — Cross-references

- كتاب تشغيل التسليم اليومي: [SPRINT_DELIVERY_PLAYBOOK.md](./SPRINT_DELIVERY_PLAYBOOK.md)
- إجراءات Risk Score المجاني: [DIAGNOSTIC_DELIVERY_SOP.md](./DIAGNOSTIC_DELIVERY_SOP.md)
- سلم العروض والأسعار: [OFFER_LADDER_AND_PRICING.md](../OFFER_LADDER_AND_PRICING.md)
- الاستراتيجية الكاملة: [GOVERNED_REVENUE_AI_OPS_STRATEGY.md](../strategic/GOVERNED_REVENUE_AI_OPS_STRATEGY.md)
- قالب العرض (Jinja2): [PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2](../../templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2)

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
