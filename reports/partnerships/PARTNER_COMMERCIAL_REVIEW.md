# المراجعة التجارية للشركاء — Partner Commercial Review (قالب تقرير)

قالب تقرير لمراجعة اقتصاد كل صفقة شريك قبل الاعتماد. القاعدة الصلبة: **أرضية هامش
15%، لا أقلّ بلا قرار صريح**. قالب فارغ يُملأ بأرقام حقيقية فقط — لا أرقام مُختلَقة.

## مفتاح القرار
`pass` (هامش ≥ 15 + معتمَد) · `flagged` (`below_min_margin`) · `rejected`.

## المراجعة (قالب — استبدل الصفوف بأرقام حقيقية)
| `partner_id` | `model` | الحقل المالي | `margin_pct` | `min_margin_pct` | الفحص | اعتماد المؤسّس |
|--------------|---------|--------------|--------------|------------------|-------|----------------|
| `[PARTNER-xxx]` | `referral` | `referral_fee_pct=[..]` | `[≥15]` | `15` | `[pass/flagged]` | ☐ |
| `[PARTNER-xxx]` | `reseller` | `reseller_discount_pct=[..]` | `[≥15]` | `15` | `[pass/flagged]` | ☐ |
| `[PARTNER-xxx]` | `co_delivery` | `revenue_share_pct=[..]` | `[≥15]` | `15` | `[pass/flagged]` | ☐ |

## منطق الفحص (مرجع `tests/test_partner_model_margin_rules.py`)
- `margin_pct = 8`, `min_margin_pct = 15` → `flagged` (`below_min_margin`).
- `margin_pct = 15`, `min_margin_pct = 15` → `pass`.
- الشرط العام: `margin_pct >= min_margin_pct` لكل سجلّ.

## قواعد التعبئة
- لا اعتماد لصفّ `flagged` إلا بقرار صريح موثّق من المؤسّس وسبب واضح.
- كل رقم هامش/إيراد حقيقي بمصدر، لا أرقام مُختلَقة للعرض.
- لا وعود إيراد، لا «بدون مخاطرة»، لا أسماء عملاء، لا PII (الأدوار فقط).
- لا عبارات محظورة؛ الأفعال المسموحة فقط.

## الربط
- التسعير والهامش: `docs/partnerships/PARTNER_PRICING_AND_MARGIN_AR.md`.
- النموذج التجاري: `docs/partnerships/PARTNER_COMMERCIAL_MODEL_AR.md`.
- نموذج إيراد القناة: `docs/partnerships/CHANNEL_REVENUE_MODEL_AR.md`.
