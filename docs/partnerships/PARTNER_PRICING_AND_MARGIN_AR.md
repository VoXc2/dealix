# تسعير الشركاء وأرضية الهامش — Partner Pricing & Margin (AR)

سياسة التسعير والهامش لصفقات الشركاء. القاعدة الصلبة: **أرضية هامش 15%، لا أقلّ
أبداً بلا قرار صريح**، وكل صفقة تمرّ باعتماد المؤسّس.

## أرضية الهامش (Margin Floor)
- `min_margin_pct = 15` لكل سجلّ شريك (مرجع `schemas/partner_opportunity.schema.json`).
- الشرط الصلب: `margin_pct >= min_margin_pct`.
- صفقة بهامش أقلّ من 15% تُوسَم `below_min_margin` وتُحجَب عن الاعتماد التلقائي.
- مرجع الاختبارات `tests/test_partner_model_margin_rules.py`:
  - «below floor is flagged»: `margin_pct=8` مع `min_margin_pct=15` → `below_min_margin`.
  - «at or above floor passes»: `margin_pct=15` مع `min_margin_pct=15` → يمرّ.
  - كل سجلّات `data/partners/partner_opportunities.jsonl`: `margin_pct ≥ min_margin_pct`
    و`approval_required=true`.

## التسعير حسب النموذج
| النموذج | ضابط التسعير | الحدّ |
|---------|--------------|------|
| `referral` | `referral_fee_pct` لا يُنزِل الهامش تحت 15% | يُرفض إن خرق الأرضية |
| `reseller` | `reseller_discount_pct` لا يُنزِل الهامش تحت 15% | يُرفض إن خرق الأرضية |
| `co_delivery` | `revenue_share_pct` يترك لنا هامشاً ≥ 15% | يُرفض إن خرق الأرضية |

التسعير يبقى ضمن أسعار السلّم `DLX-L0..L6` (مرجع اصطلاحات السوق)؛ لا خصم يكسر الأرضية.

## مسار الاعتماد
1. حساب `margin_pct` للنموذج المختار.
2. التحقّق `margin_pct >= 15`؛ إن لا → وسم `below_min_margin` وإيقاف.
3. إن كان على/فوق الأرضية → عرض على المؤسّس.
4. موافقة المؤسّس الصريحة (`approval_required=true`) قبل أي تفعيل.
5. التسجيل في `reports/partnerships/PARTNER_COMMERCIAL_REVIEW.md`.

## استثناء تحت الأرضية (نادر ومضبوط)
- لا اعتماد تحت 15% إلا بقرار صريح موثّق من المؤسّس وسبب واضح.
- الوضع الافتراضي: الرفض، لا الاستثناء.

## ممنوعات صارمة
- لا «بدون مخاطرة» على الشريك، لا وعد إيراد، لا أرقام هامش مُختلَقة للعرض.
- لا عبارات محظورة (نضمن/نضاعف الإيرادات/نتائج مضمونة/بدون مخاطرة/10x/
  guaranteed revenue/no risk). الأفعال المسموحة فقط: نساعد/نقلّل/نرتّب/نحلّل/نوضّح/نلاحظ.
- لا أسماء عملاء، لا PII (الأدوار فقط).

## الربط
- النموذج التجاري: `docs/partnerships/PARTNER_COMMERCIAL_MODEL_AR.md`.
- نموذج إيراد القناة وقواعد الهامش: `docs/partnerships/CHANNEL_REVENUE_MODEL_AR.md`.

## مبادئ الصوت
مختصر، واضح، واثق، سعودي، مؤسّسي، عملي. أرضية 15% لا تُكسَر بلا قرار صريح.
