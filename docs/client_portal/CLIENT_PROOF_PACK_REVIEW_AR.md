# مراجعة Proof Pack (حزمة الإثبات) عبر البوابة

> **نظام Dealix — Saudi B2B Revenue Operating System**
> الإصدار: 1.0 | التاريخ: 2026-06-03 | المالك: Agent #2
> السكيمة المرجعية: `schemas/proof_pack.schema.json`
> المسار: `/client/proof-pack`

---

## 1. ما هو الـ Proof Pack؟

Proof Pack هو **تقرير التشخيص المدعوم بالأدلة** الذي يُوضح لعميل Dealix:
- أين يتسرب إيراده (leakage points)
- الكسب السريع الأكثر أثرًا (quick win)
- المقارنة قبل/بعد (before-after) كأهداف، لا ضمانات
- خطة القياس والتحقق
- التوصية بالمنتج الملائم للـ pilot

**ثابت لا يتغير:**
```
guaranteed_roi: false  ← دائمًا
confidential:   true   ← دائمًا
```

لا يوجد في Dealix ضمان عائد. كل رقم يحمل `evidence_level` واضح.

---

## 2. حقول Proof Pack (proof_pack.schema.json)

| الحقل | الإلزامية | الوصف |
|---|---|---|
| `id` | إلزامي | `PRF-XXXX` |
| `company` | إلزامي | الشركة العميلة |
| `current_workflow` | إلزامي | وصف العملية الحالية للمبيعات |
| `leakage_points` | إلزامي | مصفوفة نقاط التسرب (انظر §3) |
| `quick_win` | إلزامي | أفضل كسب سريع واحد |
| `before_after` | إلزامي | مقياس + قبل + هدف بعد (ليس ضمانًا) |
| `measurement_plan` | إلزامي | كيف نقيس النتائج |
| `evidence_level` | **إلزامي** | مستوى دليل التقرير الكلي |
| `risks` | إلزامي | المخاطر التي تؤثر على الدقة |
| `recommended_pilot_product_id` | **إلزامي** | يجب أن يكون في كتالوج المنتجات |
| `guaranteed_roi` | `const: false` | **دائمًا خطأ** — لا ضمان عائد |
| `confidential` | `true` افتراضي | سري — لا يُشارك بدون إذن |

---

## 3. نقاط التسرب (leakage_points)

كل نقطة تسرب تحمل:

| الحقل | الوصف |
|---|---|
| `stage` | المرحلة (مثل: `first_response`, `followup`, `proposal`) |
| `description` | وصف المشكلة |
| `estimated_impact_sar` | التأثير المقدَّر بالريال — قابل للـ null |
| `evidence_level` | دليل هذه النقطة تحديدًا |

**القاعدة:** إذا كان `evidence_level=none` أو `assumption` على نقطة تسرب → يجب إبراز هذا التحفظ بوضوح في العرض.

---

## 4. سلّم مستويات الأدلة (evidence_level)

| المستوى | المعنى | هل يكفي لقرار؟ |
|---|---|---|
| `none` | لا دليل | لا — غير مسموح كأساس قرار |
| `assumption` | تقدير داخلي | بتحفظ واضح فقط |
| `benchmark` | معيار صناعة خارجي | نعم بتحفظ |
| `client_reported` | ذكره العميل (غير مُتحقَّق) | نعم بتحفظ |
| `client_data` | من بيانات العميل الفعلية | نعم |
| `measured` | قِسناه أثناء التسليم | نعم — قوي |
| `verified` | نتيجة مُتحقَّقة مستقلًا | نعم — الأقوى |

---

## 5. مثال واقعي: Digital Rise Agency — PRF-1001

| الحقل | القيمة |
|---|---|
| `company` | Digital Rise Agency |
| `current_workflow` | استفسار → رد يدوي متأخر → لا متابعة منظمة |
| `evidence_level` | `client_data` |
| `guaranteed_roi` | `false` |
| `quick_win` | تفعيل SLA رد خلال 15 دقيقة + تذكير متابعة آلي |
| `recommended_pilot_product_id` | `followup_recovery_workflow` |

**نقاط التسرب:**

| المرحلة | المشكلة | التأثير المقدَّر (SAR) | الدليل |
|---|---|---|---|
| `first_response` | متوسط زمن الرد 4.2 ساعة مقابل أفضل ممارسة 15 دقيقة | 18,000 شهريًا | `client_data` |
| `followup` | 37% من الفرص بلا متابعة بعد أول رد | 22,000 شهريًا | `client_data` |

**Before-After (هدف وليس ضمانًا):**

| المقياس | قبل | الهدف بعد |
|---|---|---|
| نسبة المتابعة | 43% | 80%+ |

**خطة القياس:** قياس أسبوعي لزمن الرد ونسبة المتابعة عبر تصدير CRM.

---

## 6. ما يراه العميل في `/client/proof-pack`

- الملخص التنفيذي وأبرز نقاط التسرب.
- كل رقم مصحوب بـ `evidence_level` ظاهر.
- توضيح صريح: **"الأهداف ليست ضمانات — النتائج تعتمد على التنفيذ"**.
- خطة القياس وكيف سنتحقق من الأثر.
- توصية الـ pilot مع ربطها بالكتالوج.

---

## 7. ما لا يحق للنظام فعله

- الادعاء بضمان نسبة تحسين محددة (`guaranteed_roi=false` دائمًا).
- نشر أو مشاركة Proof Pack بدون إذن العميل (`confidential=true`).
- عرض أرقام بدون `evidence_level`.
- استخدام Proof Pack كأداة ضغط مبيعات بوعود غير واقعية.

---

## الروابط المرجعية

- سكيمة Proof Pack: `schemas/proof_pack.schema.json`
- قالب Proof Pack الأساسي: [`company_os/delivery/proof_pack_template.md`](../../company_os/delivery/proof_pack_template.md)
- مصنع Proof Pack: [`../revenue_execution/PROOF_PACK_FACTORY_AR.md`](../revenue_execution/PROOF_PACK_FACTORY_AR.md)
- سياسة البوابة: [`SECURE_CLIENT_PORTAL_AR.md`](SECURE_CLIENT_PORTAL_AR.md)
- الحوكمة الموحّدة: [`AGENTS.md`](../../AGENTS.md)

---

*ينبغي قراءة هذا المستند مع [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لكل وكيل/سكربت/مستند في Dealix.*
