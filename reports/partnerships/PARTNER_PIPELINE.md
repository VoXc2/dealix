# خط الشركاء — Partner Pipeline (قالب تقرير)

قالب تقرير لتتبّع فرص الشركاء عبر التأهيل والاعتماد. كل سجلّ `approval_required=true`
و`dry_run=true` حتى الاعتماد، ويحترم أرضية الهامش (≥ 15%). قالب فارغ يُملأ بحقائق فقط.

## مفتاح الحالة (`status`)
`prospect` → `qualified` → `approved` → `active` (أو `disqualified`).

## الخط (قالب — استبدل الصفوف بسجلّات حقيقية)
| `partner_id` | `name` | `type` | `model` | `margin_pct` | ≥ `min_margin_pct` (15)؟ | `status` | اعتماد المؤسّس |
|--------------|--------|--------|---------|--------------|---------------------------|----------|----------------|
| `[PARTNER-xxx]` | `[الاسم]` | `[type]` | `referral` | `[≥15]` | ☐ | `prospect` | ☐ |
| `[PARTNER-xxx]` | `[الاسم]` | `[type]` | `reseller` | `[≥15]` | ☐ | `prospect` | ☐ |
| `[PARTNER-xxx]` | `[الاسم]` | `[type]` | `co_delivery` | `[≥15]` | ☐ | `prospect` | ☐ |

مرجع البيانات: `data/partners/partner_opportunities.jsonl`
(PARTNER-001/002/003 — كلّها `margin_pct ≥ 15`, `approval_required=true`, `dry_run=true`).

## قواعد التعبئة
- أنواع الشركاء ضمن enum الـ `schema`؛ النماذج: `referral`/`reseller`/`co_delivery`.
- أي صفّ بهامش < 15% يُوسَم `below_min_margin` ولا يُعتمد بلا قرار صريح
  (مرجع `tests/test_partner_model_margin_rules.py`).
- لا ترقية إلى `approved` بلا اعتماد المؤسّس الصريح.
- لا وعود إيراد، لا أرقام أداء مُختلَقة، لا أسماء عملاء، لا PII (الأدوار فقط).
- لا عبارات محظورة؛ الأفعال المسموحة فقط.

## الربط
- نظام القناة: `docs/partnerships/PARTNER_CHANNEL_OS_AR.md`.
- التأهيل: `docs/partnerships/PARTNER_QUALIFICATION_AR.md`.
- المراجعة التجارية: `reports/partnerships/PARTNER_COMMERCIAL_REVIEW.md`.
