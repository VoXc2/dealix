# مصنع أدلة الإثبات (Proof Pack Factory)

> **نظام Dealix — Saudi B2B Revenue Operating System**
> الإصدار: 1.0 | التاريخ: 2026-06-03 | المالك: Agent #2
> السكيمة المرجعية: `schemas/proof_pack.schema.json`
> القالب الأساسي (لا يُعاد كتابته): [`company_os/delivery/proof_pack_template.md`](../../company_os/delivery/proof_pack_template.md)

---

## 1. العلاقة بالقالب الأساسي

هذا المستند **يوسّع ويربط** القالب الأساسي في `company_os/delivery/proof_pack_template.md` — لا يُعيد كتابته. القالب الأساسي يُعرّف هيكل التقرير (الأقسام 1-7 + الملحق). هذا المصنع يُضيف:

- حقول السكيمة الإلزامية لكل قسم.
- قواعد `evidence_level` لكل رقم.
- بوابة موافقة المؤسس قبل مشاركة Proof Pack مع العميل.
- ربط `recommended_pilot_product_id` بالكتالوج.
- ثابت `guaranteed_roi=false` وتطبيقه.

---

## 2. هيكل المصنع: من البيانات إلى الإثبات

```
[1] جمع البيانات (عبر البوابة — client_upload + client_permission)
            ↓
[2] تشغيل التحليل (محليًا، بيانات مُخفاة الهوية)
            ↓
[3] بناء proof_pack (id: PRF-XXXX)
    - leakage_points: كل نقطة لها evidence_level
    - quick_win: أفضل كسب سريع واحد
    - before_after: هدف (ليس ضمانًا)
    - measurement_plan: كيف نُثبت الأثر
            ↓
[4] مراجعة المؤسس → موافقة (L4)
            ↓
[5] مشاركة مع العميل في /client/proof-pack
```

---

## 3. نقاط التسرب (leakage_points) — القلب النابض للـ Proof Pack

| الحقل | إلزامي | الوصف |
|---|---|---|
| `stage` | نعم | المرحلة: `first_response`, `followup`, `proposal`, `close` |
| `description` | نعم | وصف المشكلة بدقة |
| `estimated_impact_sar` | اختياري | التأثير المالي المُقدَّر — null إن لم يكن قابلًا للتقدير |
| `evidence_level` | **نعم** | مستوى دليل هذه النقطة تحديدًا |

**قاعدة العرض:** كل رقم `estimated_impact_sar` يُعرَض مصحوبًا بـ `evidence_level` الخاص به. لا أرقام بدون مصدر.

### جدول تفسير evidence_level للعميل

| المستوى | ما نقوله للعميل |
|---|---|
| `assumption` | "تقدير مبدئي بناءً على معايير السوق — سيُحسَّن بعد تحليل بياناتك" |
| `benchmark` | "معيار صناعة موثّق من مصادر خارجية" |
| `client_reported` | "بناءً على ما أفدتنا به — لم نُتحقَّق منه بعد من البيانات" |
| `client_data` | "محسوب من بياناتك الفعلية" |
| `measured` | "قِسناه مباشرةً أثناء التسليم" |
| `verified` | "نتيجة مُتحقَّقة من طرف مستقل" |

---

## 4. الكسب السريع (quick_win)

- إجراء واحد قابل للتنفيذ خلال أسبوع.
- له أعلى عائد/جهد من نقاط التسرب.
- يُرتبط بـ `recommended_pilot_product_id` عند الاقتضاء.

**مثال (Digital Rise Agency):** "تفعيل SLA رد خلال 15 دقيقة + تذكير متابعة آلي" — يُعالج نقطتي التسرب الأكبر في آنٍ واحد.

---

## 5. المقارنة قبل/بعد (before_after)

```json
{
  "metric": "نسبة المتابعة",
  "before": "43%",
  "after_target": "80%+ (هدف وليس ضمان)"
}
```

**إلزامي:** عبارة "(هدف وليس ضمان)" في `after_target`. النتائج تعتمد على تنفيذ العميل.

---

## 6. خطة القياس (measurement_plan)

تُحدد:
- الأداة / المصدر (تصدير CRM، تقارير أسبوعية، لوحة متابعة).
- الإيقاع الزمني (يومي / أسبوعي / شهري).
- المسؤول عن القياس.
- الأساس المرجعي قبل التدخل (`before`).

---

## 7. ربط توصية الـ Pilot بالكتالوج

`recommended_pilot_product_id` يجب أن يكون في `data/catalog/product_catalog.json`:

| بعد تشخيص `revenue_leakage_diagnostic` → يُوصى بـ | product_id |
|---|---|
| إذا المشكلة = ضعف متابعة | `followup_recovery_workflow` |
| إذا المشكلة = غياب نظام شامل | `ai_revenue_ops_starter` |
| إذا الشركة كبيرة/معقدة | `full_revenue_os` |
| إذا يحتاج تحسين مستمر | `monthly_optimization` |

---

## 8. ثوابت Proof Pack الأمنية

| الحقل | القيمة | السبب |
|---|---|---|
| `guaranteed_roi` | `false` دائمًا (const) | لا ضمان عائد — ثابت في السكيمة |
| `confidential` | `true` افتراضيًا | سري — لا يُشارك بدون إذن العميل |
| `evidence_level` | إلزامي على مستوى التقرير | كل Proof Pack له مستوى دليل كلي |

---

## 9. مثال كامل: Digital Rise Agency — PRF-1001

| الحقل | القيمة |
|---|---|
| `id` | PRF-1001 |
| `company` | Digital Rise Agency |
| `current_workflow` | استفسار → رد يدوي متأخر → لا متابعة منظمة → عرض بدون قياس |
| `evidence_level` | `client_data` |
| `quick_win` | تفعيل SLA رد 15 دقيقة + تذكير متابعة |
| `before_after.metric` | نسبة المتابعة |
| `before_after.before` | 43% |
| `before_after.after_target` | 80%+ (هدف وليس ضمان) |
| `measurement_plan` | قياس أسبوعي عبر تصدير CRM |
| `recommended_pilot_product_id` | `followup_recovery_workflow` |
| `guaranteed_roi` | false |

نقاط التسرب:
- `first_response`: زمن رد 4.2 ساعة → تأثير 18,000 SAR/شهر (`client_data`)
- `followup`: 37% فرص بلا متابعة → تأثير 22,000 SAR/شهر (`client_data`)

---

## 10. بوابة موافقة المؤسس قبل المشاركة

```
PRF-XXXX مكتمل
    ↓ كارت إجراء: type=generate_proof_pack → يُطرح على المؤسس
    ↓ موافقة المؤسس (L4)
    ↓ جلسة بوابة للعميل: /client/proof-pack
```

---

## الروابط المرجعية

- قالب Proof Pack الأساسي: [`company_os/delivery/proof_pack_template.md`](../../company_os/delivery/proof_pack_template.md) ← **لا تُعِد كتابته**
- سكيمة Proof Pack: `schemas/proof_pack.schema.json`
- مراجعة العميل: [`../client_portal/CLIENT_PROOF_PACK_REVIEW_AR.md`](../client_portal/CLIENT_PROOF_PACK_REVIEW_AR.md)
- كتالوج المنتجات: `data/catalog/product_catalog.json`
- مصنع العروض: [`PROPOSAL_FACTORY_AR.md`](PROPOSAL_FACTORY_AR.md)
- الحوكمة الموحّدة: [`AGENTS.md`](../../AGENTS.md)

---

*ينبغي قراءة هذا المستند مع [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لكل وكيل/سكربت/مستند في Dealix.*
