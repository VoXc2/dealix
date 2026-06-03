# نظام قناة الشركاء — Partner Channel OS (AR)

نظام تشغيل قناة شركاء Dealix: من نوع الشريك، إلى نموذج التعاون، إلى الاعتماد. كل
علاقة شريك تبدأ `approval_required=true` و`dry_run=true`، ولا تُفعَّل إلا بموافقة المؤسّس.

## أنواع الشركاء (مرجع `schemas/partner_opportunity.schema.json` — `type`)
وكالات تسويق (`marketing_agency`) · مطبّقو CRM (`crm_implementer`) ·
مستشارو أعمال (`business_consultant`) · مكاتب محاسبة (`accounting_firm`) ·
مزوّدو تدريب (`training_provider`) · وكالات ويب (`web_agency`) ·
موزّعو برمجيات (`software_reseller`) · مستشارو عمليات (`operations_consultant`).

## نماذج التعاون (`model`)
| النموذج | الفكرة | الحقل المالي |
|---------|--------|--------------|
| `referral` | الشريك يُحيل، ونحن ننفّذ ونبيع | `referral_fee_pct` |
| `reseller` | الشريك يعيد البيع بخصم | `reseller_discount_pct` |
| `co_delivery` | تسليم مشترك بتقاسم إيراد | `revenue_share_pct` |

الاقتصاد التفصيلي: `docs/partnerships/PARTNER_COMMERCIAL_MODEL_AR.md`.

## أرضية الهامش (إلزامية)
- `min_margin_pct = 15`: أي صفقة شريك بهامش أقلّ من 15% تُوسَم (flagged) ولا تُعتمد
  بلا قرار صريح. مرجع `tests/test_partner_model_margin_rules.py`
  (دالة `below_min_margin`، والاختبار «at-or-above floor passes»).
- التفصيل: `docs/partnerships/PARTNER_PRICING_AND_MARGIN_AR.md`.

## دورة العلاقة (مختصرة)
1. تأهيل الشريك (`docs/partnerships/PARTNER_QUALIFICATION_AR.md`).
2. اختيار النموذج المناسب وفحص الهامش (≥ 15%).
3. اعتماد المؤسّس (`approval_required=true`).
4. تجهيز الشريك (`docs/partnerships/PARTNER_ENABLEMENT_KIT_AR.md`).
5. التسجيل في `reports/partnerships/PARTNER_PIPELINE.md`.

أمثلة السجلّات: `data/partners/partner_opportunities.jsonl`
(PARTNER-001 referral، PARTNER-002 reseller، PARTNER-003 co_delivery) — كلّها
`approval_required=true`، `dry_run=true`، و`margin_pct ≥ min_margin_pct`.

## ممنوعات صارمة
- لا إثبات مُختلَق في أي مادة شريك: لا جوائز، لا تغطية، لا شهادات، لا أسماء عملاء، لا أرقام بلا مصدر.
- لا عبارات محظورة (نضمن/نضاعف الإيرادات/نتائج مضمونة/بدون مخاطرة/10x/
  guaranteed revenue/no risk). الأفعال المسموحة فقط: نساعد/نقلّل/نرتّب/نحلّل/نوضّح/نلاحظ.
- لا PII (الأدوار فقط).

## مبادئ الصوت
مختصر، واضح، واثق، سعودي، مؤسّسي، عملي. هامش منضبط، اعتماد لكل علاقة.
