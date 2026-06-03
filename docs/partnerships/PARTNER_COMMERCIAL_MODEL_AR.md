# النموذج التجاري للشركاء — Partner Commercial Model (AR)

اقتصاد نماذج الشركاء الثلاثة لـ Dealix: `referral` · `reseller` · `co_delivery`.
كل نموذج يلتزم أرضية الهامش (≥ 15%) ويمرّ باعتماد المؤسّس.

## النماذج الثلاثة
| النموذج | كيف يعمل | الحقل (`schema`) | أثره على الهامش |
|---------|----------|------------------|-----------------|
| `referral` | الشريك يُحيل عميلاً، ونحن نبيع وننفّذ | `referral_fee_pct` | نسبة إحالة تُخصم من إيرادنا |
| `reseller` | الشريك يعيد البيع بخصم متّفق | `reseller_discount_pct` | الخصم يخفض هامشنا مباشرة |
| `co_delivery` | تسليم مشترك بتقاسم الإيراد | `revenue_share_pct` | الحصّة المشتركة تحدّد صافي هامشنا |

## كيف يُحسب الهامش لكل نموذج
- **referral:** الهامش ≈ إيراد الصفقة − تكلفة التنفيذ − (إيراد × `referral_fee_pct`).
- **reseller:** الهامش ≈ السعر بعد `reseller_discount_pct` − تكلفتنا.
- **co_delivery:** الهامش ≈ حصّتنا من الإيراد (`revenue_share_pct` للشريك) − تكلفتنا.
في كل الحالات: `margin_pct` المُسجَّل يجب أن يكون ≥ `min_margin_pct` (=15).

## أمثلة من البيانات (مرجع `data/partners/partner_opportunities.jsonl`)
- PARTNER-001 (`referral`, `referral_fee_pct=15`, `margin_pct=85`): فوق الأرضية.
- PARTNER-002 (`reseller`, `reseller_discount_pct=20`, `margin_pct=20`): فوق الأرضية.
- PARTNER-003 (`co_delivery`, `revenue_share_pct=40`, `margin_pct=35`): فوق الأرضية.
كلّها `min_margin_pct=15`، `approval_required=true`، `dry_run=true`.

## قواعد الاتّساق
- كل سجلّ يحمل `margin_pct` و`min_margin_pct` و`approval_required` صراحةً
  (مرجع `tests/test_partner_model_margin_rules.py`).
- صفقة تحت الأرضية تُوسَم `below_min_margin` ولا تُعتمد بلا قرار صريح.
- تفاصيل الأرضية والاعتماد: `docs/partnerships/PARTNER_PRICING_AND_MARGIN_AR.md`.

## ممنوعات صارمة
- لا وعود إيراد للشريك، لا أرقام أداء مُختلَقة، لا شهادات/تغطية مزعومة، لا أسماء عملاء.
- لا عبارات محظورة (نضمن/نضاعف الإيرادات/نتائج مضمونة/بدون مخاطرة/10x/
  guaranteed revenue/no risk). الأفعال المسموحة فقط: نساعد/نقلّل/نرتّب/نحلّل/نوضّح/نلاحظ.

## الربط
- نظام القناة: `docs/partnerships/PARTNER_CHANNEL_OS_AR.md`.
- نموذج إيراد القناة: `docs/partnerships/CHANNEL_REVENUE_MODEL_AR.md`.
- المراجعة التجارية: `reports/partnerships/PARTNER_COMMERCIAL_REVIEW.md`.

## مبادئ الصوت
مختصر، واضح، واثق، سعودي، مؤسّسي، عملي. اقتصاد واضح، هامش لا يُكسَر.
